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

import smtplib
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address
from email.parser import HeaderParser

from .MessengerGateBase import MessengerGateBase


################################################################################
# Module                                                                       #
################################################################################

class EmailSmtp(MessengerGateBase):

    def __init__(self, configuration: dict):
        MessengerGateBase.__init__(self, configuration)

    def __addRecipients(self, recipients):
        returnRecipients = []
        if recipients:
            for recipient in recipients:
                email = ''
                if 'email' in recipient:
                    email = recipient['email']
                if 'name' in recipient:
                    name = recipient['name']
                else:
                    name = email
                address = Address(name, email).__str__()
                if 'smtpAddressForceFormat' in self.configuration and self.configuration['smtpAddressForceFormat'] is True:
                    address = address.replace('<"', '<').replace('">', '>').strip()
                returnRecipients.append(address)
        return ', '.join(returnRecipients)

    def email(self, data):
        if 'rawSmtp' in data and data['rawSmtp']:
            return self.__emailRawSmtp(data)
        else:
            return self.__emailData(data)

    def __emailRawSmtp(self, data):
        msg = HeaderParser().parsestr(data["rawSmtp"])
        emailFrom = msg.get('from')
        emailTo = msg.get_all('to')
        if not emailTo: emailTo = []
        emailCc = msg.get_all('cc')
        if not emailCc: emailCc = []
        emailBcc = msg.get_all('bcc')
        if not emailBcc: emailBcc = []
        msg = data["rawSmtp"].encode("utf8")
        return self.__sendSmtp(msg, emailFrom, emailTo + emailCc + emailBcc)

    def __emailData(self, data):
        emailSubject = data["subject"]
        emailBody = data["body"]

        # prepare message
        msg = MIMEMultipart('alternative')
        if "to" in data:
            msg['To'] = self.__addRecipients(data["to"])
        if "cc" in data:
            msg['Cc'] = self.__addRecipients(data["cc"])
        if "bcc" in data:
            msg['Bcc'] = self.__addRecipients(data["bcc"])

        smtpFromName = self.configuration["smtpFromName"]
        smtpFromEmail = self.configuration["smtpFromEmail"]
        if 'from' in data:
            if 'email' in data['from']:
                smtpFromEmail = data['from']['email']
            if 'name' in data['from']:
                smtpFromName = data['from']['name']
            else:
                smtpFromName = smtpFromEmail
        smtpFrom = Address(smtpFromName, smtpFromEmail).__str__().strip()
        if 'smtpAddressForceFormat' in self.configuration and self.configuration['smtpAddressForceFormat'] is True:
            smtpFrom = smtpFrom.replace('<"', '<').replace('">', '>').strip()
        if smtpFrom.endswith('<>'):
            smtpFrom = smtpFrom.rstrip('<>').strip()
        msg['From'] = smtpFrom
        msg['Subject'] = emailSubject

        smtpCustomHeaders = {}

        if 'smtpCustomHeaders' in self.configuration and self.configuration['smtpCustomHeaders'] and isinstance(self.configuration['smtpCustomHeaders'], dict):
            for headerKey in self.configuration['smtpCustomHeaders']:
                if headerKey and headerKey.strip() and headerKey.strip() in self.configuration['smtpCustomHeaders']:
                    headerValue = self.configuration['smtpCustomHeaders'][headerKey]
                    if headerValue and headerValue.strip():
                        smtpCustomHeaders[headerKey] = headerValue

        if 'replyTo' in data:
            smtpCustomHeaders['Reply-To'] = data['replyTo']
        if 'returnPath' in data:
            smtpCustomHeaders['Return-Path'] = data['returnPath']
        elif 'replyTo' in data:
            smtpCustomHeaders['Return-Path'] = data['replyTo']

        if 'userAgent' in data and data['userAgent'] and data['userAgent'].strip():
            smtpCustomHeaders['User-Agent'] = data['userAgent']
        elif 'smtpUserAgent' in self.configuration and self.configuration['smtpUserAgent'] and self.configuration['smtpUserAgent'].strip():
            smtpCustomHeaders['User-Agent'] = self.configuration['smtpUserAgent']

        if 'customHeaders' in data and data['customHeaders'] and isinstance(data['customHeaders'], dict):
            for headerKey in data['customHeaders']:
                if headerKey and headerKey.strip() and headerKey.strip() in data['customHeaders']:
                    headerValue = data['customHeaders'][headerKey]
                    if headerValue and headerValue.strip():
                        smtpCustomHeaders[headerKey] = headerValue

        for smtpCustomHeaderKey, smtpCustomHeaderValue in smtpCustomHeaders.items():
            msg.add_header(smtpCustomHeaderKey, smtpCustomHeaderValue)

        if 'plain' in emailBody or 'html' in emailBody:
            if 'plain' in emailBody:
                plain = MIMEText(emailBody['plain'], 'plain')
                msg.attach(plain)
            if 'html' in emailBody:
                html = MIMEText(emailBody['html'], 'html')
                msg.attach(html)
        elif 'boundary' in emailBody and 'payload' in emailBody:
            msg.set_boundary(emailBody['boundary'])
            msg.set_payload(emailBody['payload'])
        else:
            plain = MIMEText(emailBody, 'plain')
            msg.attach(plain)

        return self.__sendSmtp(msg)

    def __sendSmtp(self, msg, fromAddress = None, toAddress = None):
        # send message
        if self.configuration["smtpTLS"]:
            server = smtplib.SMTP_SSL(self.configuration["smtpHost"], self.configuration["smtpPort"])
        else:
            server = smtplib.SMTP(self.configuration["smtpHost"], self.configuration["smtpPort"])
        server.set_debuglevel(logging.getLogger().getEffectiveLevel() == logging.DEBUG)
        server.ehlo()
        if self.configuration["smtpStartTLS"]:
            server.starttls()
            server.ehlo()
        server.login(self.configuration["smtpUsername"], self.configuration["smtpPassword"])
        if fromAddress is None or toAddress is None:
            server.send_message(msg)
        else:
            server.sendmail(fromAddress, toAddress, msg)
        server.quit()

        return True

################################################################################
#                                End of file                                   #
################################################################################
