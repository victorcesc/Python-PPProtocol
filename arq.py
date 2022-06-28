import sys
from subcamada import Subcamada
from quadro import Quadro

# ack = 1
# Data = 0

#dataM = 0
#dataN = 1
#verifica o id conexao correspondente que esta recebendo
class Arq(Subcamada):
    
    def __init__(self, timeout):
        Subcamada.__init__(self, timeout)
        self._fsm = self.state_ocioso
        self.quadro = None
        self.enable_timeout()
  
    def recebe(self, quadro:Quadro):
        self.quadro = quadro
        self._fsm(quadro)        
        print("[ARQ]: recebendo do enq : " , quadro.serialize())
      # dados recebidos da subcamada inferior

    def envia(self,quadro:Quadro):
        self.quadro = quadro
        print( "[ARQ]: recebendo da sessão : " , quadro.serialize())
        if self._fsm == self.state_ocioso:
           print("[ARQ]: enviando pro enq : " , quadro.serialize())
           self.lower.envia(quadro)#!dataN
           self._fsm = self.state_espera
        #self._fsm(quadro)
        
    #dataM = 0 recebendo
    #dataN = 1 transmitindo
    def state_ocioso(self, quadro:Quadro):
        #M = 0
        #_M = 1        
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.quadro.sequencia :#dataM 
          ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.quadro.sequencia,idsessao = quadro.idSessao)          
          #ack idSessao tem q ser igual ao quadro data recebido
          self.lower.envia(ack) #envia pra camada de baixo         
          self.upper.recebe(quadro) #envia p camada de cima
        if quadro.tipoMsgArq == 0 and quadro.sequencia !=  self.quadro.sequencia: #data_M
          print("recebeu data_M e enviou ack -- quadro recebido", quadro.sequencia)
          ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.quadro.sequencia,idsessao = quadro.idSessao)
          self.lower.envia(ack_M)#envia p camada de baixo
         
        #self._fsm = self.state_espera

    def state_espera(self, quadro:Quadro):
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.quadro.sequencia: #ackM , app!msg
            print("entrou no !ackM, app!msg")
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.quadro.sequencia,idsessao = quadro.idSessao)
            self.lower.envia(ack)
            self.upper.recebe(quadro)
            
        if quadro.tipoMsgArq == 0 and quadro.sequencia != self.quadro.sequencia: #data_M
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = not self.quadro.sequencia,idsessao = quadro.idSessao)
            self.lower.envia(ack_M)
            
        if quadro.tipoMsgArq == 1 and quadro.sequencia != self.quadro.sequencia: #ack_N
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 1 and quadro.sequencia == self.quadro.sequencia: #ackN
            self._fsm = self.state_ocioso
            
        

    def handle(self):      
      #o que eu colocaria aqui...
      pass

    def handle_timeout(self):
        self.lower.envia(self.quadro)
        