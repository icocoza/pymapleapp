
import sys
from AppExecutor import AppExecutor
from common.config.configloader import Config
import common.utils.ExceptionUtil as exutil
import common.utils.InitLogger as InitLogger

appExecutor = None
def _main(argv=None):
    try:
        #argv = ['aa', 'maple', 'dev']
        if len(argv) < 3:
            print('MapleApp needs two parameters. \nFirst: "maple" or ... \nSecond: "dev: or "prod"\n')
            return

        serviceType = argv[1]
        buildType = argv[2]
        if buildType != 'dev' and buildType != 'prod':
            print(f'You have invalid type parameter({buildType}).\nYou have to set "dev" or "prod" for second param.')
            return

        InitLogger.initLogging()
        Config().init(buildType)

        appExecutor = AppExecutor()
        if appExecutor.start(serviceType, buildType) == False:
            print(f'You have wrong service type param({serviceType}). Service type is "maple".')
            sys.exit()
    except Exception as ex:
        exutil.printException()

def main(argv=None):
    try:        
        return _main(argv)
    except KeyboardInterrupt:
        if appExecutor != None:
            appExecutor.stop()
        return 1

if __name__ == "__main__":
    main(sys.argv)