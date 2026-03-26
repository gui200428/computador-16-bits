def lerCodigo(nomeArquivo):
    with open(nomeArquivo) as arquivo:
        conteudo = arquivo.readlines()
        conteudo = [linha.strip().split() for linha in conteudo if linha.strip() != ""]
    return conteudo


if __name__ == "__main__":
    print(lerCodigo(".\Compilador\Codigos\ArquivosBrutos\snake.txt"))