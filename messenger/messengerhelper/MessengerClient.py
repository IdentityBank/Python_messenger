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

import json
import logging
import socket

from secureclientserverservice import ScssClientInet, ScssProtocol, ScssSecurityHelper
from messenger import MessengerCommon


################################################################################
# Module                                                                       #
################################################################################

class MessengerClient(ScssClientInet):
    jscConfigFilePath = None

    def __init__(self, jscConfigFilePath: str, requestType: str):
        self.jscConfigFilePath = jscConfigFilePath
        connectionConfiguration = self.__getConnectionConfiguration(requestType)
        super().__init__(connectionConfiguration['host'], connectionConfiguration['port'])

    @staticmethod
    def connect(jscConfigFilePath: str, request: str):

        request = json.loads(request)
        if request and 'type' in request:
            client = MessengerClient(jscConfigFilePath, request['type'])
            if client._connect():
                configuration = MessengerCommon.getClientConfig(jscConfigFilePath)
                if configuration is not None:
                    client.setConfiguration(configuration)
                    client.setConnectionSecurity(ScssSecurityHelper.load(configuration))
                return client
            else:
                return None

    def __getConnectionConfiguration(self, requestType: str):
        host = port = None
        configuration = MessengerCommon.getClientConfig(self.jscConfigFilePath)

        if requestType == 'sms':
            if "smsHost" in configuration: host = configuration["smsHost"]
            if "smsPort" in configuration: port = configuration["smsPort"]
        elif requestType == 'email':
            if "emailHost" in configuration: host = configuration["emailHost"]
            if "emailPort" in configuration: port = configuration["emailPort"]
        elif requestType == 'communicator':
            if "slackHost" in configuration: host = configuration["slackHost"]
            if "slackPort" in configuration: port = configuration["slackPort"]

        return {'host': host, 'port': port}

    def execute(self, request: str):
        return super().send(request)

    def sendNone(self, data):
        receivedString = None
        try:
            logging.debug("Send [None] data.")
            ScssProtocol.sendNoneData(self.clientSocket, data)
            logging.debug("Data sent.")
            receivedString = ScssProtocol.receiveNoneData(self.clientSocket, self.max_buffer_size)
            logging.debug("Data received.")
            logging.debug("Data [{}]".format(receivedString))
        except socket.timeout:
            logging.debug("Connection timeout.")

        return receivedString

    def sendToken(self, data):
        receivedString = None
        try:
            if ScssProtocol.sendTokenData(self.clientSocket, self.connectionSecurity, data):
                receivedString = ScssProtocol.receiveTokenData(self.clientSocket, self.connectionSecurity,
                                                               self.max_buffer_size)
        except socket.timeout:
            logging.debug("Connection timeout.")

        return receivedString

    def sendCertificate(self, data):
        logging.warning('CERTIFICATE access not implemented yet!')
        return None

################################################################################
#                                End of file                                   #
################################################################################
