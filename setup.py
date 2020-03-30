# -*- coding: utf-8 -*-
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

import os

from setuptools import setup

################################################################################
# Module                                                                       #
################################################################################

description = 'Messenger - tools to deliver messages to clients via different channels.'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


def parse_requirements_internal(filename):
    """ load requirements from a pip requirements file """
    line_iterator = (line.strip() for line in open(filename))
    return [line for line in line_iterator if line and not line.startswith("#")]


try:
    long_description = read('README.md')
except IOError:
    long_description = description

setup(
    name='messenger',
    version='0.1',
    description=description,
    long_description=long_description,
    keywords="binary secure messenger deliver message channel encryption decryption share tools",
    author='Marcin Zelek',
    author_email='marcin.zelek@identitybank.eu',
    license='GNU Affero General Public License v3.0',
    url='https://www.identitybank.eu',
    packages=['messenger',
              'messenger.messages',
              'messenger.messengercommon',
              'messenger.messengergate',
              'messenger.messengerhelper'],
    python_requires='>=3',
    entry_points=
    {
        'console_scripts':
        [
            'messengerclient = messenger.client:main',
            'messengerserver = messenger.server:main',
            'messengerrequest = messenger.request:main',
            'messengerrequestfile = messenger.requestfile:main',
        ],
    },
    zip_safe=False
)

################################################################################
#                                End of file                                   #
################################################################################
