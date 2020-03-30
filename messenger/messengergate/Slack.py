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
import urllib.parse
import urllib.request

from .MessengerGateBase import MessengerGateBase


################################################################################
# Module                                                                       #
################################################################################

class Slack(MessengerGateBase):
    req = None
    timeout = 300

    def __init__(self, configuration: dict):
        MessengerGateBase.__init__(self, configuration)

    def communicator(self, data):
        data['messageFrom'] = data['from'] if 'from' in data else 'Slack'
        return self.__message(data)

    def __message(self, data):
        channels = self.configuration["channels"] if "channels" in self.configuration else {}
        channel = channels[data['to']] if 'to' in data and data['to'] in channels else None
        if channel:
            body = {"text": data['body']}
            return self.__directMessage(channel, body)
        else:
            logging.error("Channel: [{}] is not defined. Trying post message ...".format(data['to']))
            action = "chat.postMessage"
            url = '{}{}'.format(self.configuration["url"], action)
            token = self.configuration['token']
            body = {
                "text": data['body'],
                "channel": data['to'],
            }
            return self.__postMessage(url, token, body)

    def __directMessage(self, url, body):
        body = json.dumps(body).encode("ASCII")
        self.req = urllib.request.Request(url, body)
        self.req.add_header("Content-Type", "application/json")
        return self.__execute()

    def __postMessage(self, url, token, body):
        body = json.dumps(body).encode("ASCII")
        self.req = urllib.request.Request(url, body)
        self.req.add_header("Content-Type", "application/json")
        self.req.add_header("Authorization", "Bearer {}".format(token))
        return self.__execute()

    def __execute(self):
        returnValue = ""
        with urllib.request.urlopen(self.req, timeout=self.timeout) as response:
            jsonResponse = response.read()
            returnValue = jsonResponse.decode("ASCII")
            logging.info("Return: {} ...".format(returnValue))
        return returnValue

################################################################################
#                                End of file                                   #
################################################################################
