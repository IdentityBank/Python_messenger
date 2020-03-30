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

from abc import abstractmethod
from messenger import MessagesStorage


################################################################################
# Module                                                                       #
################################################################################

class MessengerGateBase:
    configuration = None

    def __init__(self, configuration):
        self.configuration = configuration

    def execute(self, request: str):
        try:
            request = json.loads(request)
        except json.decoder.JSONDecodeError as error:
            logging.error('Error decoding request data: ' + str(error))
            request = None

        try:
            if isinstance(request, dict) and 'type' in request:
                if self.configuration and 'db' in self.configuration and self.configuration['db']:
                    itemId = self.store(request)
                    if itemId:
                        logging.debug("Stored as: Item ID: [{}]".format(itemId))
                    else:
                        logging.error("Cannot store to DB : {} ...".format(request))
                logging.info("Execute: {} ...".format(request['type']))

                if request['type'] == 'sms' and 'smsData' in request:
                    return self.sms(request['smsData'])
                elif request['type'] == 'email' and 'emailData' in request:
                    return self.email(request['emailData'])
                elif request['type'] == 'communicator' and 'messageData' in request:
                    return self.communicator(request['messageData'])

        except Exception as e:
            logging.critical('Request error: ' + str(e))

        return None

    def store(self, request):
        return MessagesStorage(self.configuration).store(request)

    @abstractmethod
    def sms(self, data):
        raise NotImplementedError("SMS - Not implemented yet...")

    @abstractmethod
    def email(self, data):
        raise NotImplementedError("Email - Not implemented yet...")

    @abstractmethod
    def communicator(self, data):
        raise NotImplementedError("Communicator - Not implemented yet...")

################################################################################
#                                End of file                                   #
################################################################################
