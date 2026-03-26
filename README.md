# Computador 16 BITS

## Objetivo do Projeto

O objetivo central do projeto é desenvolver um ecossistema computacional completo de 16 bits a partir do zero, desde a engenharia física do hardware até o desenvolvimento de software de alto nível. O escopo da construção é dividido em quatro pontos principais:

* **Arquitetura de Hardware Customizada:** Projetar e construir fisicamente o minicomputador (migrando para uma Placa de Circuito Impresso - PCB), definindo a lógica da Unidade Central de Processamento (CPU), barramentos e o mapeamento físico de memória (RAM e ROM).
* **Controlador de Vídeo Dedicado:** Desenvolver um periférico de vídeo em hardware (uma "GPU") para gerenciar o mapeamento e a renderização de gráficos em um monitor construído com matriz de LEDs, liberando a CPU principal do processamento de imagem.
* **Linguagem de Programação e Ferramentas:** Criar um conjunto de instruções (ISA) exclusivo e desenvolver as ferramentas de compilação necessárias para traduzir código lógico em linguagem de máquina nativa.
* **Sistema Operacional e Jogos:** Programar o sistema base para gerenciar o hardware, o espaço de memória e as rotinas de I/O, seguido do desenvolvimento e execução de jogos interativos rodando nativamente na plataforma.

## Regras
Podemos imaginar que temos os seguintes BITs

<span style="color:#A0C4FF">[00][01][02][03]</span><span style="color:#C0EBA6">[04][05]</span><span style="color:#FFB7B2">[06][07]</span><span style="color:#DDBDF1">[08][09][10][11][12][13][14][15]</span>

Dividimos eles em alguns grupos

### Instruções
Os BITs <span style="color:#A0C4FF">[00][01][02][03]</span> são os BITs de instruções seguindo a tabela verdade abaixo

|[00]|[01]|[02]|[03]|Comando|
|:---|:---|:---|:---|:---|
|0|0|0|0|Não Faz Nada|
|0|0|0|1|Carrega o numero no registrador|
|0|0|1|0|Lê o dado da memória ram e passa pro registrador|
|0|0|1|1|Grava os dados do registrador na ram|
|0|1|0|0|Soma dois registradores|
|0|1|0|1|Subtrai dois registradores|
|0|1|1|0|And dois registradores|
|0|1|1|1|Or dois registradores|
|1|0|0|0|XOr dois registradores|
|1|0|0|1|Desloca os BITs para a ESQUERDA|
|1|0|1|0|Desloca os BITs para a DIREITA|
|1|0|1|1|Compara dois valores e atualiza as flags|
|1|1|0|0|Pulo INCONDICIONAL|
|1|1|0|1|Pula se IGUAL|
|1|1|1|0|Pula se MAIOR|
|1|1|1|1|Para o clock e encerra o programa|

### Registradores
Os BITs <span style="color:#C0EBA6">[04][05]</span> são utilizados para dizer o endereço do primeiro grupo de registradores e os BITs <span style="color:#FFB7B2">[06][07]</span> do segundo grupo de registradores sendo:
- R0 = 00
- R1 = 01
- R2 = 10
- R3 = 11

Se quisermos escrever um comando que copia de um registrador para o outro podemos escrever assim:

(Os espaços é para facilitar a leitura)

1000 01 01 -> Aplicamos um XOr no proprio registrador para ele zerar

0100 01 10 -> Somamos o valor do registrador R2 com o R1 e salvamos em R1

Em comandos que utilizam apenas registradores sem precisar de um dado externo, os BITs restantes são ignorados pelo sistema

### Representação de Dados
Os BITs <span style="color:#FFB7B2">[06][07]</span><span style="color:#DDBDF1">[08][09][10][11][12][13][14][15]</span> representam os dados que conseguimos escrever e utilizando o método **Complemento de Dois** o BIT mais a esquerda representa o número negativo, que se ativado, tal numero é negativo.

Os BITs <span style="color:#FFB7B2">[06][07]</span> só serão utilizados como números quando o comando não for de fazer conta, chamamos isso de **Tipo II** assim permitindo números de **-512** até **+511** sem esses BITs podemos representar números de **-128** até **+127**

## Mapa de Memória

Nosso computador possui um barramento de endereços de 16 fios. Isso significa que ele consegue acessar $2^{16}$ posições de memória, totalizando **65.536 endereços** (64 KB).

Para organizar o sistema, dividimos esse espaço físico em três grandes "bairros":

* **ROM (32 KB):** Do endereço **0** ao **32.767**. 
    * É aqui que o código do jogo/programa fica gravado. A CPU sempre liga procurando a primeira instrução no endereço 0.
