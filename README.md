# amazon-ses-template-editor
Console command to edit, test and upload amazon SES templates

# Usage

```bash
pip install amazon-ses-template-editor
amazon-ses-template-editor.py -c config.toml upload
amazon-ses-template-editor.py -c config.toml test
```

# Config example

```toml
[[templates]]
name = 'weekly-email'
html = "templates/weekly-email.hb2"
title = 'Your links weekly report'

[partials]
footer = 'partials/footer.hb2'

[tests]
from = 'andrii@short.cm'
to = 'andrey@kostenko.name'
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
