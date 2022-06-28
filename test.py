from arq import Arq
from pypoller import poller
import sys
from sessao import Sessao
from subcamada import Subcamada
from enq import Enquadramento
from adp import Aplicacao
from serial import Serial

Timeout = 7 


# nome da porta serial informada como primeiro argumento
# de linha de comando
porta = sys.argv[1]

# cria objeto Enquadramento
enq = Enquadramento(porta, Timeout)

# Cria objeto Aplicacao
app = Aplicacao()

arq = Arq(Timeout)

sessao = Sessao(Timeout)

# Conecta as subcamadas
# Deve ser feito a partir da subcamada inferior
#enq.conecta(app)
enq.conecta(arq)
arq.conecta(sessao)
sessao.conecta(app)
# cria o Poller e registra os callbacks
sched = poller.Poller()

sched.adiciona(enq)
sched.adiciona(app)
#sched.adiciona(arq)
#enq.enable()
#enq.enable_timeout()
# entrega o controle ao Poller
sched.despache()