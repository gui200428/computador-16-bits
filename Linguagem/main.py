from Compilador.IO import *
from Compilador.Tradutor import compilar
from Compilador.Lexer import lerCodigo
from Compilador.Parser import traduzirCodigo
import tkinter as tk
from tkinter import messagebox

DIRETORIO_ATUAL = Path(__file__).parent

WORKSPACE = DIRETORIO_ATUAL / "Workspace"
PASTA_SRC = WORKSPACE / "src"
PASTA_BUILD = WORKSPACE / "build"

def main():
    init()
    url = "https://github.com/JFScripts"
    nomeClicavel = f"\033]8;;{url}\aJoão Francisco\033]8;;\a"
    print("==================================================")
    print(f"= COMPILADOR 16 BITS ~ FEITO POR: {nomeClicavel} =")
    print("==================================================")

    curPrograma = input("Digite o programa que você quer abrir/criar:\n> ")
    arquivoCodigo = PASTA_SRC / f"{curPrograma}.txt"
    
    if not verificarDiretorio(arquivoCodigo):
        criarTxt(PASTA_SRC, curPrograma)
        abrirArquivo(arquivoCodigo)
        print(f"\n[!] O programa [{curPrograma}] não existia.")
        print(f"[+] Um novo arquivo foi criado em: {PASTA_SRC}")
        print(f"> Escreva seu código, salve o arquivo e rode o compilador novamente")
        return

    pastaDestino = PASTA_BUILD / curPrograma

    codigoLido = lerCodigo(str(arquivoCodigo))
    codigoAssembly = compilar(codigoLido)
    codigoBinario = traduzirCodigo(codigoAssembly)
    criarBinario(pastaDestino, curPrograma, codigoBinario)
    criarTxt(pastaDestino, curPrograma, codigoBinario)
    
    root = tk.Tk()
    root.withdraw()
    mensagem = f"Compilação concluída!\n\nOs arquivos compilados estão na pasta:\n{pastaDestino}"    
    messagebox.showinfo("Sucesso!", mensagem)

def init():
    caminhosObrigatorios = [PASTA_SRC, PASTA_BUILD]
    criarPastasObrigatorias(caminhosObrigatorios)

if __name__ == "__main__":
    main()
