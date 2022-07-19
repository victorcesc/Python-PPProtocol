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
# sessao.enable()
# sessao.enable_timeout()
# Conecta as subcamadas
# Deve ser feito a partir da subcamada inferior
# enq.conecta(app)
enq.conecta(arq)
arq.conecta(sessao)
sessao.conecta(app)
# cria o Poller e registra os callbacks
sched = poller.Poller()

sched.adiciona(enq)
sched.adiciona(app)

if len(sys.argv) > 2:

    if sys.argv[2] or sys.argv[3] == '--debug':
        app.debug = True
        sessao.debug = True
        arq.debug = True
        enq.debug = True

    if sys.argv[2] == '--master':
        sessao.master = 1
        if sys.argv[2] == '--idSessao':
            app.START(int(sys.argv[3]));
        elif sys.argv[3] == '--idSessao':
            app.START(int(sys.argv[4]));
        elif sys.argv[4] == '--idSessao':
            app.START(int(sys.argv[5]));
        elif sys.argv[5] == '--idSessao':
            app.START(int(sys.argv[6]));
        else:
            app.START(0)

# sched.adiciona(arq)
# enq.enable()
# enq.enable_timeout()
# entrega o controle ao Poller

try:
    sched.despache()
except:
    sys.exit()