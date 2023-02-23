import re

class Automato:

    def __init__(self):
        # -- Declaração de variaveis -- #
        self.State = dict() # Dicionario de todos os estados
        self.LastName = str('') # Ultimo nome usado para a produção
        self.EndState = set() # Conjunto de todos os estados finais
        self.Token = [] # Cria um conjunto de todos os simbolos 

        self.NewState = dict() # Cria um novo estado no qual será armazanado o automato minimizado

        self.Epsilon = '?' # Simbolo de epsilon

    def nameGenerator(self): # Função responsavel por criar um novo estado
        
        # Verifica se o ultimo estado criado ainda não foi usado
        if self.LastName == '':
            self.LastName = 'A'

        # Caso não, será comparado o tamanho e tomado a devida providencia em relação
        else:
            size = len(self.LastName)

            # Se a ultima letra do nome do estado é Z então ele verifica se há outras letras para atualizar
            if self.LastName[-1] == 'Z':
                occorrences = re.findall('[A-Y]',self.LastName) # Verifica se há outras letras para atualizar
                if occorrences == []: # Se não há letras para atualizar ele cria outra sequencia de char
                    self.LastName = 'A' * (size + 1)
                else: # Se tiver, ele verifica qual letra deve-se atualizar e a troca 
                    indexOccorrence = self.LastName.rfind(occorrences[-1])
                    lastName = list(self.LastName)
                    
                    # Troca a ultima letra que não é Z 
                    lastName[indexOccorrence] = chr(ord(occorrences[-1]) + 1)
                    # Cria uma nova lista A com a quantidade de letras depois da letra atualizada
                    restart = ['A'] * (len(lastName) - (indexOccorrence + 1))
                    # Junta a sequencia acima com a lastName do index 0 até ultima letra trocada 
                    lastName = lastName[:indexOccorrence + 1] + restart
                    self.LastName = ''.join(lastName) 
            
            # Se a ultima letra não for Z então só atualiza a ultima letra
            else:
                self.LastName = self.LastName[:-1] + chr(ord(self.LastName[-1]) + 1)
        
        if self.LastName == 'S':
            self.LastName = 'T'
        
        return self.LastName 
    
    def readGrammar(self,gramatica):
        productionRelation = dict()
        productionName = ''

        # SubFunção responsavel por adicionar uma nva produção para os estados e mapeala para saber qual produção antiga re enraiza com ela
        def adicionaNovaProdução(self,token):

            if token == 'S':
                
                if 'Epsilon' in productionRelation: # Verifica se há epsilon transição dentro das relações de produções e salva
                    ep = productionRelation['Epsilon']
                    productionRelation.clear()
                    productionRelation['Epsilon'] = ep
                else:
                    productionRelation.clear()

                productionRelation.update({'S': 'S'})
                
            else:
                productionRelation.update({token: self.nameGenerator()})
                self.State.update({self.LastName: {}})
            
        # SubFunção responsavel por pegar um token e uma produção e verificar se ambas estao dentro dos estados e se não cria-los
        def adicionaNovaTransição(self,token,production):
            if token not in self.Token:
                self.Token.append(token)
        
            if production not in productionRelation:
                adicionaNovaProdução(self,production)
            
            # Caso exista ja o token que esta em uso é inserido mais uma produção na lista
            if token in self.State[productionName]:
                self.State[productionName][token].append(productionRelation[production])
            
            # Caso o token não exista então é só inserido
            else: 
                self.State[productionName].update({token: [productionRelation[production]]})
            

        # -- Leitura e verificação dos tokens e produções -- #
        ignore = [' ', ':']
        
        for production in gramatica: # Passa por cada produção da lista de gramtica
            
            token = '' # Inicia uma palavra valida

            for index in range(len(production)): # Passa por cada letra de uma produção
                
                if production[index] in ignore: # Ignora os characteres listados acima
                    continue

                token += production[index] # Adiciona cada character para a palavra
            
                if re.match('<\S>',token) is not None: # Se for sinal de uma nova transição
                    if token[1] not in productionRelation or token[1] == 'S':
                        adicionaNovaProdução(self,token[1])
                    productionName = productionRelation[token[1]]
                    token = ''
                    
                elif re.match('\|\S<\S>',token) is not None or re.match('=\S<\S>', token) is not None: # Se for uma transição com token
                    adicionaNovaTransição(self,token[1],token[3])
                    token = ''
                
                elif (token == '|' + self.Epsilon) or (token == '=' + self.Epsilon): # Se for uma transição final
                    self.EndState.add(productionName)
                    token = ''
                
                elif (re.match('\|\S',token) is not None and index == len(production) -1 or 
                        re.match('=\S',token) is not None and index == len(production) -1 or 
                        re.match('\|\S\|',token) is not None or re.match('=\S\|',token) is not None): # Caso for uma transição sem produção
                    adicionaNovaTransição(self,token[1],'Epsilon')
                    self.EndState.add(productionRelation['Epsilon'])

                    if len(token) > 2:
                        token = '|'
                    else:
                        token = ''                
                
    def readToken(self,token,flag):
        if token not in self.Token:
            self.Token.append(token) # Adiciona o simbolo para o conjunto caso ele ainda não exista dentro do conjunto Token
        
        # Caso a flag seja verdadeira então deve-se criar um novo token
        if flag:
            if token in self.State['S']: # Verifica se ele já está na produção de S
                self.State['S'][token].append(self.nameGenerator())
    
            else: # Caso o token ainda não estiver em S
                self.State['S'].update({token: [self.nameGenerator()]}) # Adiciona uma nova entrada para o token
                
            self.State.update({self.LastName : {}}) # Adiciona um novo estado vazio para a proxima rodada do FOR
        
        if not flag:
            self.State[self.LastName].update({token: [self.nameGenerator()]})  # Insere no último estado criado
            self.State.update({self.LastName: {}})                         # Cria um estado vazio para a próxima iteração

    def read(self,file):
        
        newState = True # Marca uma flag de novo estado

        self.State.update({'S': {}}) # Inicializa o dicionario de estados com void

        gramatica = file # Salva gramatica para ser usada depois
        
        if file[-1] != '\n':
            file += '\n'

        if not "::=" in file[:file.index('\n')]: # Verifica se não é uma gramatica que está como primeiro no arquivo
            
            if file[-1] != '\n':
                file += '\n'
            
            # -- Responsavel pela identificação dos tokens -- #
            for word in file:
                
                word = word.lower() # Para que todas letras fiquem minusculas
            
                if word == '\n': # Caso for o final da linha então tem-se a certeza que terminamos um token
                    if newState: # Caso haver duas quebras de linha então para-se de ler o arquivo 
                        break
                    newState = True
                    self.EndState.add(self.LastName)
                else:
                    self.readToken(word,newState) # Chama a função para adicionar o token para o alfabeto
                    newState = False # Reseta a flag para o proximo simbolo
        
            # -- Responsavel pela identificação das gramaticas -- #
            gramatica = file.partition('\n\n')[2] # Pega a gramatica separada dos tokens ja visualizados
    
        self.readGrammar(gramatica.splitlines())
