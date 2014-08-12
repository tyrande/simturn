from twisted.internet import protocol
from simturn.core.gol import Gol
import struct

class TurnServer(protocol.DatagramProtocol, object):
    addrPeers = {}
    recvNum = 0
    sendNum = 0

    def datagramReceived(self, dgram, address):
        if len(dgram) > 18:
            tok = dgram[:18]
            self.recvNum = (self.recvNum + 1)%50000
            Gol().logCall('FR', '', address, tok, self.transport.port, self.recvNum)
            self.addrPeers[tok] = address
            othTok = (tok[0] + '\x00' + tok[2:]) if (tok[1] == '\x01') else (tok[0] + '\x01' + tok[2:])
            othAddr = self.addrPeers.get(othTok, None)
            if othAddr:
                self.sendNum = (self.sendNum + 1)%50000
                Gol().logCall('TO', '', address, tok, self.transport.port, self.sendNum)
                self.transport.write(dgram[18:], othAddr)
