class Symbol:
    
    '''
        Simbolo que está dentro da tabela de simbolos. Seus conteúdos:
        - Identificador (o nome da variável)
        - Tipo (se é uma variável ou função)
        - Tipo de token (identificador)
        - Parametros - opcional (caso seja uma função e tenha parâmetros, ele terá uma lista de parâmetros
        nos quais estão inclusas em uma nova tabela de símbolos.)
        - Valor que está associado a ele (caso exista uma atribuição)
    '''
    
    def __init__(identifier, identifier_type, token_type, value):
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.token_type = token_type
        self.parameters = []
        self.value = value

    def addParameters(self, symbol):
        self.parameters.append(symbol)

    def removeParameters(self, symbol):
        self.parameters.remove(symbol)




