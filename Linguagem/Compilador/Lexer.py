def lerCodigo(nomeArquivo):
    with open(nomeArquivo) as arquivo:
        conteudo = arquivo.readlines()
        
        linhas_processadas = []
        for linha in conteudo:
            linha = linha.strip()
            if linha != "":
                simbolos = ["(", ")", "+", "-", "*", "/", "="]
                for simbolo in simbolos:
                    linha = linha.replace(simbolo, f" {simbolo} ")
                
                linhas_processadas.append(linha.split())
                
    return linhas_processadas


if __name__ == "__main__":
    print(lerCodigo(".\Compilador\Codigos\ArquivosBrutos\snake.txt"))