* **RAM (16 KB):** Do endereço **32.768** ao **49.151**. 
    * É o quadro branco. Onde guardamos as variáveis dinâmicas (ex: posição X do jogador, vida do monstro).
* **I/O e GPU (16 KB):** Do endereço **49.152** ao **65.535**. 
    * Mapeamento de Hardware. Se escrevermos um dado no endereço 50.000, ele não vai para uma memória, ele acende um pixel na tela

### Como a CPU acessa a memória sem confundir com Instruções?
Como nossas instruções têm 16 BITs, não sobra espaço na mesma linha para escrever um endereço inteiro de 65 mil. 

Para resolver isso, usamos o conceito de **Instrução de Palavra Dupla**. 
Quando usamos comandos de memória (**{A ser definido}**, **{A ser definido}**) ou pulos distantes (**{A ser definido}**), o compilador gera duas linhas seguidas:
1.  **Linha 1 (Instrução):** A CPU lê o OpCode e entende que o comando exige um endereço.
2.  **Linha 2 (Endereço):** A CPU lê os próximos 16 BITs inteiros como um endereço de memória puro (ignorando os formatos de OpCode ou Registrador).
---

# Documentação do Assembly (Arquitetura 16-bits) - Gerado Pelo Gemini (Revisar Depois)

Este é o manual de referência para o conjunto de instruções (ISA) do nosso processador customizado de 16-bits.

## 💾 Registradores Disponíveis
O processador possui 4 registradores de uso geral:
* `r0`, `r1`, `r2`, `r3`

---

## 🛠️ Conjunto de Instruções

### 1. Movimentação de Dados e Matemática (1 Palavra)
Instruções básicas que ocupam apenas 1 linha na memória.

* `NOP` : Não faz nada (No Operation).
* `LDI rx, valor` : Carrega um número direto (até 10 bits) no registrador. *(Ex: `LDI r0 5`)*
* `SUM rx, ry` : Soma o valor de `ry` com `rx` e salva em `rx`. *(Ex: `SUM r0 r1`)*
* `SUB rx, ry` : Subtrai `ry` de `rx`.
* `AND rx, ry` : Operação lógica AND bit a bit.
* `ORR rx, ry` : Operação lógica OR bit a bit.
* `XOR rx, ry` : Operação lógica XOR bit a bit.
* `SHL rx` : Desloca os bits de `rx` para a esquerda.
* `SHR rx` : Desloca os bits de `rx` para a direita.
* `CMP rx, ry` : Compara `rx` e `ry` e atualiza as flags do processador (usado antes de pulos condicionais).
* `HLT` : Para o clock e encerra a execução do programa.

### 2. Memória RAM (2 Palavras / Palavra Dupla)
Instruções que acessam a memória RAM. Exigem 2 linhas na ROM. O endereço pode ser um número de 16 bits ou uma Label.

* `LDR rx, endereco` : Lê um valor da RAM e salva no registrador `rx`. *(Ex: `LDR r1 1000`)*
* `STR rx, endereco` : Grava o valor do registrador `rx` na RAM. *(Ex: `STR r0 100`)*

### 3. Controle de Fluxo / Saltos (2 Palavras / Palavra Dupla)
Instruções que alteram o Program Counter (PC). O destino pode ser uma linha exata ou uma Label.

* `JMP destino` : Pulo incondicional. Vai para o destino sem perguntar nada. *(Ex: `JMP loop`)*
* `JEQ destino` : Pula apenas se a última comparação (`CMP`) deu IGUAL.
* `JGT destino` : Pula apenas se a última comparação (`CMP`) deu MAIOR.

---

## 🏷️ Labels (Marcadores)
As labels são usadas para marcar posições no código sem precisar decorar o número da linha na memória física. Elas não ocupam espaço na ROM compilada.

**Regras:**
1. Devem terminar obrigatoriamente com dois pontos `:`.
2. Ficam sozinhas na linha.

**Exemplo de uso:**
```assembly
LDI r0 0
LDI r1 1

inicio_loop:
SUM r0 r1
CMP r0 r1
JEQ fim
JMP inicio_loop

fim:
HLT

---
# Criadores

|                                           Avatar                                           | Nome                                                       | Contribuição |
| :----------------------------------------------------------------------------------------: | ---------------------------------------------------------- | ------------ |
| <img src="https://github.com/gui200428.png?size=80" width="80px" alt="Guilherme Augusto"/> | [Guilherme Augusto](https://github.com/gui200428)          | TODO         |
|  <img src="https://github.com/jfscripts.png?size=80" width="80px" alt="João Francisco"/>   | [João Francisco B. Ferreira](https://github.com/jfscripts) | TODO         |

---