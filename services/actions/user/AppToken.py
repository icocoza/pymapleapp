from datetime import datetime, timedelta
import common.utils.CryptoHelper as CryptoHelper
from services.actions.admin.AdminToken import AdminToken
from repository.db.admin.AdminAppRepository import AdminAppRepository
from services.constant.AllError import AllError
from services.constant.MapleEnum import EAdminAppStatus
from module.db.MultiDbHelper import MultiDbHelper

class AppToken(AdminToken):

    def __init__(self):
        super().__init__()

        self.adminAppRepository = AdminAppRepository()

    def checkScode(self, scode):
        app = self.adminAppRepository.getAppByScode(scode)
        if app == None:
            return AllError.NoServiceCode
        if app['status'] != EAdminAppStatus.ready.name():
            return AllError.NotAvailableServiceCode
            #def addMySql(self, scode, host, port, user, passwd, dbname, cbAndEvt):
        if MultiDbHelper.instance().hasScode(scode) == True:
            return AllError.ok
        if MultiDbHelper.instance().initMySqlWithDatabase(scode, app['dbHost'], app['dbPort'], app['dbUserId'], app['dbPassword'], scode) == False:
            return AllError.FailToMakePooling
        return AllError.ok
