from model.Token import Token

class Identifier(Token):
    def __init__(self,value):
        Token.__init__(self,value)
        self.supported_neighbors = '([+]|[-]|[*]|[=]|[!]|[>]|[<]|[\/]|[;]|[,]|[.]|[&]|[|]|[(]|[)]|[{]|[}]|[\[]|[\]])'
        self.reserved_words = ("var","const","typedef","struct","extends","procedure","function","start","return","if","else","then","while","read","print","int","real","boolean","string","true","false","global","local")  
        self.value = value

    def isValid(self, currentChar):
        if self.isChar(currentChar) or self.isNumber(currentChar) or self.is_underscore(currentChar):
            return True
        elif(not self.validNeighbors(currentChar) and not self.isSpace(currentChar)):
            self.error = True
        return False

    def continueInvalidToken(self,currentChar):
        return True if self.isValid(currentChar) else False

    def isReserved(self, term):
        return True if term in self.reserved_words else False

    def setError(self,value):
        self.error = value
    

    '''
        Retorno: 
                 valido   -  PRE - Palavra Reservada ou IDE - Identificador
                 inválido -  SIB - Simbolo inválido
    '''


    def returnValue(self, current_line):
        if self.isReserved(self.value):
            self.type = 'PRE' 
        else:
            self.type = 'IDE' if not self.error else 'SIB'
        self.current_line = current_line
        return self.getToken()
