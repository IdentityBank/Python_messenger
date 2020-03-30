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

class Sms(MessagesModel):
    smsFrom = None
    smsTo = None
    smsBody = None
    smsSchedule = None

    def __init__(self, data):
        smsData = {}
        smsData['smsFrom'] = data['from'] if 'from' in data else 'messenger'
        smsData['smsTo'] = data['to'] if 'to' in data else None
        smsData['smsBody'] = data['body'] if 'body' in data else None
        smsData['smsSchedule'] = data['schedule'] if 'schedule' in data else None
        self.__initFromAttributes(**smsData)

    def __initFromAttributes(self, smsFrom, smsTo, smsBody, smsSchedule):
        self.smsFrom = smsFrom
        self.smsTo = smsTo
        self.smsBody = smsBody
        self.smsSchedule = smsSchedule
        self.toModel()

    def toModel(self):
        self.dbSchedule = self.smsSchedule
        self.dbTag = None
        self.dbType = 'sms'
        self.dbStatus = 'messenger'
        self.dbFrom = self.smsFrom
        self.dbTo = self.smsTo
        self.dbAttributes = None
        self.dbData = json.dumps({'body': self.smsBody})

################################################################################
#                                End of file                                   #
################################################################################
