class Dead:

    def __init__(self, automato):
        self.automato = automato
        self.State = {k:v for k,v in automato.State.items()} # Carrega os estados determinizados e livre dos inalcançável
        self.EndState = automato.EndState # Carrega os estados finais para testes e possiveis edições
        
        self.Token = [] # Inicia uam lista de tokens do automato
        self.EstadosVisitados = [] # Inicia a lista de Estados visitados

    def read(self,grammar):
        deletar = [] # Transição que deve ser deletada
        
        morto = True # Marca o estado testado com inutil para ser trocado o valor caso ele não seja

        if grammar in self.EndState: # Verifica se o estado é um estado final para ser marcado com não inutil
            # Verifica se o estado atual ja foi visitado
            if grammar in self.EstadosVisitados:
                return 1
            else: # Caso ainda n ter sido visitado, verifica se ele é ou n folha
                if len(self.State[grammar]) == 0:
                    return 1

        # Verifica se o estado ja foi visitado anteriormente
        if grammar in self.EstadosVisitados:
            
            # Caso o estado atual foi testado por ultimo então estamos em um loop
            if self.EstadosVisitados[-1] == grammar:
                return 0

            # Senão ele so retorna como não morto
            return 1

        else: # Senão adiciona ele para a lista de visitados
            self.EstadosVisitados.append(grammar)
        
        for letra, estado in self.automato.State[grammar].items():
            
            if self.read(estado[0]):
                morto = False
                
                # Adiciona o token para o conjunto de letras
                if letra not in self.Token:
                    self.Token.append(letra)
            
            else:
                if morto:
                    deletar.append(letra) # Salva o token que deve ser deletado para quando terminar o laço apagar 
                
        # Caso após os testes, a variavel ainda continuar verdadeira para inutil, o estado é apagado
        if morto and grammar not in self.EndState:
            del[self.State[grammar]]
            return 0

        # Passa pelos tokens que devem ser deletados
        for token in range(len(deletar)):
            del[self.State[grammar][deletar[token]]]
            
        # Caso o estado não seja inutil
        return 1

            

