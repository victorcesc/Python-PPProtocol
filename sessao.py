from subcamada import Subcamada
from quadro import Quadro

class Sessao(Subcamada):

    def __init__(self, timeout):
        Subcamada.__init__(self, timeout)
        # define o estado desconectado como estado inicial da máquina de estado
        self._fsm = self.state_desconectado
        self.quadro = None
        self.master = 0
        

    def envia(self, dados: Quadro):
        self.quadro = dados
        print("[SESSÃO]: recebendo da app: " , dados.serialize())
        if self._fsm == self.state_conectado:
            print("[SESSÃO]: enviando pro arq: " , dados.serialize())
            # enviar um CR e            
            self.lower.envia(dados)
            # ir para o estado espera se for o iniciador
            if self.master == 1:
                self._fsm = self.state_espera

    def recebe(self, dados: Quadro):
        self.quadro = dados
        self._fsm(dados)
        print("[SESSÃO]: recebendo do arq: " , dados.serialize())
    
    # estado desconectado da máquina de estado
    def state_desconectado(self, dados:Quadro):
        print('[SESSÃO]: desconectado')

        # se receber um CR
        if dados.tipoMsgControle == 0: #CR
            # enviar um CC e
            
            CC = Quadro(tiposessao = dados.tipoSessao,
                msgcontrole = 1,sequencia = dados.sequencia,
                idsessao = dados.idSessao)
            self.lower.envia(CC)
            # ir para o estado conectado
            self._fsm = self.state_conectado

    # estado conectado da máquina de estado
    def state_conectado(self, dados:Quadro):
        print('[SESSÃO]: conectado')
        self.enable_timeout()
        # se receber dados
        if dados.tipoSessao == 0 :
            # enviar mensagem para a aplicação e
            self.upper.recebe(dados)
            # manter no estado atual
        # se receber mensagem da aplicação
        if dados.tipoSessao == 1:
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
        print('[SESSÃO]: half1')

        # se receber um DR
        if dados.tipoMsgControle == 2:
            # enviar um DR e
            self.lower.envia(dados)
            # manter no estado atual

        # se timeout ou receber um DC
        elif dados.tipoMsgControle == 3: # or timeout
            # enviar um reset para o arq
            reset = Quadro(tiposessao = 1,
                sequencia = dados.sequencia,
                idsessao = dados.idSessao,
                data = "reset")

            self.lower.envia(reset)
            # ir para o estado desconectado
            self._fsm = self.state_desconectado

    # estado half2 da máquina de estado
    def state_half2(self, dados:Quadro):
        print('[SESSÃO]: half2')

        # se receber dados
        if dados.tipoSessao == 0:
            # enviar mensagem para a aplicação e
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

    def state_espera(self, dados:Quadro):
        print('[SESSÃO]: espera')
        # se receber um CC
        if dados.tipoMsgControle == 1:
            # ir para o estado conectado
            self._fsm = self.state_conectado

    #isso  é na app e nao na sessao !!!
    def START(self):
        # cria o quadro
        self.master = 1 # definido que esse é o iniciador da conexao
        start = Quadro(tiposessao = 1,sequencia = 0,
                idsessao = ,data="start")
        print('[SESSÃO]: iniciando sessão com id =',start.idSessao)

        if self._fsm == self.state_desconectado:
            # enviar um CR e           
            self.lower.envia(start)
            # ir para o estado espera
            self._fsm = self.state_espera

    def handle(self, dados:Quadro):
        print('handle')

        self._fsm(dados)

    # timeout
    def handle_timeout(self):
        self.disable_timeout()
        