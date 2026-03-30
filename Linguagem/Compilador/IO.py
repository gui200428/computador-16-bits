from pathlib import Path
import subprocess
import os
import sys

def criarPastasObrigatorias(pastas):
    for pasta in pastas:
        pasta.mkdir(parents=True, exist_ok=True)

def criarBinario(pasta: Path, nome: str, dados=None, qntBytes=2):
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo_bin = pasta / f"{nome}.bin" 
    if dados is None:
        arquivo_bin.touch() 
        return
    with open(arquivo_bin, "wb") as arquivo:
        for linha in dados:
            arquivo.write(linha.to_bytes(qntBytes, byteorder="big"))

def criarTxt(pasta: Path, nome: str, dados=None):
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo_txt = pasta / f"{nome}.txt"
    if dados is None:
        arquivo_txt.touch()
        return
    with open(arquivo_txt, "w") as arquivo:
        for linha in dados:
            arquivo.write(f"{linha:016b}\n")

def verificarDiretorio(arquivo: Path):
    return arquivo.is_file()

def abrirArquivo(arquivo: Path):
    caminho_absoluto = str(arquivo.resolve())
    editores = ["code", "codium"]
    for editor in editores:
        try:
            subprocess.run(f'{editor} "{caminho_absoluto}"', shell=True, check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            return 
        except subprocess.CalledProcessError:
            continue 
            
    try:
        if sys.platform == "win32":
            os.startfile(caminho_absoluto)
        elif sys.platform == "darwin":
            subprocess.run(f'open "{caminho_absoluto}"', shell=True, check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        else:
            subprocess.run(f'xdg-open "{caminho_absoluto}"', shell=True, check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except Exception as erro:
        print(f"Aviso: Não consegui abrir o editor de texto automaticamente. ({erro})")