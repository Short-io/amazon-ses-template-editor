import boto3
from pathlib import Path
import argparse
import json
import toml

ses = boto3.client('ses')

def upload(config):
    for template_conf in config['templates']:
        html_part = open(template_conf['html']).read()
        for partial_name, partial in config.get('partials', []).items():
            partial_text = '{{#* inline \"%s\"}}' % partial_name
            partial_text += open(partial).read()
            partial_text += '{{/inline~}}'
            html_part = partial_text + html_part
        text_part = open(template_conf['text']).read() if template_conf.get('text') else ''
        try:
            ses.create_template(Template=dict(
                TemplateName=template_conf['name'],
                SubjectPart=template_conf['subject'],
                TextPart=text_part,
                HtmlPart=html_part,
            ))
        except ses.exceptions.AlreadyExistsException:
            ses.update_template(Template=dict(
                TemplateName=template_conf['name'],
                SubjectPart=template_conf['subject'],
                TextPart=text_part,
                HtmlPart=html_part,
            ))

def test(config):
    for test in config['test']:
        res = ses.send_templated_email(
            Destination=dict(
                ToAddresses=[config['tests']['to']],
            ),
            Source=config['tests']['from'],
            Template=test['template'],
            TemplateData=json.dumps(test['data']),
            ConfigurationSetName='template',
        )
        print(res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', required=False, default='config.toml', help='Path to configuration file, default ./config.toml')
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True
    subparsers.add_parser('upload', help='Uploads templates from configuration file to SES using your system credentials')
    subparsers.add_parser('test', help='Sends emails to your email address so you can test layout')
    args = parser.parse_args()
    if args.subcommand:
        locals()[args.subcommand](toml.load(args.config))