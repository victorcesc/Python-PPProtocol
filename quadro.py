
import crc

'''
byte controle
bit 7 = tipo de quadro
bit 3 = sequencia

bit 2 = indica qual ẽ o tipo de mensagem pra conteudo de conexao (0=dados 1=controle) 
bit 0 e 1  =  {00 = CR // 01 = CC // 10 = DR // 11 = DC}
'''

class Quadro:

    def __init__(self, tipo, sequencia, tipo_sessao, msg_sessao, id_sessao, proto, data):
        self.tipo = tipo
        self.sequencia = sequencia
        self.tipo_sessao = tipo_sessao
        self.msg_sessao = msg_sessao
        self.sessao = id_sessao
        self.controle = 0
        if self.tipo == 0:
            self.proto = proto    
        self.data = data

    def serialize(self):
        # cria um vetor de bytes
        self.quadro = bytearray()
        # adiciona o delimitador do quadro
        self.quadro.append(0x7e)

        # modifica o bit 7 do byte de controle para indicar o tipo
        # e o bit 3 para indicar a sequencia
        self.controle |= (self.tipo << 7)
        self.controle |= (self.sequencia << 3)

        # modifica o bit 2 do byte de controle da sessão para indicar o tipo
        # e o bit 1 e 0 para indicar o tipo de mensagem de controle
        self.controle |= (self.tipo_sessao << 2)
        self.controle |= (self.msg_sessao << 0)

        # adiciona o byte de controle ao quadro
        # self.controle = 0x04
        self.quadro.append(self.controle)
        self.quadro.append(self.sessao)

        # se o tipo é 0 (dados)
        # adiciona o byte de proto ao quadro
        if self.tipo == 0:
            self.quadro.append(self.proto)

        # adiciona os dados ao quadro
        self.quadro += self.data.encode()

        # gerar crc e formata o quadro com o fcs no final
        fcs = crc.CRC16(self.quadro)
        self.quadro = fcs.gen_crc()

        # delimitador de quadro
        self.quadro.append(0x7e)

        # retorna o quadro
        return self.quadro