import re

class AFD:
    def __init__(self,Automato):
        self.Automato = Automato
    
        self.State = self.Automato.State
        self.EndState = Automato.EndState
        self.Automato.EndState = set() # Reinicia o conjunto dos finais 
        self.Token = Automato.Token

        self.NewState = self.Automato.NewState # Ponteiro para o estado sem inalcançaveis
        self.ProductionRelation = dict() # Cria uma relação de nomes das produções criadas na determinização

    def read(self):
        # -- Variaveis para controle dos estados -- #
        producoes = list(self.State.keys()) # Todos as produções inciais de State para o laço iterador
        used = set('S') # Conjunto de estados que pode ser visitados
        
        # -- Contadores de laço -- #
        size = len(self.State)
        index = 0

        # Laço iterador para passar por todo o State mesmo ele sendo editado
        while index < size:

            # -- Verifica se o estado pode ser visitado -- #
            if producoes[index] in used:
                
                # Cria um novo estado dentro dos estados de minimização
                self.Automato.NewState.update({ producoes[index] : {}})
                
                # -- Passa por cada token e os estados de transição dentro do estado atual -- # 
                for token, estado in self.State[producoes[index]].items():
                    
                    nomeDoEstado = estado[0] # Nome usado para armazenar um nome de produção atual
                    
                    # -- Se a quantidade de estados de transição for maior que 1 então deve-se determinizar -- #
                    if len(estado) > 1:
                        
                        # Verifica se a determinização ja existe 
                        if tuple(sorted(estado)) in self.ProductionRelation:
                            nomeDoEstado = self.ProductionRelation[tuple(sorted(estado))]
    
                            # -- Altera a transição dentro do estado -- #
                            self.State[producoes[index]][token] = [nomeDoEstado]

                        else: # Senão gera um novo nome de estado
                            self.Automato.nameGenerator() # Gera um novo estado
                            nomeDoEstado = self.Automato.LastName
                            
                            # -- Altera a transição dentro do estado -- #
                            self.State[producoes[index]][token] = [nomeDoEstado]
                           
                            # -- Adiciona o novo estado para produções caso ele não esteja -- #
                            producoes.insert(index + 1, nomeDoEstado)

                            # -- Cria estado novo e aumenta o size para o laço correr a lista toda -- #
                            size += 1

                            # -- Adiciona o novo estado para a relação de de estados -- #
                            self.ProductionRelation.update({ tuple(sorted(estado)) : nomeDoEstado })

                            # -- Adiciona o novo estado para o State para ser verificado -- #
                            self.State.update({ nomeDoEstado : {} }) 

                            # -- Laço iterador de estados nos quais deve-se determinizar -- # 
                            for nome in estado:
                                
                                # Verifica se a produção determinizada faz transição com um estado final
                                if nome in self.EndState:
                                    self.Automato.EndState.add(nomeDoEstado)

                                # -- Laço iterador para as transições do estado testado -- #
                                for letra, transicao in self.State[nome].items():
                                    
                                    # -- Verifica se ja possui uma transição com essa letra dentro do estado -- #
                                    if letra in self.State[nomeDoEstado]:
                                        
                                        # -- Passa pelos estados criados para verificar se a nova transição é um estado criado ou se a transição ja existente é um estado criado
                                        conjuntoTupla = self.State[nomeDoEstado][letra].copy() # Conjunto contido no estado
                                        conjuntoTransicao = transicao.copy() # Conjunto contido na transicao
                                        
                                        for tupla in self.ProductionRelation.keys():
                                    
                                            if self.ProductionRelation[tupla] == self.State[nomeDoEstado][letra][0]:
                                                conjuntoTupla = list(tupla)

                                            if self.ProductionRelation[tupla] in transicao[0]:
                                                conjuntoTransicao = list(tupla)
                                        
                                        # Adiciona o conjunto para o estado    
                                        self.State[nomeDoEstado][letra] = list(set(conjuntoTransicao).union(set(conjuntoTupla))) 
                                        
                                        # Altera a variavel caso ela exista
                                        for tupla in self.ProductionRelation.keys():
                                            # Verifica se existe a variavel dentro da relação de produções
                                            if tuple(sorted(self.State[nomeDoEstado][letra])) == tupla:
                                                self.State[nomeDoEstado][letra] = [self.ProductionRelation[tupla]]
                                                
                                    else:    
                                        # Adiciona a transição para o estado novo
                                        self.State[nomeDoEstado].update({ letra : transicao })
                       
                    # Verifica se a produção é um estado final
                    if nomeDoEstado in self.EndState:
                        self.Automato.EndState.add(nomeDoEstado)

                    # -- Adiciona o novo estado para a lista de produções que podem ser testadas -- #
                    used.add(nomeDoEstado)
                    
                    # Adiciona a transição para o novo estado
                    self.Automato.NewState[producoes[index]].update({ token : [nomeDoEstado]})
                    
            index += 1       




        '''
        # -- Prepara as variaveis -- #
        producoes = [] # Nome das produções para poder passar pelos estados e altera-los
        used = set('S') # Conjunto de produções que deve ser verificado / Começa com o valor inicial de S para varificar o primeiro estado
        size = len(self.State) # Quantidade original de estados
        index = 0 # Contador do laço

        novaProdução = True

        # Prepara a lista de produções
        for name in self.State.keys():
            producoes.append(name)
        
        while index < size:
            
            if producoes[index] in used: # Verifica se a produção pode ser usada para determinização            
               
                # Verifica se o estado é um estado final e adiciona ele para a lista    
                if producoes[index] in self.EndState:
                    self.Automato.EndState.add(producoes[index])

                # Salva em NewState um novo estado para o proximo passo que será a minimização
                self.Automato.NewState.update({producoes[index] : {}})

                for token, estado in self.State[producoes[index]].items(): # Passa pelos tokens e pelo(s) estado(s) de determinado estado  
                    
                    if len(estado) > 1:
                        
                        if estado[0] in self.ProductionRelation:
                            # Se a produção que esta em estado[0] estiver dentro da relação, devesse fazer uma interesecção entre as listas
                            # para saber se deve-se criar um novo nome de produção ou usar o que ja existe
                            conjA = set(self.ProductionRelation[estado[0]])
                            
                            # Se só houveremm dois estados no mesmo token então ele compara os dois
                            if len(estado) == 2:
                                if estado[1] in self.ProductionRelation:
                                    conjA = conjA.intersection(self.ProductionRelation[estado[1]])
                                else:
                                    conjA = set()
                            else: # Senão ele passa por cada conjunto
                                for x in range(1,len(estado)): # Gera as intersecções
                                    if estado[x] in self.ProductionRelation:
                                        conjA = conjA.intersection(self.ProductionRelation[estado[x]])
                                    else:
                                        conjA = set()
                                        break
                                
                            # Se o conjA não for uum conuunto vazio então foi encontrado o estado existente
                            if conjA != set():
                                for name in conjA:
                                    self.nomeProducao = name
                                    novaProdução = False
                            # Senão deve-se criar um novo estado
                            else:
                                self.Automato.nameGenerator() # Cria um novo estado
                                self.nomeProducao = self.Automato.LastName
                                novaProdução = True
                                size += 1
                        else:
                            self.Automato.nameGenerator() # Cria um novo estado
                            self.nomeProducao = self.Automato.LastName
                            novaProdução = True
                            size += 1
                        
                        # Altera dentro da gramatica a transição para a determinização
                        self.State[producoes[index]][token] = [self.nomeProducao]
                        
                        # Salva a transição dentro do estado verificado e cria uma produção para o novo estado 
                        self.Automato.NewState[producoes[index]].update({token : [self.nomeProducao]})
                        
                        # Adiciona a nova produção para ser testada
                        if self.nomeProducao not in self.State:
                            self.State.update({self.nomeProducao : {}})

                        # Adiciona a produção para que seja verificado posteriormente
                        if self.nomeProducao not in producoes:
                            producoes.insert(index + 1,self.nomeProducao)
                        
                        # Adiciona a produção para ser testada
                        used.add(self.nomeProducao)
                        
                        # Passa pelas produções dentro de estado caso a produção seja criada
                        for name in estado:
                            
                            # Adiciona o estado para os estados finais caso seja necessario
                            #if self.State[name] == {}:
                            #    self.EndState.add(self.nomeProducao)

                            # Verifica se a letra atual esta dentro da relação de nomes das produções
                            if name not in self.ProductionRelation:
                                self.ProductionRelation.update({name : [self.nomeProducao]})
                            else:
                                # Verifica se o nome da produção nova esta dentro da relação
                                if self.nomeProducao not in self.ProductionRelation[name]:
                                    self.ProductionRelation[name].append(self.nomeProducao)
                            
    
                            # Passa pelos tokens e pelos estados dentro do estado testado
                            for letra, prods in self.State[name].items():
                                
                                # Se a letra já esta alocada dentro do estado entao é so adicionar ele na lista
                                if letra in self.State[self.nomeProducao]:
                                    
                                    # Verifica se o que tem dentro do State é uma variavel criada a partir da produção verificada 
                                    for w in prods:
                                        if w in self.ProductionRelation:
                                            for tmp in self.State[self.nomeProducao][letra]:
                                                if tmp not in self.ProductionRelation[w]:
                                                    self.State[self.nomeProducao][letra].append(w)
                                    
                                # Senão só cria uma nova lista
                                else:
                                    self.State[self.nomeProducao].update({letra : prods.copy()})

                    else:
                        # Adiciona a produção para ser testada
                        used.add(estado[0])
                        
                        # Adiciona estados para ser minimizado
                        self.Automato.NewState[producoes[index]].update({token: self.State[producoes[index]][token]})
               
            index += 1 
    '''