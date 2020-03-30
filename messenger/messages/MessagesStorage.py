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
import psycopg2
import logging

from .Sms import Sms
from .Email import Email
from .Communicator import Communicator


################################################################################
# Class                                                                        #
################################################################################

class MessagesStorage:
    configuration = None

    def __init__(self, configuration):
        self.configuration = configuration

    def store(self, request):

        model = None
        if request['type'] == 'sms' and 'smsData' in request:
            model = Sms(request['smsData'])
        elif request['type'] == 'email' and 'emailData' in request:
            model = Email(request['emailData'])
        elif request['type'] == 'communicator' and 'messageData' in request:
            model = Communicator(request['messageData'])

        if model:
            if self.configuration:
                attributes = model.dbAttributes
                if attributes is None:
                    attributes = {}
                else:
                    attributes = json.loads(attributes)
                if isinstance(attributes, dict):
                    attributes['connectionType'] = self.configuration['connectionType']
                    model.dbAttributes = json.dumps(attributes)
            return self.__dbStore(model.toQuerySave())

    def __dbStore(self, query):
        itemId = None
        dbConnection = None
        if 'db' in self.configuration:
            db = self.configuration['db']
            if db:
                try:
                    dbConnection = psycopg2.connect(host=db['dbHost'],
                                                    port=db['dbPort'],
                                                    database=db['dbName'],
                                                    user=db['dbUser'],
                                                    password=db['dbPassword'])
                    dbCursor = dbConnection.cursor()
                    dbCursor.execute(query['query'], query['queryAttributes'])
                    dbConnection.commit()
                    dbRespond = dbCursor.fetchone()
                    if isinstance(dbRespond, tuple) and len(dbRespond) == 1:
                        itemId = dbRespond[0]
                    logging.debug('DB Respond: ' + str(dbRespond))
                    dbCursor.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    logging.error(error)
                finally:
                    if dbConnection is not None:
                        dbConnection.close()
        return itemId

################################################################################
#                                End of file                                   #
################################################################################
