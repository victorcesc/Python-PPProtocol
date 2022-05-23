import sys
from subcamada import Subcamada
from serial import Serial


class Enquadramento(Subcamada):
    def __init__(self,porta_serial,t_out):
        Subcamada.__init__(self,porta_serial,t_out)
        self.porta_serial = porta_serial
        self.buffer = bytearray() #buffer que recebe os bytes
        try:
            self._serial = Serial(self._porta_serial, 9600, timeout=self._tout)
        except Exception as e:
            print('Não conseguiu acessar a porta serial', e)
            sys.exit(0)
        self._fsm = None

    
    def envia(self,dados:bytes):
        quadro = self.delimita(dados) #delimita os dados com as flags de quadro
        self._serial.write(quadro) #escreve na porta serial
  
    def recebe(self):
        #logica de recepcao do enquadramento - fsm
        dados = self._serial.read(128)
        return dados  



    def delimita(self, dados):
        quadro = bytearray()
        quadro.append(0x7e)
        quadro += dados
        quadro.append(0x7e)
        return quadro


    def state_rx(self,dados):
        pass

    def handle(self):
        
        #Ao termino das operacoes para enviar para a camada superior
        octeto = self.porta_serial.read(1)
        self.buffer += octeto
        if len(self.buffer) == 8:
            self.upper.recebe(bytes(self.buffer))        
        

    def handle_timeout(self):
        self.buffer.clear()
        pass