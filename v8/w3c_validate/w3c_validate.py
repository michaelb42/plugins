# -*- coding: utf-8 -*-

# Copyright © 2018 Michael Brakemeier

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""W3C HTML Validator plugin for generated content."""

from html.parser import HTMLParser
import os
import os.path

import logbook
from nikola.plugin_categories import Command

from py_w3c.validators.html.validator import HTMLValidator

class CommandW3CValidate(Command):
    """W3C HTML Validator plugin for generated content."""

    name = "w3c_validate"

    errors_only = False

    posts_only = False
    validate_extensions = ['html']

    verbose = False

    doc_usage = "[-p, --posts] [-v, --verbose] [-e, --errors-only]"
    doc_purpose = "validate generated HTML using the W3C HTML Validator service."
    cmd_options = [
        {
            'name': 'errors-only',
            'long': 'errors-only',
            'short': 'e',
            'type': bool,
            'default': False,
            'help': 'Show only errors.',
        },
        {
            'name': 'posts',
            'long': 'posts',
            'short': 'p',
            'type': bool,
            'default': False,
            'help': 'Validate posts and pages only.',
        },
        {
            'name': 'verbose',
            'long': 'verbose',
            'short': 'v',
            'type': bool,
            'default': False,
            'help': 'Be more verbose.',
        },
    ]

    def _execute(self, options, args):
        """W3C HTML Validator plugin for generated content."""

        if options['errors-only']:
            self.errors_only = True

        if options['posts']:
            self.posts_only = True

        if options['verbose']:
            self.verbose = True
            self.logger.level = logbook.DEBUG
        else:
            self.logger.level = logbook.INFO

        self.site.scan_posts()

        self.logger.info("Sending validation requests. This can take some time....")

        self.validate_files()


    def validate_files(self):
        """
        Validate a generated HTML file
        """
        self.logger.debug("Validate files:")
        self.logger.debug("===============\n")
        not_found = True
        output_folder = self.site.config['OUTPUT_FOLDER']

        if self.posts_only:
            for post in self.site.timeline:
                for lang in self.site.config['TRANSLATIONS'].keys():
                    destination_path = post.destination_path(lang)
                    filepath = os.path.join(output_folder, destination_path)
                    if self.should_validate(filepath) and os.path.isfile(filepath):
                        not_found = False
                        self.validate(filepath)
        else:
            for dirpath, _, filenames in os.walk(output_folder):
                for name in filenames:
                    if self.should_validate(name):
                        not_found = False
                        filepath = os.path.join(dirpath, name)
                        self.validate(filepath)

        if not_found:
            self.logger.warn('Got no files to validate.')


    def validate(self, filename):
        """
        Use W3C validator service: https://bitbucket.org/nmb10/py_w3c/ .
        :param filename: the filename to validate
        """

        html_parser = HTMLParser()  # for unescaping WC3 messages

        vld = HTMLValidator()
        self.logger.info("Validating: {0}".format(filename))

        # call w3c webservice
        vld.validate_file(filename)

        # display errors, warnings and notices
        for err in vld.errors:
            self.logger.error(u'line: {0}; col: {1}; message: {2}'.
                              format(err['lastLine'], err['firstColumn'],
                                     html_parser.unescape(err['message'])))
            self.logger.debug('extract: {0}'.format(err['extract']))

        if not self.errors_only:
            for warn in vld.warnings:
                self.logger.warning(u'line: {0}; col: {1}; message: {2}'.
                                    format(warn['lastLine'], warn['firstColumn'],
                                           html_parser.unescape(warn['message'])))
                self.logger.debug('extract: {0}'.format(warn['extract']))

            for info in vld.info:
                self.logger.info(u'line: {0}; col: {1}; {2} / message: {3}'.
                                 format(info['lastLine'], info['firstColumn'], info['subType'],
                                        html_parser.unescape(info['message'])))
                self.logger.debug('extract: {0}'.format(info['extract']))


    def should_validate(self, filename):
        """Check if the filename is a type of file that should be validated.
        :param filename: A file name to check against
        """
        for extension in self.validate_extensions:
            if filename.endswith(extension):
                return True
        return False
