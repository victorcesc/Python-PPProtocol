from operator import xor
import sys
from subcamada import Subcamada
from serial import Serial
from quadro import Quadro
import crc

class Enquadramento(Subcamada):
    def __init__(self,porta_serial,t_out):
        try:
            self._serial = Serial(porta_serial, 9600, timeout=t_out)
        except Exception as e:
            print('Não conseguiu acessar a porta serial', e)
            sys.exit(0)
        Subcamada.__init__(self,self._serial,t_out)
        self.debug = False
        self.buffer = bytearray() # buffer que recebe os bytes
        self._fsm = self.state_idle
    
    def envia(self,quadro:Quadro):
        dados = bytearray()
        dados.append(0x7e)
        dados += quadro.serialize()        
        dados.append(0x7e)
        self._serial.write(dados) # escreve na porta serial
        if self.debug:
                print('[ENQ]: enviando quadro, tamanho =', len(dados))
  
    def recebe(self):
        # lógica de recepcao do enquadramento - fsm
        octeto = self._serial.read(1)
        self._fsm(octeto)
        
    def state_rx(self,octeto):              
        if octeto.decode(errors='replace') == "~":
            fcs = crc.CRC16(self.buffer)            
            if fcs.check_crc(): 
                quadro = self.desserializa(self.buffer)        
                self.upper.recebe(quadro)
                self.buffer.clear()                             
                self._fsm = self.state_idle
        if octeto.decode(errors='replace') == "}":
            self._fsm = self.state_esc
        if octeto.decode(errors='replace') != "~" and octeto.decode(errors='replace') != "}":
            self.buffer += octeto

    def state_idle(self,octeto):
        if octeto.decode(errors='replace') == "~":            
            self._fsm = self.state_prep
        else:
            self._fsm = self.state_idle
        
    def state_prep(self,octeto):
        if octeto.decode(errors='replace') == "}":
            self._fsm = self.state_esc
        if octeto.decode(errors='replace') != "~" and octeto.decode(errors='replace') != "}":
            self.buffer += octeto
            self._fsm = self.state_rx
        
    def state_esc(self,octeto):        
        if octeto.decode(errors='replace') == "}" or octeto.decode(errors='replace') == "~": #or timeout
            # descarta
            self._fsm = self.state_idle                
        octeto = chr(ord(octeto.decode()) ^ ord(bytes(" ",'utf-8').decode())) #xor com 0x20(" ")
        self.buffer += octeto.encode()
        self._fsm = self.state_rx

    def handle(self):       
        self.recebe() 

    def handle_timeout(self):
        self.buffer.clear()

    def desserializa(self,dados:bytearray):        
        msgarq = (dados[0] & (1 << 7) ) >> 7
        sequencia = (dados[0] & (1 << 3) ) >> 3
        tiposessao = (dados[0] & (1 << 2) ) >> 2   
        msgcontrole = 0     
        if tiposessao == 1:            
            msgcontrole |= ( ( (dados[0] & (1 << 1) ) >> 1 ) << 1)
            msgcontrole |= ( ( (dados[0] & (1 << 0) ) >> 0 ) << 0)
        idSessao = dados[1]
        idProto = dados[2]
        data = dados[3:len(dados)-2].decode(errors='replace')
        # fcs nao precisa pq é gerado qnd é serializado novamente        
        quadro = Quadro(tiposessao = tiposessao, msgarq = msgarq,sequencia = sequencia,msgcontrole=msgcontrole,idsessao = idSessao,idproto = idProto,data = data)
        return quadro