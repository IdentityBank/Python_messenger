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

from .MessagesModel import MessagesModel


################################################################################
# Class                                                                        #
################################################################################

class Communicator(MessagesModel):
    messageFrom = None
    messageTo = None
    messageBody = None
    messageSchedule = None

    def __init__(self, data):
        messageData = {}
        messageData['messageFrom'] = data['from'] if 'from' in data else 'messenger'
        messageData['messageTo'] = data['to'] if 'to' in data else None
        messageData['messageBody'] = data['body'] if 'body' in data else None
        messageData['messageSchedule'] = data['schedule'] if 'schedule' in data else None
        self.__initFromAttributes(**messageData)

    def __initFromAttributes(self, messageFrom, messageTo, messageBody, messageSchedule):
        self.messageFrom = messageFrom
        self.messageTo = messageTo
        self.messageBody = messageBody
        self.messageSchedule = messageSchedule
        self.toModel()

    def toModel(self):
        self.dbSchedule = self.messageSchedule
        self.dbTag = None
        self.dbType = 'communicator'
        self.dbStatus = 'messenger'
        self.dbFrom = self.messageFrom
        self.dbTo = self.messageTo
        self.dbAttributes = None
        self.dbData = json.dumps({'body': self.messageBody})

################################################################################
#                                End of file                                   #
################################################################################
