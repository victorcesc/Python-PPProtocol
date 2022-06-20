from operator import xor
import sys
from subcamada import Subcamada
from serial import Serial
from quadro import Quadro


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

    
    def envia(self,quadro:Quadro):        
        #self.esc(dados) 
        dados = bytearray()
        dados.append(0x7e)
        dados += quadro.serialize()        
        dados.append(0x7e)   
        print(dados)   
        self._serial.write(dados) #escreve na porta serial
  
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
        
    def esc(self, dados):
        quadro = bytearray(dados)

        x = quadro.find(0x7e)
       # print(x)
        if x > 0:            
            quadro.insert(x, 110)        
        #print(x)
        # while(x > 0):
        #     print(x)
        #     quadro.insert(x, 0x7d)

        return quadro

        
    def state_rx(self,octeto):
        print("rx")
        print(octeto)        
        if octeto.decode(errors='replace') == "~":
            self._fsm = self.state_idle
        if octeto.decode(errors='replace') == "}":
            self._fsm = self.state_esc
        if octeto.decode(errors='replace') != "~" and octeto.decode(errors='replace') != "}":
            self.buffer += octeto
        

    def state_idle(self,octeto):
        if octeto.decode(errors='replace') == "~":
            print(octeto)
            print("entrou")
            self._fsm = self.state_prep
        else:
            self._fsm = self.state_idle
        
    def state_prep(self,octeto):
        print(self._fsm)
        print("prep")
        print(octeto)
        if octeto.decode(errors='replace') == "}":
            self._fsm = self.state_esc
        if octeto.decode(errors='replace') != "~" and octeto.decode(errors='replace') != "}":
            self.buffer += octeto
            self._fsm = self.state_rx
        
        #if timeout:
       
        
        
    def state_esc(self,octeto):
        print("esc")
        if octeto.decode(errors='replace') == "}" or octeto.decode(errors='replace') == "~": #or timeout
            #descarta
            self._fsm = self.state_idle                
        octeto = chr(ord(octeto.decode()) ^ ord(bytes(" ",'utf-8').decode())) #xor com 0x20(" ")
        self.buffer += octeto.encode()
        self._fsm = self.state_rx

    def handle(self):
        
        #Ao termino das operacoes para enviar para a camada superior
        #octeto = self.porta_serial.read(1)
        # self.buffer += octeto   
        self.recebe() 
        print(len(self.buffer))                   
        if len(self.buffer) == 8:             
            print(self.buffer)                     
            self.upper.recebe(bytes(self.buffer)) #envia p camada de cima
            self.buffer.clear()       
        

    def handle_timeout(self):
        self.buffer.clear()
        