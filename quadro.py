

'''
byte controle
bit 7 = tipo de quadro
bit 3 = sequencia

bit 2 = indica qual ẽ o tipo de mensagem pra conteudo de conexao (0=dados 1=controle) 
bit 0 e 1  =  {00 = CR // 01 = CC // 10 = DR // 11 = DC}
'''

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

   