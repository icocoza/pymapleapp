from datetime import datetime, timedelta

from services.actions.admin.AdminToken import AdminToken
from services.constant.AllError import AllError
from services.constant.MapleEnum import EAdminAppStatus

from repository.db.admin.AdminAppRepository import AdminAppRepository
from module.db.MultiDbHelper import MultiDbHelper

import common.config.appconfig as appconfig
import common.utils.CryptoHelper as CryptoHelper
class AppToken(AdminToken):

    def __init__(self):
        super().__init__()
        self.adminAppRepository = AdminAppRepository()

    def checkScode(self, scode):
        app = self.adminAppRepository.getAppByScode(scode)
        if app == None:
            return AllError.NoServiceCode
        if EAdminAppStatus[app['status']] != EAdminAppStatus.ready:
            return AllError.NotAvailableServiceCode
            #def addMySql(self, scode, host, port, user, passwd, dbname, cbAndEvt):
        if MultiDbHelper.instance().hasScode(scode) == True:
            return AllError.ok
        dbInfo = self.__updateDbInfo(app)
        if MultiDbHelper.instance().initMySqlWithDatabase(scode, dbInfo['dbHost'], dbInfo['dbPort'], dbInfo['dbUserId'], dbInfo['dbPassword'], scode) == False:
            return AllError.FailToMakePooling
        return AllError.ok

    def __updateDbInfo(self, app):
        if app['dbHost'] is not None:
            return app
        app['dbHost'] = appconfig.dbhost
        app['dbPort'] = appconfig.dbport
        app['dbUserId'] = appconfig.dbuser
        app['dbPassword'] = appconfig.dbpassword
        return app
