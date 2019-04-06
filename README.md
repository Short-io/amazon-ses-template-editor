# Create, preview, test and upload Amazon SES templates

[![Maintainability](https://api.codeclimate.com/v1/badges/2c5997ebabeaf46de9d8/maintainability)](https://codeclimate.com/github/Short-cm/amazon-ses-template-editor/maintainability)

Console command to edit, test and upload amazon SES templates

Currently AWS SES has API endpoint to create email templates with handlebars syntax and API endpoint to send emails with template name and a dictionary with template variables.
But it does not provide any UI to create and edit templates. This script allows you to manage your email templates from command line

# Installation

```bash
pip install amazon-ses-template-editor
```

# Usage
```
usage: amazon-ses-template-editor.py [-h] [-c CONFIG]
                                     {upload,test,preview} ...

positional arguments:
  {upload,test,preview}
    upload              Uploads templates from configuration file to SES using
                        your system credentials
    upload_test         Uploads templates for testing purposes
    test                Sends emails to your email address so you can test
                        layout
    preview             Starts minimal http server for email template testing

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to configuration file, default ./config.toml
```

## Uploading emails
```
usage: amazon-ses-template-editor.py upload [-h] [-t TEMPLATE]

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Uploads only one template with given name
```
## Testing emails
```
usage: amazon-ses-template-editor.py upload_test [-h] [-t TEMPLATE]

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Uploads only one template with given name


usage: amazon-ses-template-editor.py test [-h] [-t TEMPLATE]

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Uploads only one template with given name
```

## Testing emails

# Config example

```toml
[[templates]]
name = 'weekly-email'
html = "templates/weekly-email.hb2"
title = 'Your links weekly report'

[[templates]]
name = 'confirmation-email'
html = "templates/confirmation-email.hb2"
title = 'Please verify your email'

[partials]
footer = 'partials/footer.hb2'

[tests]
from = 'andrii@short.cm'
to = ['andrey@kostenko.name', 'someone_else@short.cm']

[[test]]
template = 'weekly-email'
    [test.data]
        encodedEmail = 'andrey@kostenko.name'
        [test.data.user]
        id = 12345
        name = 'Test test'
        [[test.data.domains]]
            [test.data.domains.domain]
            hostname = 'test.com'
            [test.data.domains.stats]
            links = 50
            clicks = 50
            humanClicks = 50
            [[test.data.domains.stats.device]]
            deviceName = "Desktop"
            score = 12345
```

# Author

Andrii Kostenko, Short.cm Inc (https://short.cm)
