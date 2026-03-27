from pathlib import Path
import subprocess
import os
import sys

def criarDiretorio(caminho):
    diretorio = Path(caminho)
    diretorio.mkdir(parents=True, exist_ok=True)

def criarPastasObrigatorias(pastas):
    for pasta in pastas:
        criarDiretorio(pasta)

def criarBinario(caminho, nome, dados=None, qntBytes=2):
    criarDiretorio(caminho)
    endereco = caminho + "/" +nome + ".bin"
    if dados == None:
        with open(endereco, "wb") as arquivo:
            pass
        return
    with open(endereco, "wb") as arquivo:
        for linhas in dados:
            arquivo.write(linhas.to_bytes(qntBytes, byteorder="big"))

def criarTxt(caminho, nome, dados=None):
    criarDiretorio(caminho)
    endereco = caminho + "/" + nome + ".txt"
    if dados == None:
        with open(endereco, "w") as arquivo:
            pass
        return
    with open(endereco, "w") as arquivo:
        for linhas in dados:
            arquivo.write(f"{linhas:016b}\n")

def verificarDiretorio(diretorio):
    return Path(diretorio).is_file()

def abrirArquivo(diretorio):
    caminho_absoluto = Path(diretorio).resolve()
    diretorioSTR = str(caminho_absoluto)
    editores = ["code", "codium"]

    for editor in editores:
        try:
            subprocess.run(f'{editor} "{diretorioSTR}"', shell=True, check=True)
            return 
        except subprocess.CalledProcessError:
            continue 
    try:
        if sys.platform == "win32":
            os.startfile(diretorioSTR)
        elif sys.platform == "darwin":
            subprocess.run(f'open "{diretorioSTR}"', shell=True, check=True)
        else:
            subprocess.run(f'xdg-open "{diretorioSTR}"', shell=True, check=True)
            
    except Exception as erro:
        print(f"Aviso: Não consegui abrir o editor de texto automaticamente. ({erro})")