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
import email

from .MessagesModel import MessagesModel


################################################################################
# Class                                                                        #
################################################################################

class Email(MessagesModel):
    emailFrom = None
    emailToEmail = None
    emailTo = None
    emailCc = None
    emailBcc = None
    emailSubject = None
    emailBody = None
    emailSchedule = None

    def __init__(self, data):
        if 'rawSmtp' in data and data['rawSmtp']:
            self.__initFromSmtpRaw(data['rawSmtp'])
        else:
            emailData = {}
            emailData['emailFrom'] = data['from'] if 'from' in data else 'messenger'
            emailData['emailToEmail'] = data['to'][0]['email'] if 'to' in data and isinstance(data['to'], list) and len(data['to']) > 0 and 'email' in data['to'][0] else None
            emailData['emailTo'] = data['to'] if 'to' in data else None
            emailData['emailCc'] = data['cc'] if 'cc' in data else None
            emailData['emailBcc'] = data['bcc'] if 'bcc' in data else None
            emailData['emailSubject'] = data['subject'] if 'subject' in data else None
            emailData['emailBody'] = data['body'] if 'body' in data else None
            emailData['emailSchedule'] = data['schedule'] if 'schedule' in data else None
            self.__initFromAttributes(**emailData)

    def __initFromAttributes(self, emailFrom, emailToEmail, emailTo, emailCc, emailBcc, emailSubject, emailBody, emailSchedule):
        self.emailFrom = emailFrom
        self.emailToEmail = emailToEmail
        self.emailTo = emailTo
        self.emailCc = emailCc
        self.emailBcc = emailBcc
        self.emailSubject = emailSubject
        self.emailBody = emailBody
        self.emailSchedule = emailSchedule
        self.toModel()

    def __initFromSmtpRaw(self, smtpRaw):
        msg = email.message_from_string(smtpRaw)
        self.emailTo = msg.get('to')
        if self.emailTo:
            self.emailTo = str(self.emailTo).split(',')
            if len(self.emailTo) > 0:
                self.emailTo = self.emailTo[0]

        self.emailToEmail = self.emailTo
        self.emailFrom = msg.get('from')
        self.emailTo = msg.get('to')
        self.emailCc = msg.get('cc')
        self.emailBcc = msg.get('bcc')
        self.emailSubject = msg.get('subject')
        self.emailBody = {'smtpRaw': smtpRaw}
        self.toModel()

    def toModel(self):
        self.dbSchedule = self.emailSchedule
        self.dbTag = None
        self.dbType = 'email'
        self.dbStatus = 'messenger'
        self.dbFrom = self.emailFrom
        self.dbTo = self.emailToEmail
        self.dbAttributes = json.dumps({'to': self.emailTo, 'cc': self.emailCc, 'bcc': self.emailBcc})
        self.dbData = json.dumps({'subject': self.emailSubject, 'body': self.emailBody})

################################################################################
#                                End of file                                   #
################################################################################
