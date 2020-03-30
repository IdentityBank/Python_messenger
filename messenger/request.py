#! /bin/sh
# -*- coding: utf-8 -*-
""":"
exec python3 $0 ${1+"$@"}
"""
# * ********************************************************************* *
# *                                                                       *
# *   Tools to provide messages to clients                                *
# *   This file is part of messenger. This project may be found at:       *
# *   https://github.com/IdentityBank/Python_messenger.                   *
# *                                                                       *
# *   Copyright (C) 2020 by Identity Bank. All Rights Reserved.           *
# *   https://www.identitybank.eu - You belong to you                     *
# *                                                                       *
# *   This program is free software: you can redistribute it and/or       *
# *   modify it under the terms of the GNU Affero General Public          *
# *   License as published by the Free Software Foundation, either        *
# *   version 3 of the License, or (at your option) any later version.    *
# *                                                                       *
# *   This program is distributed in the hope that it will be useful,     *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of      *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the        *
# *   GNU Affero General Public License for more details.                 *
# *                                                                       *
# *   You should have received a copy of the GNU Affero General Public    *
# *   License along with this program. If not, see                        *
# *   https://www.gnu.org/licenses/.                                      *
# *                                                                       *
# * ********************************************************************* *

################################################################################
# Import(s)                                                                    #
################################################################################

import sys
import signal
import argparse
import logging
import re

from messenger import ProcessRequest

################################################################################
# Module Variable(s)                                                           #
################################################################################

versionString = "0.0.1"
applicationNameString = "messengerrequest"
applicationDescriptionString = "Messenger request client - command line interface for messenger"


################################################################################
# Module                                                                       #
################################################################################

def parameters():
    parser = argparse.ArgumentParser(description=applicationDescriptionString)
    parser.add_argument('-v', '--version', action='version',
                        version=applicationNameString + " - " + versionString + " - " + applicationDescriptionString)
    parser.add_argument('-i', '--jscConfigFilePath', type=argparse.FileType('r'), help='Path to config file.',
                        required=True)
    parser.add_argument('-n', '--connectionName', help='Connection name.', required=True)
    parser.add_argument('-r', '--request', help='Request data.', required=True)

    loggingLeveChoices = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }
    parser.add_argument('-ll', '--logging_level', dest="loggingLevel", choices=loggingLeveChoices.keys(),
                        help='Output log level', required=False)
    args, leftovers = parser.parse_known_args()

    if vars(args)['loggingLevel'] is None:
        level = logging.CRITICAL
    else:
        level = loggingLeveChoices.get(vars(args)['loggingLevel'], logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s][%(levelname)-8s] [%(module)-20s] - %(message)s', datefmt='%Y.%m.%d %H:%M.%S', level=level)

    return vars(args)


def main(argv=sys.argv):
    signal.signal(signal.SIGINT, handler)
    args = parameters()
    logging.info('* Arguments:')
    for key, value in args.items():
        logging.info('** [{}]: [{}]'.format(' '.join(
            ''.join([w[0].upper(), w[1:].lower()]) for w in (re.sub("([a-z])([A-Z])", "\g<1> \g<2>", key)).split()),
            value))

    if args['request']:
        args['request'] = args['request'].strip('"').strip("'")

    print("Processing requests: {}".format(args['request']))
    print("Wait...")

    if args['loggingLevel'] == 'DEBUG':
        print(ProcessRequest.execute(args['jscConfigFilePath'].name, args['connectionName'], args['request']))
    else:
        try:
            print(ProcessRequest.execute(args['jscConfigFilePath'].name, args['connectionName'], args['request']))
        except:
            print('Error!')

    print("Done.")


def handler(signum, frame):
    sys.exit()


# Execute main function
if __name__ == '__main__':
    main()
    sys.exit()

################################################################################
#                                End of file                                   #
################################################################################
