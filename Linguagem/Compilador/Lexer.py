def lerCodigo(nomeArquivo):
    with open(nomeArquivo) as arquivo:
        conteudo = arquivo.readlines()
        
        linhas_processadas = []
        for linha in conteudo:
            linha = linha.strip()
            if linha != "":
                linha = linha.replace("==", " IGUAL_DUPLO ")
                linha = linha.replace(">=", " MAIOR_IGUAL ")
                linha = linha.replace("<=", " MENOR_IGUAL ")
                simbolos = ["(", ")", "+", "-", "*", "/", "=", "{" , "}", ">", "<"]
                for simbolo in simbolos:
                    linha = linha.replace(simbolo, f" {simbolo} ")
                linha = linha.replace(" IGUAL_DUPLO ", "==")
                linha = linha.replace(" MAIOR_IGUAL ", ">=")
                linha = linha.replace(" MENOR_IGUAL ", "<=")
                linhas_processadas.append(linha.split())
                
    return linhas_processadas


if __name__ == "__main__":
    print(lerCodigo(".\Compilador\Codigos\ArquivosBrutos\snake.txt"))