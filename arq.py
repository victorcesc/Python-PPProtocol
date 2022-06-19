import sys
from subcamada import Subcamada
from quadro import Quadro

# ack = 0
# Data = 1
#verifica o id conexao correspondente que esta recebendo
class Arq(Subcamada):
    
    def __init__(self, timeout):
        Subcamada.__init__(self, timeout)
        self._fsm = self.state_ocioso
        self.quadro = None
  
    def recebe(self, quadro:Quadro):
        self._fsm(quadro)
      # dados recebidos da subcamada inferior

    def envia(self,quadro:Quadro):
        if self._fsm == self.state_ocioso:
           self.lower.envia(quadro)
           self._fsm = self.state_espera
           self._fsm(quadro)
        #se esta no estado ocioso faz algo se n faz nada

    def state_ocioso(self, quadro:Quadro):
        #M = 0
        #_M = 1        
        if quadro.tipoMsgArq == 0 and quadro.sequencia == 0 :
          ack  = Quadro(0,0,0,0,"ack")
          #ack tipoSessao tem q ser igual ao quadro data recebido
          self.lower.envia(ack) #envia pra camada de baixo         
          self.upper.recebe(quadro) #envia p camada de cima
        if quadro.tipoMsgArq == 1 and quadro.sequencia == 1:
          ack_M = Quadro(tiposessao = 1,data = "ack") #apenas teste
          self.lower.envia(ack_M)#envia p camada de baixo

        self._fsm = self.state_espera

    def state_espera(self, quadro:Quadro):
        if quadro.tipoMsgArq == 0 and quadro.sequencia == 0 :
            ack  = Quadro(0,0,0,0,"ack")
            self.lower.envia(ack)
            self.upper.recebe(quadro)
        if quadro.tipoMsgArq == 0 and quadro.sequencia == 1 :
            ack_M  = Quadro(0,0,0,0,"ack")
            self.lower.envia(ack_M)
        if quadro.tipoMsgArq == 1 and quadro.sequencia == 0:
            self._fsm = self.state_espera
        if quadro.tipoMsgArq == 1 and quadro.sequencia == 1:
            self._fsm = self.state_ocioso
        

    def handle(self):      
      #o que eu colocaria aqui...
      pass
