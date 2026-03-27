from Compilador.IO import *
from Compilador.Tradutor import compilar
from Compilador.Lexer import lerCodigo
import tkinter as tk
from tkinter import messagebox

def main():
    init()
    pastaDeCodigo = "./Compilador/Codigos/AltoNivel"
    pastaDeBinario = "./Linguagem/Codigos/Binario"
    curPrograma = input("Digite o programa que você quer abrir:\n")

    if not verificarDiretorio(f"{pastaDeCodigo}/{curPrograma}.txt"):
        criarTxt(pastaDeCodigo, curPrograma)
        abrirArquivo(pastaDeCodigo + "/" +curPrograma + ".txt")
        print(f"\nPrograma não existe\nEle foi criado em {pastaDeCodigo}")
        return
    codigoLido = lerCodigo(f"{pastaDeCodigo}/{curPrograma}.txt")
    codigoAssembly = compilar(codigoLido)
    codigoBinario = traduzirCodigo(codigoAssembly)
    criarBinario(pastaDeBinario, curPrograma, codigoBinario)
    root = tk.Tk()
    root.withdraw()
    mensagem = f"Pode Ser Encontrado em:\n{pastaDeBinario}/{curPrograma}/{curPrograma}.bin"
    messagebox.showinfo("Programa Compilado Com Sucesso!",mensagem)

def init():
    caminhosObrigatorios = ["./Linguagem/Codigos/Binario",
    "./Linguagem/Codigos/ProgramasBrutos",
    "./Linguagem/Codigos/AltoNivel"]

    criarPastasObrigatorias(caminhosObrigatorios)

if __name__ == "__main__":
    main()
