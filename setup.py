#!/usr/bin/env python

from setuptools import setup

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]



reqs = parse_requirements('requirements.txt')

setup(name='amazon-ses-template-editor',
      version='0.5.0',
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
