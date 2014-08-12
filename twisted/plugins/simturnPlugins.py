# -*- coding: utf-8 -*-
# Started by Alan
# MainTained by Alan
# Contact: alan@sinosims.com

from twisted.application import internet
from twisted.application import service
from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.python import log
from zope.interface import implements

from simturn.core.gol import Gol
from simturn.servers.turnServer import TurnServer
from simturn.servers.stunServer import StunServer
import ConfigParser, socket

def _emit(self, eventDict):
    text = log.textFromEventDict(eventDict)
    if not text: return

    timeStr = self.formatTime(eventDict['time'])
    log.util.untilConcludes(self.write, "%s %s\n" % (timeStr, text.replace("\n", "\n\t")))
    log.util.untilConcludes(self.flush)

class Options(usage.Options):
    optParameters = [["env", None, "test", "The environment of the running application, should be 'test' or 'productino'"],
                     ["pools", None, "../pools", "The dir contains application configuration"],
                     ["log", None, "./logs", "The dir contains application log"]]

class ServiceMaker(object):
    implements(service.IServiceMaker, IPlugin)
    tapname = "simturn"
    description = "Call tunnels of the simhub"
    options = Options

    def makeService(self, options):
        _srvs = service.MultiService()
        _channel = socket.gethostname()

        Gol().init(options["env"])
        application = service.Application("simturn") 

        self.initLog(application, options["env"], options["log"])
        self.initServices(_srvs, _channel, "%s/%s"%(options["pools"], options["env"]))

        _srvs.setServiceParent(application)
        return _srvs

    def initLog(self, app, env, logdir):
        if env == "production":
            from twisted.python.log import ILogObserver, FileLogObserver
            from twisted.python.logfile import DailyLogFile
            logfile = DailyLogFile("production.log", logdir)
            app.setComponent(ILogObserver, FileLogObserver(logfile).emit)
        else:
            log.FileLogObserver.emit = _emit

    def initServices(self, srvs, chn, nsdir):

        with open("%s/channel.ini"%nsdir, 'r') as f:
            chns = dict([ (c[0].strip(), c[1].strip()) for c in [s.split(' ') for s in f.readlines()] ])
            
        with open("%s/stunServer.ini"%nsdir, 'r') as f:
            [ internet.UDPServer(int(addr[1].strip()), StunServer()).setServiceParent(srvs) for addr in [s.split(':') for s in f.readlines()] if chns[addr[0]] == chn ]

        with open("%s/turnServer.ini"%nsdir, 'r') as f:
            [ internet.UDPServer(int(addr[1].strip()), TurnServer()).setServiceParent(srvs) for addr in [s.split(':') for s in f.readlines()] if chns[addr[0]] == chn ]

serviceMaker = ServiceMaker()
