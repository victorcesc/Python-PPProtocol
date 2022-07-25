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
        print("RECEBE timeout enabled? : ", self.timeout_enabled)
        print("Quadro : ", self.quadro.data)
        print("estado recebe : " ,self._fsm)
        self._fsm(quadro)
        if self.debug:
                print('[ARQ]: entregando quadro para camada superior, tamanho =', len(quadro.serialize()))       
        if quadro.tipoMsgArq == 0:
           self.sequencia_M = not self.sequencia_M  
 
    def envia(self,quadro:Quadro):
        print("estado envia : ",self._fsm)
        print("ENVIA timeout enabled? : ", self.timeout_enabled)
        self.quadro = quadro
        self.queue_msg.put(quadro) 
        if quadro.data == "reset":
            self._fsm = self.state_ocioso
            self.quadro = None
        if self._fsm == self.state_ocioso:
           if self.queue_msg.qsize() > 1:                     
              self.lower.envia(self.queue_msg.get()) # !dataN 
              self.sequencia_N = not self.sequencia_N    
           self.lower.envia(self.queue_msg.get())      
           self._fsm = self.state_espera
        
        
    # dataM = 0 recebendo
    # dataN = 1 transmitindo
    def state_ocioso(self, quadro:Quadro):
        # M = 0
        # _M = 1
        self.disable_timeout()
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.sequencia_M and  quadro.idSessao == self.quadro.idSessao:# dataM 
            print("recebendo dataM")
            print("sequencia correta: ",self.sequencia_M, "sequencia q veio : " ,quadro.sequencia )
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = quadro.sequencia,idsessao = quadro.idSessao)  
            # ack idSessao tem q ser igual ao quadro data recebido
            self.lower.envia(ack) # envia pra camada de baixo             
            self.upper.recebe(quadro) # envia p camada de cima
            self._fsm = self.state_ocioso

        if quadro.tipoMsgArq == 0 and quadro.sequencia !=  self.sequencia_M and  quadro.idSessao == self.quadro.idSessao: # data_M
            print("recebendo data_M")
            print("preciso da retransmissao!!! sequencia correta: ",self.sequencia_M, "sequencia q veio : " ,quadro.sequencia )
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = quadro.sequencia,idsessao = quadro.idSessao)
            self.lower.envia(ack_M) # envia p camada de baixo 
            self._fsm = self.state_ocioso

    def state_espera(self, quadro:Quadro, timeout:bool = False):
        if not self.timeout_enabled:
            self.reload_timeout()
            self.enable_timeout()
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.sequencia_M and  quadro.idSessao == self.quadro.idSessao: # ackM , app!msg
            print("entrou aqui dataM, devolvendo ackM")
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = quadro.sequencia,idsessao = quadro.idSessao)
            self.lower.envia(ack)
            self.upper.recebe(quadro)
            self.sequencia_M = not self.sequencia_M  
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 0 and quadro.sequencia != self.sequencia_M and  quadro.idSessao == self.quadro.idSessao  : # data_M
            print("entrou aqui data_M devolvendo ack_M")
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.sequencia_M,idsessao = quadro.idSessao)
            self.lower.envia(ack_M)
            self._fsm = self.state_espera            
        
        if quadro.tipoMsgArq == 1 and quadro.sequencia != self.sequencia_N and  quadro.idSessao == self.quadro.idSessao: # ack_N
            print("ack_N retransmite?")
            self.quadro.sequencia = not self.quadro.sequencia
            self.lower.envia(self.quadro)                 
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 1 and quadro.sequencia == self.sequencia_N and  quadro.idSessao == self.quadro.idSessao:
            print("AckN normal")
            self.sequencia_N = not self.sequencia_N            
            self._fsm = self.state_ocioso

        if timeout:
            print("retransmitindo", self.quadro)
            self.lower.envia(self.quadro)
            self.disable_timeout()

    def handle(self):      
        pass

    def handle_timeout(self):
        print("TIMEOUT")
        if self._fsm == self.state_espera:
            self._fsm(self.quadro,True)
        