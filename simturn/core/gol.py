# -*- coding: utf-8 -*-
# Started by Alan
# MainTained by Alan
# Contact: alan@sinosims.com

class Gol(object):
    # Gol is the global Singlone Class maintain global resource
    # @attr env:            Twisted running envirement (test, dev, production)

    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Gol, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def init(self, env):
        self.env = env

    def logCall(self, dr, channel, addr, tok, port, num):
        if not num%100 == 0: return
        dr = '\033[47;34m %s '%dr if dr == 'TO' else '\033[43;37m %s '%dr
        tok = ["{0:02X}".format(ord(i)) for i in tok]
        tok = tok[0] + '-' + tok[1] + '-' + ''.join(tok[2:])
        print "\033[45;37m[{0:>15}:{1:<5}][{2}]\033[49;36m [V {3}] deva:{4} {5}\033[0m".format(addr[0], addr[1], dr, tok, port, num)

