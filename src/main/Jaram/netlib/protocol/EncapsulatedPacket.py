# Jaram
# A MC:BE Software
# https://github.com/SFWTeam/Jaram
# By SFW-Team
# And GianC-Dev
#-------------------------------

from src.main.Jaram.netlib.Binary import Binary


class EncapsulatedPacket:
    reliability = None
    hasSplit = False
    length = 0
    messageIndex = None
    orderIndex = None
    orderChannel = None
    splitCount = None
    splitID = None
    splitIndex = None
    buffer = bytearray()
    needACK = False
    identifierACK = None

    @staticmethod
    def fromBinary(binary, internal = False, offset = None):
        if isinstance(binary, str):
            binary = bytes(binary, "UTF-8")
        packet = EncapsulatedPacket()
        flags = binary[0]
        packet.reliability = (flags & 0b11100000) >> 5
        packet.hasSplit = (flags & 0b00010000) > 0
        if internal:
            length = Binary.readInt(binary[1:5])
            packet.identifierACK = Binary.readInt(binary[5:9])
            offset = 9
        else:
            length = int(Binary.readShort(binary[1:3]) / 8)
            offset = 3
            packet.identifierACK = None

        if packet.reliability > 0:
            if (packet.reliability > 2 or packet.reliability == 2) and packet.reliability is not 5:
                packet.messageIndex = Binary.readLTriad(binary[offset:offset+3])
                offset += 3

            if (packet.reliability < 4 or packet.reliability == 4) and packet.reliability is not 2:
                packet.orderIndex = Binary.readLTriad(binary[offset:offset+3])
                offset += 3
                packet.orderChannel = Binary.readByte(binary[offset:offset+1])
                offset += 1

        if packet.hasSplit:
            packet.splitCount = Binary.readInt(binary[offset:offset+4])
            offset += 4
            packet.splitID = Binary.readShort(binary[offset:offset+2])
            offset += 2
            packet.splitIndex = binary.readInt(binary[offset:offset+4])
            offset += 4

        packet.buffer = binary[offset:offset+length]
        offset += length

        return packet, offset

    def getTotalLength(self):
        length = 3 + len(self.buffer)
        if self.messageIndex is not None:
            length += 3
        if self.orderIndex is not None:
            length += 4
        if self.hasSplit:
            length += 10

        return length

    def toBinary(self, internal = False):
        payload = bytearray()
        if self.hasSplit:
            payload += (Binary.writeByte((self.reliability << 5) | 0b00010000))
        else :
            payload += (Binary.writeByte(self.reliability << 5))

        if internal:
            payload += (Binary.writeInt(len(self.buffer)))
            payload += (Binary.writeInt(self.identifierACK))
        else:
            payload += (Binary.writeShort(len(self.buffer) << 3))

        if self.reliability > 0:
            if (self.reliability > 2 or self.reliability == 2) and self.reliability is not 5:
                payload += (Binary.writeLTriad(self.messageIndex))
            if (self.reliability < 4 or self.reliability == 4) and self.reliability is not 2:
                payload += (Binary.writeLTriad(self.orderIndex))
                payload += (Binary.writeByte(self.orderChannel))

        if self.hasSplit:
            payload += (Binary.writeInt(self.splitCount))
            payload += (Binary.writeShort(self.splitID))
            payload += (Binary.writeInt(self.splitIndex))

        payload += (self.buffer)

        return payload