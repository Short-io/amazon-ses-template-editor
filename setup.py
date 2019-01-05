#!/usr/bin/env python

from setuptools import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

setup(name='amazon-ses-template-editor',
      version='0.4.6',
      description='A tool for editing, uploading and testing Amazon SES email templates',
      author='Andrii Kostenko',
      author_email='andrii@short.cm',
      scripts=['amazon-ses-template-editor.py'],
      long_description_content_type="text/markdown",
      long_description=open('README.md').read(),
      install_requires=reqs,
      url='https://github.com/Short-cm/amazon-ses-template-editor',
      python_requires='>=3.4.0',
     )
