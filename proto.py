import enq
import adapt
import poller
## exemplo da uniao das camadas do protocolo

framing = enq.Enquadramento(Serial('/dev/pts/1',9600),1)

terminal = adapt.Adaptacao()

framing.conecta(terminal)

#exemplo de conexao de duas subcamadas

sched = poller.Poller()
sched.adiciona(framing)
sched.adiciona(terminal)

#eventos de recepcao e envio somente as camadas de cima e de baixo

# as camadas do meio serao eventos de timeout
sched.despache()
