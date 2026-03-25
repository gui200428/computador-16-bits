def main():
    comandos = {
        "wait" : "0000", #Não Faz Nada
        "lregister" : "0001", #	Carrega o numero no registrador
        "loadramregister" : "0010", # Lê o dado da memória ram e passa pro registrador
        "sregister":"0011", # Grava os dados do registrador na ram
        "sumregister" : "0100", # Soma dois registradores
        "subregister" : "0101", # Subtrai dois registradores
        "andregister" : "0110", # And dois registradores
        "orregister" : "0111", # Or dois registradores
        "xorregister" : "1000", # XOr dois registradores
        "lshift" : "1001", # Desloca os BITs para a ESQUERDA
        "rshift" : "1010", # Desloca os BITs para a DIREITA
        "compare" : "1011", # Compara dois valores e atualiza as flags
        "ijump" : "1100", # Pulo INCONDICIONAL
        "ejump" : "1101", # Pula se IGUAL
        "bjump" : "1110", # Pula se MAIOR
        "end" : "1111" # Para o clock e encerra o programa
    }

    #comando = input("Digite um comando\n")
    #if comando in comandos:
    #    binario = comandos[comando]
    #    print(binario)
    #else:
    #    print("Comando não existe")
    novoPrograma = input("Digite o programa que deseja compilar\n")
    programa = lerArquivo(novoPrograma)
    if programa == None:
        print("Arquivo não existia, ele foi criado, digite o código nele")
    else:
        codigoBinario = []
        for linha in programa:
            for comando in comandos:
                if comando in linha:
                    codigoBinario.append(comandos[comando])
        escreverArquivo(novoPrograma, codigoBinario)       
    salvarBinarioEmTxt(novoPrograma)
        


def lerArquivo(nomeArquivo):
    caminho = "./Compilador/" + nomeArquivo + ".txt"
    try:
        arquivo = open(caminho, "x")
        arquivo.close()
        return
    except FileExistsError:
        with open(caminho, "r") as arquivo:
            conteudo = arquivo.readlines()
            conteudo = [linha.strip() for linha in conteudo if linha.strip() != ""]
        return conteudo

def escreverArquivo(nomeArquivo, conteudo):
    caminho = "./Compilador/CodigoCompilado/" + nomeArquivo + ".bin"
    conteudoFormatado = converterDecimal(conteudo)

    with open(caminho, "wb") as arquivo:
        for linhas in conteudoFormatado:
            linhaDeslocado = linhas << 12
            arquivo.write(linhaDeslocado.to_bytes(2, byteorder="big"))

def converterDecimal(conteudo):
    listaBinario = []
    for linha in conteudo:
        listaBinario.append(int(linha, 2))
    return listaBinario

def salvarBinarioEmTxt(nomeArquivo):
    caminho_binario = "./Compilador/CodigoCompilado/" + nomeArquivo + ".bin"
    caminho_txt = "./Compilador/CodigoCompilado" + nomeArquivo + "_bits.txt"
    with open(caminho_binario, "rb") as arquivo_binario, open(caminho_txt, "w") as arquivo_txt:
        while True:
            curByte = arquivo_binario.read(2)
            if not curByte:
                break
            numero = int.from_bytes(curByte, byteorder="big")
            linhaBits = f"{numero:016b}\n"
            arquivo_txt.write(linhaBits)
        

if __name__ == "__main__":
    main()