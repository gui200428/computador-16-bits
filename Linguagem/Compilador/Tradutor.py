from IO import *
from Lexer import lerCodigo

def compilar(codigoAltoNivel, finalRam=49151):
    assembly = []
    ponteiroRam = finalRam
    variaveis = {} #NomeVariavel : Endereço
    contadores = {"mult" : 0, "div" : 0}
    
    for linha in codigoAltoNivel:
        if "var" in linha[0]:
            assembly.extend(compilarVariavel(linha, ponteiroRam, variaveis))
            ponteiroRam -= 1
        elif linha[0] in variaveis and "=" in linha:
            if len(linha) >= 5:
                assembly.extend(compilarMatematica(linha[2:], variaveis, contadores, ponteiroRam))
                assembly.append(f"STR r0 {variaveis[linha[0]]}")
    return assembly

# Lidar com Variaveis
def compilarVariavel(linha, ponteiroRam, variaveis):
    # As variaveis sempre são sempre colocadas em R0 primeiro
        variaveis[linha[1]] = ponteiroRam
        return [f"LDI r0 {linha[3]}",f"STR r0 {ponteiroRam}"]

# Lidar com matematica

def compilarMatematica(linha, variaveis, contadores, ponteiroRam):
    if len(linha) == 1:
        ultimoValor = linha[0]
        if ultimoValor in variaveis:
            return [f"LDR r0 {variaveis[linha[0]]}"]
        else:
            return [f"LDI r0 {linha[0]}"]
    elif "(" == linha[0] and ")" == linha[-1]:
            linhaInterna = linha[1:-1]
            return compilarMatematica(linhaInterna, variaveis, contadores, ponteiroRam)
    else:
        parenteses = 0
        corte = -1
        for i in range(len(linha) - 1, -1, -1):
            caracter = linha[i]
            if caracter == ")":
                parenteses += 1
            elif caracter == "(":
                parenteses -= 1
            elif (caracter == "+" or caracter == "-") and parenteses == 0:
                corte = i
                break
        if corte < 0:
            parenteses = 0
            for i in range(len(linha) - 1, -1, -1):
                caracter = linha[i]
                if caracter == ")":
                    parenteses += 1
                elif caracter == "(":
                    parenteses -= 1
                elif (caracter == "*" or caracter == "/") and parenteses == 0:
                    corte = i
                    break
        operador = linha[corte]
        contaEsquerda = linha[:corte]
        contaDireita = linha[corte+1:]

        codigoFinal = compilarMatematica(contaEsquerda, variaveis, contadores, ponteiroRam)
        codigoFinal.append(f"STR r0 {ponteiroRam}")
        codigoFinal.extend(compilarMatematica(contaDireita, variaveis, contadores, ponteiroRam-1))
        codigoFinal.append(f"STR r0 {ponteiroRam-1}")
        
        if operador == "+":
            codigoFinal.extend(soma(ponteiroRam))
        elif operador == "-":
            codigoFinal.extend(subtracao(ponteiroRam))
        elif operador == "*":
            codigoFinal.extend(multiplicacao(ponteiroRam, contadores))
        else:
            codigoFinal.extend(divisao(ponteiroRam, contadores))
    return codigoFinal
        
def soma(ponteiroRam):
    codigoSoma = [f"LDR r0 {ponteiroRam}"]
    codigoSoma.append(f"LDR r1 {ponteiroRam - 1}")
    codigoSoma.append(f"SUM r0 r1")
    return codigoSoma

def subtracao(ponteiroRam):
    codigoSub = [f"LDR r0 {ponteiroRam}"]
    codigoSub.append(f"LDR r1 {ponteiroRam - 1}")
    codigoSub.append(f"SUB r0 r1")
    return codigoSub

def multiplicacao(ponteiroRam, contadores):
    inicioLoop = f"MULT_LOOP_{contadores['mult']}"
    finalLoop = f"MULT_FIM_{contadores['mult']}"
    
    codigoMult = ["LDI r0 0"]
    codigoMult.append(f"LDR r1 {ponteiroRam}")
    codigoMult.append(f"LDR r2 {ponteiroRam - 1}")
    codigoMult.append(f"{inicioLoop}:")
    codigoMult.append("CMP r2 0")
    codigoMult.append(f"JEQ {finalLoop}")
    
    codigoMult.append(f"SUM r0 r1")
    codigoMult.append("SUB r2 1")
    codigoMult.append(f"JMP {inicioLoop}")
    
    codigoMult.append(f"{finalLoop}:")
    contadores["mult"] += 1
    return codigoMult

def divisao(ponteiroRam, contadores):
    inicioLoop = f"DIV_LOOP_{contadores['div']}" 
    fimLoop = f"DIV_FIM_{contadores['div']}" 


    codigoDiv = ["LDI r0 0"]
    codigoDiv.append(f"LDR r1 {ponteiroRam}")
    codigoDiv.append(f"LDR r2 {ponteiroRam - 1}")
    codigoDiv.append(f"{inicioLoop}:")
    codigoDiv.append(f"CMP r2 r1")
    codigoDiv.append(f"JGT {fimLoop}")
    codigoDiv.append(f"SUB r1 r2")
    codigoDiv.append(f"SUM r0 1")
    codigoDiv.append(f"JMP {inicioLoop}")
    codigoDiv.append(f"{fimLoop}:")

    contadores["div"] += 1
    return codigoDiv
    


if __name__ == "__main__":
    print(compilar(lerCodigo("./Linguagem/teste.txt")))