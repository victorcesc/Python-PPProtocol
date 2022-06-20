from subcamada import Subcamada
from quadro import Quadro

class Sessao(Subcamada):

    def __init__(self, timeout):
        Subcamada.__init__(self, timeout)
        # define o estado desconectado como estado inicial da máquina de estado
        self._fsm = self.state_desconectado
        self.quadro = None
    
    # estado desconectado da máquina de estado
    def state_desconectado(self, dados:Quadro):
        print('desconectado')

        # se receber um CR
        if dados.tipoMsgControle == 0:
            # enviar um CC e
            dados.tipoMsgControle = 1
            self.lower.envia(dados)
            # ir para o estado conectado
            self._fsm = self.state_conectado

    # estado conectado da máquina de estado
    def state_conectado(self, dados:Quadro):
        print('conectado')

        # se receber dados
        if dados.tipoSessao == 0:
            # enviar mensagem para a aplicação e
            dados.tipoSessao = 1
            self.upper.recebe(dados)
            # manter no estado atual

        # se receber mensagem da aplicação
        elif dados.tipoSessao == 1:
            # enviar dados e
            dados.tipoSessao = 0
            self.lower.envia(dados)
            # manter no estado atual

        # se receber um DR
        if dados.tipoMsgControle == 2:
            # enviar um DR e
            self.lower.envia(dados)
            # ir para o estado half1
            self._fsm = self.state_half1

        # se receber um STOP
        # if :
        # receber STOP da onde?
        # é um comando pra implementar na camada de aplicação?
            # enviar um DR e
            # dados.tipoMsgControle = 2
            # self.lower.envia(dados)
            # ir para o estado half2
            # self._fsm = self.state_half2

    # estado half1 da máquina de estado
    def state_half1(self, dados:Quadro):
        print('half1')

        # se receber um DR
        if dados.tipoMsgControle == 2:
            # enviar um DR e
            self.lower.envia(dados)
            # manter no estado atual

        # se timeout ou receber um DC
        elif dados.tipoMsgControle == 3: # or timeout
            # enviar um reset para o arq
            self.lower.envia(dados)
            # ir para o estado desconectado
            self._fsm = self.state_desconectado

    # estado half2 da máquina de estado
    def state_half2(self, dados:Quadro):
        print('half2')

        # se receber dados
        if dados.tipoSessao == 0:
            # enviar mensagem para a aplicação e
            dados.tipoSessao = 1
            self.upper.recebe(dados)
            # manter no estado atual

        # se timeout
        # if :
            # enviar DR e
            # dados.tipoMsgArq = 2
            # self.lower.envia(dados)
            # manter no estado atual

        # se timeout
        # if :
            # enviar um reset para o arq e
            # self.lower.envia(dados)
            # ir para o estado desconectado
            # self._fsm = self.state_desconectado

        # se receber um DR
        if dados.tipoMsgControle == 2:
            # enviar um DC e
            dados.tipoMsgControle = 3
            # ir para o estado desconectado
            self._fsm = self.state_desconectado

    def handle(self, dados:Quadro):
        print('handle')

        self._fsm(dados)

    # timeout
    def handle_timeout(self):
        self.disable_timeout()
        self.disable()