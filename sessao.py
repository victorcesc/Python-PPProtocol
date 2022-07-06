from math import fsum
from subcamada import Subcamada
from quadro import Quadro

class Sessao(Subcamada):

    def __init__(self, timeout):
        Subcamada.__init__(self, timeout)
        # define o estado desconectado como estado inicial da máquina de estado
        self._fsm = self.state_desconectado
        self.quadro = None
        self.master = 0
        self.debug = False

    def envia(self, quadro: Quadro):
        self.quadro = quadro
        if self.state_desconectado and quadro.data == "start":
            #envia CR(0)
            CR = Quadro(tiposessao = quadro.tipoSessao,
                msgcontrole = 0,sequencia = quadro.sequencia,
                idsessao = quadro.idSessao)
            self.lower.envia(CR)    
            self._fsm = self.state_espera        
        if self._fsm == self.state_conectado:
            self.lower.envia(quadro)
            # ir para o estado espera se for o iniciador
            
    def recebe(self, quadro: Quadro):
        self.quadro = quadro
        self._fsm(quadro)
    
    # estado desconectado da máquina de estado
    def state_desconectado(self, quadro:Quadro):
        # se receber um CR
        if quadro.tipoMsgControle == 0: # CR
            if self.debug:
                print('[SESSÃO]: recebeu quadro de controle CR')
            # enviar um CC(1)            
            CC = Quadro(tiposessao = quadro.tipoSessao,
                msgcontrole = 1,sequencia = quadro.sequencia,
                idsessao = quadro.idSessao)
            self.lower.envia(CC)
            # ir para o estado conectado
            self._fsm = self.state_conectado

    # estado conectado da máquina de estado
    def state_conectado(self, quadro:Quadro):
        self.enable_timeout()
        # se receber quadro
        if quadro.tipoSessao == 0 :
            # enviar mensagem para a aplicação e
            self.upper.recebe(quadro)
            # manter no estado atual
        # se receber mensagem da aplicação        

        # se receber um DR
        if quadro.tipoMsgControle == 2:
            # enviar um DR e
            self.lower.envia(quadro)
            # ir para o estado half1
            self._fsm = self.state_half1
        
    def state_half1(self, quadro:Quadro):
        # se receber um DR
        if quadro.tipoMsgControle == 2:
            # enviar um DR e
            self.lower.envia(quadro)
            # manter no estado atual

        # se timeout ou receber um DC
        elif quadro.tipoMsgControle == 3: # or timeout
            # enviar um reset para o arq
            reset = Quadro(tiposessao = 1,
                sequencia = quadro.sequencia,
                idsessao = quadro.idSessao,
                data = "reset")
            self.lower.envia(reset)
            # ir para o estado desconectado
            self._fsm = self.state_desconectado

    # estado half2 da máquina de estado
    def state_half2(self, quadro:Quadro):
        # se receber quadro
        if quadro.tipoSessao == 0:
            # enviar mensagem para a aplicação e
            self.upper.recebe(quadro)
            # manter no estado atual

        # se receber um DR
        if quadro.tipoMsgControle == 2:
            # enviar um DC e
            DC = Quadro(tiposessao = quadro.tipoSessao,
                msgcontrole = 3,sequencia = quadro.sequencia,
                idsessao = quadro.idSessao)
            # ir para o estado desconectado
            self._fsm = self.state_desconectado

    def state_espera(self, quadro:Quadro):
        # se receber um CC
        if quadro.tipoMsgControle == 1:
            if self.debug:
                print('[SESSÃO]: recebeu quadro de controle CC')
            # ir para o estado conectado
            self._fsm = self.state_conectado

    def handle(self, quadro:Quadro):
        pass
        
    # timeout
    def handle_timeout(self):
        if self._fsm == self.state_half2 and self._fsm == self.state_half1:
            reset = Quadro(tiposessao = 1,
                sequencia = self.quadro.sequencia,
                idsessao = self.quadro.idSessao,
                data = "reset")
            self.lower.envia(reset)
            self._fsm = self.state_desconectado
        if self.master == 1 and self._fsm == self.state_espera:
            reset = Quadro(tiposessao = 1,
                sequencia = self.quadro.sequencia,
                idsessao = self.quadro.idSessao,
                data = "reset")
            self.lower.envia(reset)
            self._fsm = self.state_desconectado
        self.disable_timeout()