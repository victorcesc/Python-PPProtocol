from operator import xor
import sys
from subcamada import Subcamada
from serial import Serial


class Enquadramento(Subcamada):
    def __init__(self,porta_serial,t_out):
        try:
            self._serial = Serial(porta_serial, 9600, timeout=t_out)
        except Exception as e:
            print('Não conseguiu acessar a porta serial', e)
            sys.exit(0)
        Subcamada.__init__(self,self._serial,t_out)                     
        self.buffer = bytearray() #buffer que recebe os bytes        
        self._fsm = self.state_idle

    
    def envia(self,dados:bytes):
        quadro = bytearray()
        self.esc(dados)
        quadro.append(0x7e)
        quadro += dados
        quadro.append(0x7e)
        self._serial.write(quadro) #escreve na porta serial
  
    def recebe(self):
        #logica de recepcao do enquadramento - fsm   
        octeto = self._serial.read(1)
        self._fsm(octeto)  
        print("octeto : ")
        print(octeto)  
        print(self.buffer)  
        #self.enable()
        #self.enable_timeout()
        #maquina de estados
        


<<<<<<< Updated upstream
    def esc(self, dados):
        quadro = bytearray(dados)

        x = quadro.find(0x7e)
        print(x)
        if x > 0:
            
            quadro.insert(x, 110)
        
        print(x)
        # while(x > 0):
        #     print(x)
        #     quadro.insert(x, 0x7d)

        return quadro
=======
    def state_rx(self,octeto):
        print("rx")
        print(octeto)        
        if octeto.decode() == "~":
            self._fsm = self.state_idle
        if octeto.decode() == "}":
            self._fsm = self.state_esc
        if octeto.decode() != "~" and octeto.decode() != "}":
            self.buffer += octeto
>>>>>>> Stashed changes
        

    def state_idle(self,octeto):
        if octeto.decode() == "~":
            print(octeto)
            print("entrou")
            self._fsm = self.state_prep
        else:
            self._fsm = self.state_idle
        
    def state_prep(self,octeto):
        print(self._fsm)
        print("prep")
        print(octeto)
        if octeto.decode() == "}":
            self._fsm = self.state_esc
        if octeto.decode() != "~":
            self.buffer += octeto
            self._fsm = self.state_rx
        #if timeout:
        #   self._fsm = self.state_idle(octeto) 
        
        
    def state_esc(self,octeto):
        if octeto.decode() == "}" or octeto.decode() == "~": #or timeout
            #descarta
            self._fsm = self.state_idle
        octeto = xor(octeto,0x20)
        self.buffer += octeto

    def handle(self):
        
        #Ao termino das operacoes para enviar para a camada superior
        #octeto = self.porta_serial.read(1)
        # self.buffer += octeto   
        self.recebe()                    
        if len(self.buffer) == 8: 
            print(self.buffer)                     
            #self.upper.recebe(bytes(self.buffer)) 
            #self.buffer.clear()       
        

    def handle_timeout(self):
        self.buffer.clear()
        