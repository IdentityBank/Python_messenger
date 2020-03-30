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

import base64
import json
import logging
import urllib.parse
import urllib.request

from psutil.tests import retry

from .MessengerGateBase import MessengerGateBase


################################################################################
# Module                                                                       #
################################################################################

class Clicksend(MessengerGateBase):
    req = None
    timeout = 300

    def __init__(self, configuration: dict):
        MessengerGateBase.__init__(self, configuration)

    def sms(self, data):
        action = "sms/price"
        if self.configuration["connectionMode"] == "send":
            action = "sms/send"
        url = self.configuration["url"] + action
        smsFrom = "IDB"
        if "from" in data:
            smsFrom = data["from"]
        smsTo = data["to"]
        smsBody = data["body"]
        smsId = "Messenger Gateway"
        body = \
            {
                "messages":
                    [
                        {
                            "source": "php",
                            "from": smsFrom,
                            "body": smsBody,
                            "to": smsTo,
                            "custom_string": smsId
                        }
                    ]
            }
        self.__setup(url, body)
        return self.__execute()

    def email(self, data):
        action = "email/price"
        if self.configuration["connectionMode"] == "send":
            action = "email/send"
        url = self.configuration["url"] + action
        emailTo = data["to"]
        emailFromName = "Identity Bank"
        emailFromId = self.configuration["emailId"]
        emailSubject = data["subject"]
        emailBody = data["body"]
        emailHeaders = {}

        if 'plain' in emailBody or 'html' in emailBody:
            if 'plain' in emailBody:
                plain = emailBody['plain']
                emailBody = plain
            if 'html' in emailBody:
                html = emailBody['html']
                emailBody = html
        elif 'boundary' in emailBody and 'payload' in emailBody:
            emailHeaders['boundary'] = emailBody['boundary']
            emailBody = emailBody['payload']

        if isinstance(emailBody, dict) or isinstance(emailBody, list):
            emailBody = json.dumps(emailBody)

        body = \
            {
                "to": emailTo,
                "from": {
                    "email_address_id": emailFromId,
                    "name": emailFromName
                },
                "subject": emailSubject,
                "body": emailBody
            }

        if "bcc" in data:
            body["bcc"] = data["bcc"]
        if "cc" in data:
            body["cc"] = data["cc"]
        if "boundary" in emailHeaders:
            body["boundary"] = emailHeaders["boundary"]

        self.__setup(url, body, emailHeaders)
        return self.__execute()

    def __setup(self, url, body, headers=None):
        body = json.dumps(body).encode("ASCII")
        self.req = urllib.request.Request(url, body)
        base64string = base64.b64encode(
            ("{}:{}".format(
                self.configuration["api_user"],
                self.configuration["api_key"])).encode("ASCII")).decode("ASCII")
        self.req.add_header("Authorization", "Basic {}".format(base64string))
        self.req.add_header("Content-Type", "application/json")
        if headers:
            for key, value in headers.items():
                self.req.add_header(key, value)

    def __execute(self):
        with self.__urlOpenWithRetry() as response:
            jsonResponse = response.read()
            returnValue = jsonResponse.decode("ASCII")

            if not returnValue or returnValue == '':
                logging.error("Cannot connect with Clicksend server [{}] ...".format(self.req.get_full_url()))
                returnValue = ""
            else:
                logging.info("Return: {} ...".format(returnValue))

        return returnValue

    @retry(urllib.error.URLError, interval=5, retries=3)
    def __urlOpenWithRetry(self):
        return urllib.request.urlopen(self.req, timeout=self.timeout)

################################################################################
#                                End of file                                   #
################################################################################
