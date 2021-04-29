from model.Token import Token
import re 

class Arithmetic(Token):
    def __init__(self, value):
        Token.__init__(self,value)
        self.supported_neighbors = '([a-z]|[A-Z]|[0-9]|[(]|[)]|[;]|[\[]|[\]])'
        self.supported_value = ['++','--']

    def isValid(self, currentChar):
        if(self.isArithmeticOperator(currentChar) and (self.value+currentChar in self.supported_value)):
            return True
        elif(self.notValidArithmetic(currentChar) and not self.isSpace(currentChar)):
            self.error = True
        return False

    def notValidArithmetic(self,currentChar):
        if((not self.validNeighbors(currentChar)) ):
            return True
        return False


    '''
        Retorno: 
                 valido   -  ART - Operador Aritmético Valido
                 inválido -  OpMF - Operador Mal Formado
    '''
    def returnValue(self, current_line):
        self.type = 'ART' if not self.error else 'OpMF'
        self.current_line = current_line
        return self.getToken()