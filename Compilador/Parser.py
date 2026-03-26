from Lexer import lerCodigo

def traduzirCodigo(caminhoArquivo):
    comandos = {
        "NOP" : "0000", #Não Faz Nada
        "LDI" : "0001", #	Carrega o numero no registrador
        "LDR" : "0010", # Lê o dado da memória ram e passa pro registrador
        "STR":"0011", # Grava os dados do registrador na ram
        "SUM" : "0100", # Soma dois registradores
        "SUB" : "0101", # Subtrai dois registradores
        "AND" : "0110", # And dois registradores
        "ORR" : "0111", # Or dois registradores
        "XOR" : "1000", # XOr dois registradores
        "SHL" : "1001", # Desloca os BITs para a ESQUERDA
        "SHR" : "1010", # Desloca os BITs para a DIREITA
        "CMP" : "1011", # Compara dois valores e atualiza as flags
        "JMP" : "1100", # Pulo INCONDICIONAL
        "JEQ" : "1101", # Pula se IGUAL
        "JGT" : "1110", # Pula se MAIOR
        "HLT" : "1111" # Para o clock e encerra o programa
    }

    comandosEspeciais = ["LDR", "STR"]

    registradores = {
        "r0":"00",
        "r1":"01",
        "r2":"10",
        "r3":"11",
    }

    codigoTraduzido = []
    codigo = lerCodigo(caminhoArquivo)
    for linha in codigo:
        curPalavra = linha[0]
        if curPalavra in comandos:
            valorComando = int(comandos[curPalavra], 2) << 12
            rx = ry = 0
            endereco = None
            if len(linha) >= 2:
                rx = int(registradores[linha[1]], 2) << 10
            if len(linha) == 3:
                if linha[2] in registradores:
                    ry = int(registradores[linha[2]], 2) << 8
                elif curPalavra in comandosEspeciais:
                    endereco = int(linha[2]) & 0b1111111111111111
                else: 
                    ry = int(linha[2]) & 0b1111111111
            valorComando = valorComando | rx | ry
            codigoTraduzido.append(valorComando)
            if endereco != None:
                codigoTraduzido.append(endereco)
    return codigoTraduzido



if __name__ == "__main__":
    traduzirCodigo(".\Compilador\Codigos\ArquivosBrutos\snake.txt")
  