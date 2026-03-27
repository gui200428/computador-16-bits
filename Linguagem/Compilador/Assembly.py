from Parser import traduzirCodigo
from IO import *

def assembly():
    pastaDeCodigo = "./Compilador/Codigos/ProgramasBrutos"
    pastaCompilada = "./Compilador/Codigos/Compilados"
    criarDiretorio(pastaDeCodigo)
    criarDiretorio(pastaCompilada)

    curPrograma = input("Digite o programa que você quer abrir:\n")
    if not verificarDiretorio(f"{pastaDeCodigo}/{curPrograma}.txt"):
        criarTxt(pastaDeCodigo, curPrograma)
        abrirArquivo(pastaDeCodigo + "/" +curPrograma + ".txt")
        print(f"\nPrograma não existe\nEle foi criado em {pastaDeCodigo}")
        return
    codigoNaoCompilado = pastaDeCodigo + "/" + curPrograma + ".txt"
    programa = traduzirCodigo(codigoNaoCompilado)
    criarBinario(pastaCompilada + f"/{curPrograma}", curPrograma, programa)
    criarTxt(pastaCompilada + f"/{curPrograma}", curPrograma, programa)
    print("Programa Compilado")
    abrirArquivo(pastaCompilada + f"/{curPrograma}/{curPrograma}.txt")
    

if __name__ == "__main__":
    assembly()