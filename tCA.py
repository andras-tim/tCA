#!/usr/bin/env python

"""%prog can generate index.days file from several sources. Input can be one or more logspace directories and one
or more index.days files."""
__author__ = 'Andras TIM <andras.tim@gmail.com>'
__version__ = '0.0.1'
__epilog__ = """
Info:
  Do not use currently opened index.days file as output, because it can break
  the process.
  Multiple sources merge holds order of parameters by types. Logspace folders
  merge first and then index.days files.

"""

import os
import sys
from optparse import OptionParser


class OptionParserWithMultilineEpilog(OptionParser):
    # Hold new line characters
    def format_epilog(self, formatter):
        return self.epilog


class Options(object):
    source_logspace_directories = []
    source_indexdays_files = []
    destination_logspace_id = ""
    destination_file = ""
    verbose = False

    def parse_and_check_parameters(self):
        opts = self.__parse()

        if opts.logspace_dirs:
            for logspace_dir in opts.logspace_dirs:
                if not os.path.isdir(logspace_dir):
                    sys.stderr.write("Logspace directory is not exist: %s\n" % logspace_dir)
                    sys.exit(1)
                self.source_logspace_directories.append(os.path.abspath(logspace_dir))

        if opts.indexdays_files:
            for indexdays_file in opts.indexdays_files:
                if not os.path.isfile(indexdays_file):
                    sys.stderr.write("Index.days file is not exist: %s\n" % indexdays_file)
                    sys.exit(1)
                self.source_indexdays_files.append(os.path.abspath(indexdays_file))

        if not len(opts.logspace_id) <= 23:
            sys.stderr.write("Logspace ID is not valid!\n")
            sys.exit(1)
        self.destination_logspace_id = opts.logspace_id

        output_file_abspath = os.path.abspath(opts.output_file)
        output_directory_path = os.path.dirname(output_file_abspath)
        if not os.path.isdir(output_directory_path):
            sys.stderr.write("Directory of output file is not found: %s\n" % output_directory_path)
            sys.exit(1)
        self.destination_file = output_file_abspath

        self.verbose = (opts.verbose is not None)

        return self

    @classmethod
    def __parse(cls):
        app_name = os.path.basename(sys.argv[0])
        parser = OptionParserWithMultilineEpilog(usage='Usage: %s [options] OUTPUT_FILE' % app_name,
                                                 version='%s: %s' % (app_name, __version__),
                                                 description=__doc__,
                                                 epilog=__epilog__,
                                                 prog=app_name,
                                                 )
        parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                          help='Print verbose messages')
        parser.add_option('-l', '--in-logspace',
                          type="string", dest='logspace_dirs', action='append',
                          help='Use specified logspace directory as source')
        parser.add_option('-i', '--in', type="string", dest='indexdays_files', action='append',
                          help='Use specified index.days file as source')
        parser.add_option('-I', '--id', type="string", dest='logspace_id', action='store',
                          help='ID of destination logspace')
        (opts, args) = parser.parse_args()

        if opts.logspace_dirs is None and opts.indexdays_files is None:
            parser.error("Source was not specified! Must be at least one.\n\n")

        if opts.logspace_id is None:
            parser.error("Logspace ID was not specified!\n\n")

        if len(args) == 0:
            parser.error("Output file was not specified!\n\n")
        elif len(args) > 1:
            parser.error("One or more unknown parameters was present: %s\n\n" % args[1:])
        opts.output_file = args[0]

        return opts


def main():
    global options

    options = Options().parse_and_check_parameters()


if __name__ == "__main__":
    main()
