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
        self.queue_msg = []
  
    def recebe(self, quadro:Quadro):
        self.quadro = quadro
        self.sequencia_M = quadro.sequencia
        #self.queue_msg.append(quadro)
        self._fsm(quadro)
        if self.debug:
                print('[ARQ]: entregando quadro para camada superior, tamanho =', len(quadro.serialize()))
      # dados recebidos da subcamada inferior
        


    def envia(self,quadro:Quadro):
        print('[ARQ]enviando quadro sequencia : ', quadro.sequencia)
        self.quadro = quadro
        self.sequencia_N = quadro.sequencia
        if quadro.data == "reset":
            self._fsm = self.state_ocioso
            self.quadro = None
        if self._fsm == self.state_ocioso:
           self.lower.envia(quadro) # !dataN
           self._fsm = self.state_espera
        
        # self._fsm(quadro)
        
    # dataM = 0 recebendo
    # dataN = 1 transmitindo
    def state_ocioso(self, quadro:Quadro):
        # M = 0
        # _M = 1
        self.enable_timeout()        
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.sequencia_M and  quadro.idSessao == self.quadro.idSessao:# dataM 
            print("[ARQ_ocioso1] Sequencia do quadro recebido", quadro.sequencia, "sequencia esperada", self.sequencia_M)
            
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.sequencia_M,idsessao = quadro.idSessao)          
            # ack idSessao tem q ser igual ao quadro data recebido
            print("[ARQ] Enviando ack com sequencia : ", ack.sequencia)
            self.lower.envia(ack) # envia pra camada de baixo         
            self.upper.recebe(quadro) # envia p camada de cima
            self._fsm = self.state_ocioso

        if quadro.tipoMsgArq == 0 and quadro.sequencia !=  self.sequencia_M and  quadro.idSessao == self.quadro.idSessao: # data_M
            print("[ARQ_ocioso2] sequencia do quadro recebido", quadro.sequencia, "sequencia esperada", self.sequencia_M, "e foi descartado")
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = not self.sequencia_M,idsessao = quadro.idSessao)
            print("[ARQ] Enviando ack com sequencia", ack_M.sequencia)
            self.lower.envia(ack_M) # envia p camada de baixo
            self._fsm = self.state_ocioso

            # self._fsm = self.state_espera

    def state_espera(self, quadro:Quadro):
        if quadro.tipoMsgArq == 0 and quadro.sequencia == self.sequencia_M and  quadro.idSessao == self.quadro.idSessao: # ackM , app!msg
            print("[ARQ_espera1] sequencia do quadro recebido", quadro.sequencia, "sequencia esperada", self.sequencia_M)
            ack  = Quadro(tiposessao = 0,msgarq = 1,sequencia = self.sequencia_M,idsessao = quadro.idSessao)
            print("[ARQ] Enviando ack com sequencia", ack.sequencia)
            self.lower.envia(ack)
            self.upper.recebe(quadro)
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 0 and quadro.sequencia != self.sequencia_M and  quadro.idSessao == self.quadro.idSessao  : # data_M
            print("[ARQ_espera2] sequencia do quadro recebido", quadro.sequencia, "sequencia esperada", not self.sequencia_M)
            ack_M  = Quadro(tiposessao = 0,msgarq = 1,sequencia = not self.sequencia_M,idsessao = quadro.idSessao)
            print("[ARQ] Enviando ack com sequencia", ack_M.sequencia)
            self.lower.envia(ack_M)
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 1 and quadro.sequencia != self.sequencia_N and  quadro.idSessao == self.quadro.idSessao: # ack_N
            print("[ARQ_espera3] sequencia do quadro recebido", quadro.sequencia, "sequencia esperada", self.sequencia_N, "e mantem no estado espera")
            self._fsm = self.state_espera
            
        if quadro.tipoMsgArq == 1 and quadro.sequencia == self.sequencia_N and  quadro.idSessao == self.quadro.idSessao:
            print("[ARQ_espera4] sequencia do quadro recebido", quadro.sequencia, "sequencia esperada", self.sequencia_N,"tudo ok e retornou ao ocuioso") # ackN
            self._fsm = self.state_ocioso

    def handle(self):      
        pass

    def handle_timeout(self):
        self.lower.envia(self.quadro)
        