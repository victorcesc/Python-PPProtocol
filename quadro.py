from operator import xor
import crc

'''
byte controle
bit 7 = tipo de quadro
bit 3 = sequencia

bit 2 = indica qual ẽ o tipo de mensagem pra conteudo de conexao (0=dados 1=controle) 
bit 0 e 1  =  {00 = CR // 01 = CC // 10 = DR // 11 = DC}


~~~ DUVIDA PROTO ~~~

'''

class Quadro:
    
    '''
    tiposessao :
    0 - dados
    1 - controle

    msgarq :
    0 - data
    1 - ack    
    
    '''
    def __init__(self, **kwargs):
        self.controle = 0
        if kwargs is not None:
            # tipo sessao pode ser dados(0) ou controle(1)
            if 'tiposessao' in kwargs:
                self.tipoSessao = kwargs['tiposessao']
            else:
                raise ValueExcpetion('falta o bit de tipo de sessao')

            if 'msgarq' in kwargs:
                self.tipoMsgArq = kwargs['msgarq']
            else:
                self.tipoMsgArq = 0

            if 'msgcontrole' in kwargs:
                self.tipoMsgControle = kwargs['msgcontrole']
            else:
                self.tipoMsgControle = 0

            if 'sequencia' in kwargs:
                self.sequencia = kwargs['sequencia']
            else:
                raise ValueException('falta o bit de sequencia') 
            
            if 'idsessao' in kwargs:
                self.idSessao = kwargs['idsessao']
            else: 
                raise ValueException('falta o byte de idSessao')

            if 'idproto' in kwargs:
                self.idProto = kwargs['idproto']
            else:
                self.idProto = 1
            
            if 'data' in kwargs:
                self.data = kwargs['data']
            else:
                self.data = ""
            
            if 'fcs' in kwargs:
                self.fcs = kwargs['fcs']

    def insertEsc(self, data):
        new_data = bytearray()

        for i in range(len(data)):
            if data[i] == 0x7e:
                new_data.append(0x7d)
                new_data.append(xor(data[i], 0x02))
                print('esc encontrado')
            else:
                new_data.append(data[i])

        return new_data

    def serialize(self):
        # cria um vetor de bytes
        self.quadro = bytearray()        
        # modifica o bit 7 do byte de controle para indicar o tipo
        # e o bit 3 para indicar a sequencia
        self.controle |= (self.tipoMsgArq << 7)
        self.controle |= (self.sequencia << 3)
        self.controle |= (self.tipoSessao << 2)
        #CR
        if self.tipoMsgControle == 0:
            self.controle |= (0 << 1)
            self.controle |= (0 << 0)
        #CC
        if self.tipoMsgControle == 1:
            self.controle |= (0 << 1)
            self.controle |= (1 << 0)
        #DR
        if self.tipoMsgControle == 2:
            self.controle |= (1 << 1)
            self.controle |= (0 << 0)
        #DC
        if self.tipoMsgControle == 3:
            self.controle |= (1 << 1)
            self.controle |= (1 << 0)
        # adiciona o byte de controle ao quadro
        self.quadro.append(self.controle)
        self.quadro.append(self.idSessao)

        # se o tipo é 0 (dados)
        # adiciona o byte de proto ao quadro
        if self.tipoMsgArq == 0:
            self.quadro.append(self.idProto)

        # adiciona os dados ao quadro
        self.quadro += self.insertEsc(self.data.encode())

        # gerar crc e formata o quadro com o fcs no final
        fcs = crc.CRC16(self.quadro)
        self.quadro = fcs.gen_crc()        

        # retorna o quadro
        return self.quadro

    def deserializa(self, bytes):
        pass