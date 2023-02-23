import csv

# -- Importação das classe necessarias -- #
from classes.Automato import Automato
from classes.AFD import AFD
from classes.Dead import Dead
from classes.Error import Error

# Função responsavel por pegar um mapeamento de Estados e transforma-lo em uma matriz para a escrita de um CSV
def toTransform(automato):
    matriz = []
    lista = [''] + automato.Token
    matriz.append(lista) # Gera a primeira linha da matriz com os tokens 

    for name, transicao in automato.State.items(): # Passa por cada item do estado
        
        if name in list(automato.EndState):
            name = '*' + name
            vetor = ['-'] * (len(automato.Token) + 1)
        else:
            vetor = [''] * (len(automato.Token) + 1)
        
        vetor[0] = name 
        
        for token, producao in transicao.items(): # Passa por cada item da transição
            for prod in producao:
                if vetor[matriz[0].index(token)] != '' and vetor[matriz[0].index(token)] != '-':
                    vetor[matriz[0].index(token)] = vetor[matriz[0].index(token)] + ',' + prod
                else:
                    vetor[matriz[0].index(token)] = prod
        
        matriz.append(vetor)

    return matriz

# Função responsavel por escrevever em um arquivo .CSV a matriz editada
def write(arquivo,nomeDoAutomato):
    with open(nomeDoAutomato, 'w', newline='') as file:
        writer = csv.writer(file)
        for lista in arquivo:
            writer.writerow(lista)

# Abre o arquivo de entrada
#nameFile = input("Digite o nome do arquivo de entrada(.extensão caso tenha): ")
nameFile = 'teste.txt'
arquivo = open(nameFile, 'r')                    
entrada = arquivo.read()

# Gera o AFND
Automato = Automato()
Automato.read(entrada)
write(toTransform(Automato),"Arquivos_CSV/AFND.csv")

# Gera o AFD
AFD = AFD(Automato)
AFD.read()
write(toTransform(Automato),"Arquivos_CSV/AFD.csv")

# Gera o arquivo minimizado
Automato.State = Automato.NewState.copy()

''' # Imprime o automato sem os estados inalcançável
#write(toTransform(Automato),"Arquivos_CSV/Minimize.csv")
'''

# Retira os estados mortos
Dead = Dead(Automato)
Dead.read('S') # Passando estado inicial para a classe
write(toTransform(Dead),"Arquivos_CSV/Minimize.csv")

# Adiciona estado de Error nas transições inexistentes
Error = Error(Dead)
Error.read()
write(toTransform(Dead),'Arquivos_CSV/ErrorState.csv')