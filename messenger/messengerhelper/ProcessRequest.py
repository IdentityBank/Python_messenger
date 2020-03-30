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

import logging
import json

from .MessengerClient import MessengerClient
from messenger import MessengerCommon, Clicksend, Database, Slack, EmailSmtp


################################################################################
# Module                                                                       #
################################################################################

class ProcessRequest:

    @staticmethod
    def executeFromFile(jscConfigFilePath: str,
                        connectionName: str,
                        inputRequestFilePath: str):

        if logging.getLevelName(logging.getLogger().getEffectiveLevel()) == 'DEBUG':

            with open(inputRequestFilePath, 'r') as requestFile:
                request = requestFile.read()
                return ProcessRequest.execute(jscConfigFilePath,
                                              connectionName,
                                              request)
        else:

            try:
                with open(inputRequestFilePath, 'r') as requestFile:
                    request = requestFile.read()
                    return ProcessRequest.execute(jscConfigFilePath,
                                                  connectionName,
                                                  request)
            except:
                logging.error("There is problem with your request. Check it and try again.")

        return None

    @staticmethod
    def execute(jscConfigFilePath: str,
                connectionName: str,
                request: str):

        if connectionName:
            connectionName = connectionName.strip('"').strip("'")

            if request:
                requestJsonData = json.loads(request)
                if isinstance(requestJsonData, dict):
                    return ProcessRequest.__executeRequest(jscConfigFilePath,
                                                           connectionName,
                                                           request)
                else:
                    returnValue = []
                    for request in requestJsonData:
                        returnValue.append(ProcessRequest.__executeRequest(jscConfigFilePath,
                                                                           connectionName,
                                                                           json.dumps(request)))
                    return returnValue

        return None

    @staticmethod
    def __executeRequest(jscConfigFilePath: str,
                         connectionName: str,
                         request: str):

        configuration = MessengerCommon.getConfig(jscConfigFilePath, connectionName)
        if configuration and 'connectionType' in configuration:
            if configuration['connectionType'] == 'clicksend':
                return Clicksend(configuration).execute(request)
            elif configuration['connectionType'] == 'db':
                return Database(configuration).execute(request)
            elif configuration['connectionType'] == 'slack':
                return Slack(configuration).execute(request)
            elif configuration['connectionType'] == 'smtp':
                return EmailSmtp(configuration).execute(request)

    @staticmethod
    def executeClient(jscConfigFilePath: str,
                      request: str):

        if request:
            requestJsonData = json.loads(request)
            if isinstance(requestJsonData, dict):
                return ProcessRequest.__executeClientRequest(jscConfigFilePath,
                                                             request)
            else:
                returnValue = []
                for request in requestJsonData:
                    returnValue.append(ProcessRequest.__executeClientRequest(jscConfigFilePath,
                                                                             json.dumps(request)))
                return returnValue

        return None

    @staticmethod
    def __executeClientRequest(jscConfigFilePath: str,
                               request: str):

        client = MessengerClient.connect(jscConfigFilePath, request)
        if client is not None:
            respond = client.execute(request)
            return respond

        return None

################################################################################
#                                End of file                                   #
################################################################################
