from model.Token import Token
import re 

class Digit(Token):
    def __init__(self, value):
        Token.__init__(self,value)
        self.point_delimiter = False
        self.supported_neighbors = '([+]|[-]|[*]|[=]|[!]|[>]|[<]|[\/]|[;]|[,]|[(]|[)]|[\[]|[\]])'

    def isValid(self, currentChar):
        if(self.isNumber(currentChar)):
            return True
        elif(self.isRealNumber(currentChar) and not self.point_delimiter):
            self.point_delimiter = True
            return True
        elif(self.notValidNumber(currentChar) and not self.isSpace(currentChar)):
            self.error = True
        return False

    def notValidNumber(self,currentChar):
        if((self.isRealNumber(currentChar) and self.point_delimiter) or not self.validNeighbors(currentChar) ):
            return True
        return False

    def supportedChars(self, char):
        p = re.compile(self.supported_neighbors)
        return True if p.match(char) is not None else False


    '''
        Retorno: 
                 valido   -  NRO - Número
                 inválido -  NMF - Número Mal Formado
    '''


    def returnValue(self, current_line):
        self.type = 'NRO' if not self.error else 'NMF'
        self.current_line = current_line
        return self.getToken()


