from operator import xor

class Quadro:

    def __init__(self, data):
        self.data = bytearray(data)
        self.controle = bytearray()
        self.reservado = bytearray()
        self.proto = bytearray()
        self.fcs = bytearray()

    def insertEsc(self, data):
        new_data = bytearray()

        for i in range(len(data)):
            if data[i] == 0x7e:
                new_data.append(0x7d)
                new_data.append(xor(data[i], 0x02))
            else:
                new_data.append(data[i])

        return new_data

    def serialize(self):
        self.quadro = bytearray()
        self.quadro.append(0x7e)
        self.quadro += self.controle
        self.quadro += self.reservado
        self.quadro += self.proto
        self.quadro += self.insertEsc(self.data)
        self.quadro += self.fcs
        self.quadro.append(0x7e)

    def setControle(self, controle):
        self.controle = controle

    def setReservado(self, reservado):
        self.reservado = reservado

    def setProto(self, proto):
        self.proto = proto

    def setFcs(self, fcs):
        self.fsc = fcs

    def getData(self):
        return self.data

    def getControle(self):
        return self.controle

    def getReservado(self):
        return self.reservado

    def getProto(self):
        return self.proto

    def getFcs(self):
        return self.fcs