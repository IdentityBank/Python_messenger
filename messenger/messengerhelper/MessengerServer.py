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

import logging

from .ProcessRequest import ProcessRequest
from secureclientserverservice import ScssServerInet, ScssSecurityHelper, ScssSecurityFirewall, ScssProtocol
from messenger import MessengerCommon


################################################################################
# Module                                                                       #
################################################################################

class MessengerServer(ScssServerInet):
    jscConfigFilePath = None
    connectionName = None

    def __init__(self, jscConfigFilePath: str, connectionName: str):
        self.jscConfigFilePath = jscConfigFilePath
        self.connectionName = connectionName
        configuration = MessengerCommon.getConfig(jscConfigFilePath, connectionName)
        host = configuration["server"]["host"] if "server" in configuration and "host" in configuration["server"] else ""
        port = configuration["server"]["port"] if "server" in configuration and "port" in configuration["server"] else 57
        self.setConfiguration(configuration["server"])
        self.setConnectionFirewall(ScssSecurityFirewall.load(configuration))
        self.setConnectionSecurity(ScssSecurityHelper.load(configuration))
        super().__init__(host, port)

    def clientActionNone(self, connection, ip, port):
        try:
            messengerRequest = ScssProtocol.receiveNoneData(connection, self.max_buffer_size)
            messengerRespond = ProcessRequest.execute(self.jscConfigFilePath, self.connectionName, messengerRequest)
            if not messengerRespond:
                messengerRespond = ''
            else:
                messengerRespond = str(messengerRespond)
            ScssProtocol.sendNoneData(connection, messengerRespond)
        except:
            pass
        finally:
            connection.close()
            logging.info('Connection ' + ip + ':' + port + " ended")

    def clientActionToken(self, connection, ip, port):
        try:
            messengerRequest = ScssProtocol.receiveTokenData(connection, self.connectionSecurity, self.max_buffer_size)
            messengerRespond = ProcessRequest.execute(self.jscConfigFilePath, self.connectionName, messengerRequest)
            if not messengerRespond:
                messengerRespond = ''
            else:
                messengerRespond = str(messengerRespond)
            ScssProtocol.sendTokenData(connection, self.connectionSecurity, messengerRespond)
        except:
            pass
        finally:
            connection.close()
            logging.info('Connection ' + ip + ':' + port + " ended")

################################################################################
#                                End of file                                   #
################################################################################
