# Computador 16 BITS

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
# Criadores

- [Guilherme Augusto](https://github.com/gui200428/)
    - *{O que fez}*
- [João Francisco](https://github.com/JFScripts)
    - *{O que fez}*
---