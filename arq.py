from queue import Queue
import sys
from subcamada import Subcamada
from quadro import Quadro

# ack = 1
# Data = 0

# dataM = 0
# dataN = 1
# verifica o id conexão correspondente que esta recebendo
class Arq(Subcamada):
    
    def __init__(self, timeout):
        Subcamada.__init__(self, timeout)
        self._fsm = self.state_ocioso
        self.quadro = None
        self.debug = False
        self.sequencia_M = 0
        self.sequencia_N = 0
        self.queue_msg = Queue()
  
    def recebe(self, quadro:Quadro):
        self.quadro = quadro
        self._fsm(quadro)
        if self.debug:
                print('[ARQ]: entregando quadro para camada superior, tamanho =', len(quadro.serialize()))       
      # dados recebidos da subcamada inferior
        if quadro.tipoMsgArq == 0:
           self.sequencia_M = not self.sequencia_M  
 
    def envia(self,quadro:Quadro):
        self.quadro = quadro
        if quadro.data == "reset":
            self._fsm = self.state_ocioso
            self.quadro = None
        if self._fsm == self.state_ocioso:
           self.lower.envia(quadro) # !dataN 
           self._fsm = self.state_espera
        
        
    # dataM = 0 recebendo
    # dataN = 1 transmitindo
    def state_ocioso(self, quadro:Quadro):
        # M = 0
        # _M = 1
        
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.sequencia_M and  quadro.idSessao == self.quadro.idSessao:# dataM 
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = quadro.sequencia,idsessao = quadro.idSessao)  
            # ack idSessao tem q ser igual ao quadro data recebido
            self.lower.envia(ack) # envia pra camada de baixo             
            self.upper.recebe(quadro) # envia p camada de cima
            self._fsm = self.state_ocioso

        if quadro.tipoMsgArq == 0 and quadro.sequencia !=  self.sequencia_M and  quadro.idSessao == self.quadro.idSessao: # data_M
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.sequencia_M,idsessao = quadro.idSessao)
            self.lower.envia(ack_M) # envia p camada de baixo 
            self._fsm = self.state_ocioso


    def state_espera(self, quadro:Quadro):
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.sequencia_M and  quadro.idSessao == self.quadro.idSessao: # ackM , app!msg
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = quadro.sequencia,idsessao = quadro.idSessao)
            self.lower.envia(ack)
            self.upper.recebe(quadro)
            self.sequencia_M = not self.sequencia_M  
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 0 and quadro.sequencia != self.sequencia_M and  quadro.idSessao == self.quadro.idSessao  : # data_M
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.sequencia_M,idsessao = quadro.idSessao)
            self.lower.envia(ack_M)
            self._fsm = self.state_espera            
        
        
        if quadro.tipoMsgArq == 1 and quadro.sequencia != self.sequencia_N and  quadro.idSessao == self.quadro.idSessao: # ack_N
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 1 and quadro.sequencia == self.sequencia_N and  quadro.idSessao == self.quadro.idSessao:
            self.sequencia_N = not self.sequencia_N            
            self._fsm = self.state_ocioso

    def handle(self):      
        pass

    def handle_timeout(self):
        self.lower.envia(self.quadro)
        