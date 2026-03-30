from .IO import *
from .Lexer import lerCodigo

def compilar(codigoAltoNivel, finalRam=49151):
    assembly = []
    ponteiroRam = finalRam
    variaveis = {} #NomeVariavel : Endereço
    contadores = {"mult": 0, "div": 0, "if": 0, "while": 0} #Conseguir numerar as labels
    pilhaBlocos = [] #Salvar a label do if
    
    for linha in codigoAltoNivel:
        if "var" in linha[0]:
            variaveis[linha[1]] = ponteiroRam
            assembly.extend(compilarMatematica(linha[3:], variaveis, contadores, ponteiroRam))
            assembly.append(f"STR r0 {ponteiroRam}")            
            ponteiroRam -= 1

        elif linha[0] in variaveis and "=" in linha:
            assembly.extend(compilarMatematica(linha[2:], variaveis, contadores, ponteiroRam))
            assembly.append(f"STR r0 {variaveis[linha[0]]}")
            
        elif linha[0] == "if":  
            labelFimCompleto = f"FIM_BLOCO_IF_{contadores['if']}"
            proxCondicao = f"PROX_CONDICAO_{contadores['if']}_0"
            dictCorrente = {"tipo": "if",
            "fimTotal": labelFimCompleto,
            "proximo": proxCondicao,
            "idIf": contadores['if'],
            "elo": 0}
            pilhaBlocos.append(dictCorrente)     
            assembly.extend(compilarIF(linha, variaveis, contadores, ponteiroRam, proxCondicao, labelFimCompleto))
            contadores["if"] += 1
            
        elif linha[0] == "}" and "elif" in linha:
            topo = pilhaBlocos[-1]
            assembly.append(f"JMP {topo['fimTotal']}")
            assembly.append(f"{topo['proximo']}:")
            topo["elo"] += 1
            proxCondicao = f"PROX_CONDICAO_{topo['idIf']}_{topo['elo']}"
            topo["proximo"] = proxCondicao
            novaLinha = linha[1:]
            novaLinha[0] = "if"
            assembly.extend(compilarIF(novaLinha, variaveis, contadores, ponteiroRam, proxCondicao, topo["fimTotal"]))

        elif linha[0] == "}" and "else" in linha:
            topo = pilhaBlocos[-1]
            assembly.append(f"JMP {topo['fimTotal']}")
            assembly.append(f"{topo['proximo']}:")
            topo["proximo"] = ""

        elif linha[0] == "while":
            labelInicio = f"INICIO_WHILE_{contadores['while']}"
            labelFim = f"FIM_WHILE_{contadores['while']}"
            assembly.append(f"{labelInicio}:")
            dictWhile = {"tipo": "while", "inicio": labelInicio, "fim": labelFim}
            pilhaBlocos.append(dictWhile)
            assembly.extend(compilarIF(linha, variaveis, contadores, ponteiroRam, labelFim, labelFim))
            contadores["while"] += 1

        elif linha[0] == "}":
            labelAtual = pilhaBlocos.pop()
            if labelAtual["tipo"] == "while":
                assembly.append(f"JMP {labelAtual['inicio']}")
                assembly.append(f"{labelAtual['fim']}:")
            elif labelAtual["tipo"] == "if":
                if labelAtual['proximo'] != "":
                    assembly.append(f"{labelAtual['proximo']}:")
                assembly.append(f"{labelAtual['fimTotal']}:")


    return assembly

# Lidar com matematica
def compilarMatematica(linha, variaveis, contadores, ponteiroRam):
    if not linha:
        return ["LDI r0 0"]
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
    
# Lidar com if/else
def compilarIF(linha, variaveis, contadores, ponteiroRam, proxCondicao, final):
    codigoFinal = []
    labelEntra = f"ENTRA_IF_{contadores['if']}"
    labelFim = proxCondicao

    linha = linha[1:-1]
    comparadores = ["==", "!=", ">=", "<=" ,">", "<"]
    curComparador = ""
    for comparador in comparadores:
        try:
            posicao = linha.index(comparador)
            esquerda = linha[:posicao]
            direita = linha[posicao + 1:]
            curComparador = comparador
            break
        except ValueError:
            pass

    rEsquerda = compilarMatematica(esquerda, variaveis, contadores, ponteiroRam)
    rDireita = compilarMatematica(direita, variaveis, contadores, ponteiroRam - 1)
    codigoFinal.extend(rEsquerda)
    codigoFinal.append(f"STR r0 {ponteiroRam}") # Esquerda
    codigoFinal.extend(rDireita)
    codigoFinal.append(f"LDR r1 {ponteiroRam}")
    
    match curComparador:
        case "==":
            codigoFinal.append("CMP r1 r0")
            codigoFinal.append(f"JEQ {labelEntra}")
            codigoFinal.append(f"JMP {labelFim}")
            codigoFinal.append(f"{labelEntra}:")
        case "!=":
            codigoFinal.append("CMP r1 r0")
            codigoFinal.append(f"JEQ {labelFim}")
        case ">":
            codigoFinal.append("CMP r1 r0")
            codigoFinal.append(f"JGT {labelEntra}")
            codigoFinal.append(f"JMP {labelFim}")
            codigoFinal.append(f"{labelEntra}:")
        case "<":
            codigoFinal.append("CMP r0 r1")
            codigoFinal.append(f"JGT {labelEntra}")
            codigoFinal.append(f"JMP {labelFim}")
            codigoFinal.append(f"{labelEntra}:")
        case ">=":
            codigoFinal.append("CMP r1 r0")
            codigoFinal.append(f"JGT {labelEntra}")
            codigoFinal.append(f"JEQ {labelEntra}")
            codigoFinal.append(f"JMP {labelFim}")
            codigoFinal.append(f"{labelEntra}:")
        case "<=":
            codigoFinal.append("CMP r0 r1")
            codigoFinal.append(f"JGT {labelEntra}")
            codigoFinal.append(f"JEQ {labelEntra}")
            codigoFinal.append(f"JMP {labelFim}")
            codigoFinal.append(f"{labelEntra}:")
    return codigoFinal
        


if __name__ == "__main__":
    assembly = compilar(lerCodigo("./Linguagem/teste.txt"))
    for instrução in assembly:
        print(instrução)