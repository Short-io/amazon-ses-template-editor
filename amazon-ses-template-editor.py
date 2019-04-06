#!/usr/bin/env python3
import boto3
from pathlib import Path
import argparse
import json
import toml
import http.server
import socketserver

ses = boto3.client('ses')

def _get_template_by_path(config, name):
    for template_conf in config['templates']:
        if template_conf['name'] == name:
            return template_conf

def upload_test(config, args):
    upload(config, args, 'test-')


def upload(config, args, prefix=''):
    for template_conf in config['templates']:
        if args.template is not None and template_conf['name'] != args.template:
            continue
        html_part = open(template_conf['html']).read()
        for partial_name, partial in config.get('partials', []).items():
            partial_text = '{{#* inline \"%s\"}}' % partial_name
            partial_text += open(partial).read()
            partial_text += '{{/inline~}}'
            html_part = partial_text + html_part
        text_part = open(template_conf['text']).read() if template_conf.get('text') else ''
        if not ses.get_template(TemplateName=prefix + template_conf['name']):
            print("Created template " + template_conf['name'])
            ses.create_template(Template=dict(
                TemplateName=prefix + template_conf['name'],
                SubjectPart=template_conf['subject'],
                TextPart=text_part,
                HtmlPart=html_part,
            ))
        else:
            print("Updated template " + template_conf['name'])
            ses.update_template(Template=dict(
                TemplateName=prefix + template_conf['name'],
                SubjectPart=template_conf['subject'],
                TextPart=text_part,
                HtmlPart=html_part,
            ))

def test(config, args):
    for test in config['test']:
        if args.template is not None and test['template'] != args.template:
            continue
        res = ses.send_templated_email(
            Destination=dict(
                ToAddresses=config['tests']['to'],
            ),
            Source=config['tests']['from'],
            Template='test-' + test['template'],
            TemplateData=json.dumps(test['data']),
            ConfigurationSetName='template',
        )
        print(res)

def configure_handler(config):
    class HB2Handler(http.server.BaseHTTPRequestHandler):
        def render_template(self, template_name):
            matching_templates = list(filter(lambda t: t['template'] == template_name, self.config['test']))
            if not matching_templates:
                self.send_response(404)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            test_config = matching_templates[0]
            template_path = _get_template_by_path(self.config, test_config['template'])['html']
            content = open(template_path).read()
            for partial_name, partial_file in self.config['partials'].items():
                partial_content = open(partial_file).read()
                self.wfile.write(f"""<script class="__partial" id="{partial_name}" type="text/x-handlebars-template">{partial_content}</script>""".encode())
            self.wfile.write(f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.0.11/handlebars.min.js"></script>
            <script id="entry-template" type="text/x-handlebars-template">{content}</script>
            <body>
            <div id="root"></div>
            <script type="text/javascript">
            var source   = document.getElementById("entry-template").innerHTML;
            for (var partial of document.getElementsByClassName("__partial"))
                Handlebars.registerPartial(partial.id, partial.innerHTML);
            var template = Handlebars.compile(source, {{strict: true}});
            var context = {json.dumps(test_config['data'])};
            var html    = template(context);
            document.getElementById("root").innerHTML = html;
            </script>
            </body>
            """.encode())

        def render_template_list(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><body>")
            for test_config in self.config['test']:
                self.wfile.write(f"""<li><a href="/{test_config['template']}">{test_config['template']}</a>""".encode())

        def do_GET(self):
            if self.path == '/':
                self.render_template_list()
            else:
                self.render_template(self.path.replace('/', ''))
    HB2Handler.config = config
    return HB2Handler

def preview(config, args):
    Handler = configure_handler(config)
    httpd = socketserver.TCPServer(("", 8654), Handler, bind_and_activate=False)
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    print("serving at port", 8654)
    httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', required=False, default='config.toml', help='Path to configuration file, default ./config.toml')
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True
    upload_parser = subparsers.add_parser('upload', help='Uploads templates from configuration file to SES using your system credentials')
    upload_parser.add_argument('-t', '--template', dest='template', help='Uploads only one template with given name')
    upload_test_parser = subparsers.add_parser('upload_test', help='Uploads templates for testing purposes')
    upload_test_parser.add_argument('-t', '--template', dest='template', help='Uploads only one template with given name')
    test_parser = subparsers.add_parser('test', help='Sends emails to your email address so you can test layout')
    test_parser.add_argument('-t', '--template', dest='template', help='Uploads only one template with given name')
    subparsers.add_parser('preview', help='Starts minimal http server for email template testing')
    args = parser.parse_args()
    if args.subcommand:
        locals()[args.subcommand](toml.load(args.config), args)
