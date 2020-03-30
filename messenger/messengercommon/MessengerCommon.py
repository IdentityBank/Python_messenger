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
import sys
import datetime
import hashlib
import string
import codecs
import unicodedata
import collections
import jsonsimpleconfig


################################################################################
# Module                                                                       #
################################################################################

class MessengerCommon:

    @staticmethod
    def getTimestemp(time=True, seconds=False, microseconds=False, utc=False):
        if utc:
            todaydate = datetime.datetime.utcnow()
        else:
            todaydate = datetime.datetime.now()
        timestemp = (str("%04d" % todaydate.year) + "-" +
                     str("%02d" % todaydate.month) + "-" +
                     str("%02d" % todaydate.day))
        if time:
            timestemp += (" " +
                          str("%02d" % todaydate.hour) + ":" +
                          str("%02d" % todaydate.minute))
            if seconds:
                timestemp += ("." + str("%02d" % todaydate.second))
                if microseconds:
                    timestemp += ("." + str("%06d" % todaydate.microsecond))
        return timestemp

    @staticmethod
    def md5sum(filename, seek=0, blocksize=4096):
        hash = hashlib.md5()
        with open(filename, "rb") as file:
            if seek > 0:
                file.seek(seek)
            for block in iter(lambda: file.read(blocksize), b""):
                hash.update(block)
        return hash.hexdigest()

    @staticmethod
    def queryYesNo(question, default="yes"):

        valid = {"yes": True, "y": True, "True": True, "T": True, "t": True, '1': True,
                 "no": False, "n": False, "False": False, "F": False, "f": False, '0': False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes/y/t/1' or 'no/n/f/0'" + os.linesep)

    @staticmethod
    def slugify(value):
        validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        value = codecs.decode(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'), 'ascii')
        return ''.join(str(char) for char in value if str(char) in validFilenameChars)

    @staticmethod
    def str2Bool(value):
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif value.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise TypeError('Boolean value expected.')

    @staticmethod
    def dictionaryMerge(dictionary, mergeDictionary):
        for k, v in mergeDictionary.items():
            if (k in dictionary and isinstance(dictionary[k], dict)
                    and isinstance(mergeDictionary[k], collections.Mapping)):
                MessengerCommon.dictionaryMerge(dictionary[k], mergeDictionary[k])
            else:
                dictionary[k] = mergeDictionary[k]
        return dictionary

    @staticmethod
    def getConfig(jscConfigFilePath: str, connectionName: str) -> dict:
        configuration = jsonsimpleconfig.load(jscConfigFilePath)
        if not configuration:
            raise ValueError("Wrong configuration file!")

        section = '"messenger"."{}"'.format(connectionName)
        if configuration and configuration.getSection(section):
            db = configuration.getSection('"messenger"."server"."db"')
            server = configuration.getSection('"messenger"."server"."bind"')
            serverConnection = '{}."server"."bind"'.format(section)
            serverSection = configuration.getSection(serverConnection)
            if serverSection:
                server = serverSection
            firewall = configuration.getSection('"messenger"."server"."Security"."Firewall"')
            firewallSection = '{}."server"."Security"."Firewall"'.format(section)
            firewallSection = configuration.getSection(firewallSection)
            if firewallSection:
                firewall = firewallSection
            security = configuration.getSection('"messenger"."server"."Security"')
            securitySection = '{}."server"."Security"'.format(section)
            securitySection = configuration.getSection(securitySection)
            if securitySection:
                security = securitySection
            connectionType = (configuration.getValue('"messenger"."{}"'.format(connectionName), 'type'))
            if connectionType == 'clicksend':
                connectionMode = (configuration.getValue('"messenger"."{}"'.format(connectionName), 'mode'))
                sectionConfiguration = '{}."configuration"'.format(section)
                sectionConfigurationEmail = '{}."configuration"."email"'.format(section)
                sectionConnection = '{}."configuration"."connection"'.format(section)
                configuration = \
                    {
                        'connectionType': connectionType,
                        'connectionMode': connectionMode,
                        'url': configuration.getValue(sectionConfiguration, 'url'),
                        'api_user': configuration.getValue(sectionConnection, 'api_user'),
                        'api_key': configuration.getValue(sectionConnection, 'api_key'),
                        'emailId': configuration.getValue(sectionConfigurationEmail, 'id'),
                    }
            elif connectionType == 'db':
                configuration = \
                    {
                        'connectionType': connectionType,
                    }
            elif connectionType == 'slack':
                sectionConfiguration = '{}."configuration"'.format(section)
                sectionConnection = '{}."configuration"."connection"'.format(section)
                sectionConfigurationChannels = '{}."configuration"."channels"'.format(section)
                configuration = \
                    {
                        'connectionType': connectionType,
                        'url': configuration.getValue(sectionConfiguration, 'url'),
                        'token': configuration.getValue(sectionConnection, 'oauth_access_token'),
                        'channels': configuration.getSection(sectionConfigurationChannels),
                    }
            elif connectionType == 'smtp':
                sectionConfigurationServer = '{}."server"'.format(section)
                sectionConfigurationServerHeaders = '{}."server"."custom-headers"'.format(section)
                sectionConfigurationServerAccount = '{}."server"."account"'.format(section)
                sectionConfigurationServerAccountFrom = '{}."server"."account"."from"'.format(section)
                configuration = \
                    {
                        'connectionType': connectionType,
                        'smtpHost': configuration.getValue(sectionConfigurationServer, 'host'),
                        'smtpPort': configuration.getValue(sectionConfigurationServer, 'port'),
                        'smtpTLS': configuration.getValue(sectionConfigurationServer, 'tls', False),
                        'smtpStartTLS': configuration.getValue(sectionConfigurationServer, 'start_tls', False),
                        'smtpUserAgent': configuration.getValue(sectionConfigurationServer, 'user-agent'),
                        'smtpAddressForceFormat': configuration.getValue(sectionConfigurationServer,
                                                                         'address_format_force'),
                        'smtpCustomHeaders': configuration.getSection(sectionConfigurationServerHeaders),
                        'smtpUsername': configuration.getValue(sectionConfigurationServerAccount, 'username'),
                        'smtpPassword': configuration.getValue(sectionConfigurationServerAccount, 'password'),
                        'smtpFromEmail': configuration.getValue(sectionConfigurationServerAccountFrom, 'email'),
                        'smtpFromName': configuration.getValue(sectionConfigurationServerAccountFrom, 'name'),
                    }
            else:
                configuration = None
                print("The messenger connection type '{}' is not supported.".format(connectionType))

            if configuration and db:
                configuration['db'] = db
            if configuration and server:
                configuration['server'] = server
            if configuration and security:
                configuration['Security'] = security
            if configuration and firewall:
                configuration['Firewall'] = firewall
        else:
            configuration = None
            print("Error parsing configuration file for connection name: {}. Execution interrupted ...".format(
                connectionName))

        return configuration

    @staticmethod
    def getClientConfig(jscConfigFilePath: str) -> dict:
        configuration = jsonsimpleconfig.load(jscConfigFilePath)
        if not configuration:
            raise ValueError("Wrong configuration file!")

        section = '"IDBank"."Messenger"'
        if configuration and configuration.getSection(section):
            configuration = configuration.getSection(section)
        else:
            configuration = None
            print("Error parsing configuration file for messenger client. Execution interrupted ...")

        return configuration

################################################################################
#                                End of file                                   #
################################################################################
