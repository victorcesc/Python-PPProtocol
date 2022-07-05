[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7891775&assignment_repo_type=AssignmentRepo)
# Projeto 2 - Protocolo de enlace

### Um protocolo de enlace ponto-a-ponto

## Descrição do PPP

Nosso projeto foi baseado no protocolo PPP (point-to-point protocol) que nada mais é que uma conexão direta entre dois nós. Ele pode fornecer autênticação de conexão, criptografia de transmissão e compressão.

É usado sobre muitos tipos de redes físicas incluindo cabo serial, linha telefônica, linha tronco, telefone celular, enlaces de rádio especializados e enlaces de fibra ótica como SONET. O PPP também é usado sobre conexões de acesso à Internet. Provedores de serviços de Internet têm usado o PPP para acesso discado à Internet pelos clientes, uma vez que pacotes IP não podem ser transmitidos sobre uma linha de modem por si próprios, sem algum protocolo de enlace de dados.

Há dois derivados do PPP, o Point-to-Point Protocol over Ethernet (PPPoE), em português protocolo ponto a ponto sobre Ethernet, e Point-to-Point Protocol over ATM (PPPoA), em português Protocolo ponto a ponto sobre ATM, que são usados mais comumente por Provedores de Serviços de Internet para estabelecer uma conexão de serviços de Internet de Linha Digital de Assinante (ou DSL) com seus clientes.

##  Projeto

Nosso protocolo se comunica através de um link utilizando portas seriais emuladas com o [Serialemu](https://github.com/IFSCEngtelecomPTC/Serialemu). O projeto se divide em algumas subcamadas como: enquadramento, arq, sessão, aplicação

### Enquadramento

É responsável por delimitar o quadro, utilizando a técnica do tipo sentinela com uma flag de valor 7E como delimitador do quadro, um byte de escape 7D para preenchimento de octeto. O transimissor faz o escape dos bytes 7E e 7D modificando por meio de um XOR 20. Podemos ver melhor o funcionamento através da máquina de estados a seguir:

![](ppp_mef.png)

### Arq



Máquina de estado
![](mef_arq.png)

### Sessão

Máquina de estado do iniciador de conexão
![](iniciador_conexao.png)

Máquina de estado do receptor de conexão
![](receptor_conexao.png)