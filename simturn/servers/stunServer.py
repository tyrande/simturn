from twisted.internet import protocol
import struct

class StunServer(protocol.DatagramProtocol, object):
    def datagramReceived(self, dgram, address):
        a, b, c, d = [ chr(int(i)) for i in address[0].split('.') ]
        ret = struct.pack('!ccccH%ds'%len(dgram), a, b, c, d, address[1], dgram)
        self.transport.write(ret, address)
