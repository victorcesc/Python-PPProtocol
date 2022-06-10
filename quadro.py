
class Quadro:

    def __init__(self, tipo, sequencia, reservado, proto, data,fcs):
        self.tipo = tipo
        self.sequencia = sequencia
        self.reservado = reservado
        self.controle = 0
        if self.tipo == 0:
            self.proto = proto    
        self.data = data
        self.fcs = fcs
 

    def serialize(self):
        self.quadro = bytearray()
        self.quadro.append(0x7e)
        self.controle |= (self.tipo << 7)
        self.controle |= (self.sequencia << 3)
        self.quadro += self.controle
        self.quadro += self.reservado
        self.quadro += self.proto
        self.quadro += self.data
        self.quadro += self.fcs
        self.quadro.append(0x7e)

    def deserialize(self):
        pass