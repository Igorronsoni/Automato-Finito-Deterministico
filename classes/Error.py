class Error:

    def __init__(self,automato):
        self.State = automato.State # Carrega os estados minimizados
        self.EndState = automato.EndState # Carrega os estados finais
        self.Token = automato.Token # Carrega o conjunto de tokens 

        # -- Faz a preparação do estado de erro -- #
        self.State.update({'Error': {}})
        self.EndState.add('Error')

    def read(self):
        for token, estado in self.State.items():
            for letra in self.Token:
                if letra not in estado.keys():
                    self.State[token].update({letra : ['Error']})
        