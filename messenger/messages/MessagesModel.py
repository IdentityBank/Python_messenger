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

from psycopg2 import sql
from abc import abstractmethod


################################################################################
# Class                                                                        #
################################################################################

class MessagesModel:
    dbTableName = 'messenger.messages'

    dbId = None
    dbCreatetime = None
    dbSchedule = None
    dbTag = None
    dbType = None
    dbStatus = None
    dbFrom = None
    dbTo = None
    dbAttributes = None
    dbData = None

    def __init__(self,
                 dbId,
                 dbCreatetime,
                 dbSchedule,
                 dbTag,
                 dbType,
                 dbStatus,
                 dbFrom,
                 dbTo,
                 dbAttributes,
                 dbData):
        self.dbId = dbId
        self.dbCreatetime = dbCreatetime
        self.dbSchedule = dbSchedule
        self.dbTag = dbTag
        self.dbType = dbType
        self.dbStatus = dbStatus
        self.dbFrom = dbFrom
        self.dbTo = dbTo
        self.dbAttributes = dbAttributes
        self.dbData = dbData

    @abstractmethod
    def toModel(self):
        raise NotImplementedError("MessagesModel::toModel - Not implemented yet...")

    def toQuerySave(self):
        queryAttributes = {
            'type': self.dbType,
            'status': self.dbStatus,
            'from': self.dbFrom,
            'to': self.dbTo,
        }
        if self.dbSchedule: queryAttributes['schedule'] = self.dbSchedule
        if self.dbTag: queryAttributes['tag'] = self.dbTag
        if self.dbAttributes: queryAttributes['attributes'] = self.dbAttributes
        if self.dbData: queryAttributes['data'] = self.dbData

        query = sql.SQL("INSERT INTO %s ({}) VALUES ({}) RETURNING id;" % self.dbTableName).format(
            sql.SQL(",").join(map(sql.Identifier, queryAttributes)),
            sql.SQL(",").join(map(sql.Placeholder, queryAttributes))
        )
        return {'query': query, 'queryAttributes': queryAttributes}

################################################################################
#                                End of file                                   #
################################################################################
