import re 
import abc

'''
Classe Token as quais as classes modelos serão heradas. Aqui contém os principais métodos
'''
class Token:
    def __init__(self, value=''):
        self.type = '' #Tipo do token
        self.value = value #Valor do token
        self.current_line = '' #Linha atual
        self.reserved_words = '' #Palavras reservadas
        self.supported_neighbors = '' #Caracteres vizinhos que são suportados para cada token
        self.error = False
    

    def getToken(self):
        #Função que retorna o token formatado com a linha atual, o tipo e o seu valor
        return "{} {} {}".format(self.current_line,self.type, self.value)

    
    def setType(self,type):
        #Função que altera o tipo de token
        self.type = type

    def setValue(self,value):
        #Função que altera o valor do token
        self.value+= value

    def validNeighbors(self,currentChar):
        #Função que verifica se o caractere vizinho de um determinado token é válido
        p = re.compile(self.supported_neighbors)
        return True if p.match(currentChar) is not None else False
    
    @abc.abstractmethod
    def isValid(self,currentChar):
        return

    @abc.abstractclassmethod
    def continueInvalidToken(self,currentChar):
        return

    @abc.abstractclassmethod
    def returnValue(self,current_line):
        return 

    @abc.abstractclassmethod
    def returnError(self,current_line):
        return
    
    @classmethod
    def isNumber(self, char):
        p = re.compile('([0-9])')
        return True if p.match(char) is not None else False

    @classmethod
    def isRealNumber(self,char):
        p = re.compile('([.])')
        return True if p.match(char) is not None else False

    @classmethod
    def isChar(self,char):
        p = re.compile('([a-z]|[A-Z])')
        return True if p.match(char) is not None else False

    @classmethod
    def is_underscore(self,char):
        p = re.compile('([_])')
        return True if p.match(char) is not None else False

    @classmethod
    def isBreakLine(self,term):
        if term == '\n' or term == '\r':
            return True

    @classmethod
    def isSpace(self, term):
        return True if term == '\n' or term == ' ' or term == '\r' or term == '\t' else False
        
    @classmethod
    def isArithmeticOperator(self,char):
        p = re.compile('([+]|-|[*]|[\/])')
        return True if p.match(char) is not None else False

    @classmethod
    def isCommentDelimiter(self, char1, char2):
        return (char1+char2 == '//' or char1+char2 == '/*')

    @classmethod
    def isDelimiter(self,char):
        p = re.compile('([;]|[,]|[(]|[)]|[{]|[}]|[\[]|[\]]|[.]|[+]|[-]|[*]|[/])')
        return True if p.match(char) is not None else False

    @classmethod
    def isStringDelimeter(self, char):
        return (char=='"')

    @classmethod
    def isSymbol(self, char):
        return True if(re.match('[\x20-\x21]|[\x23-\x7e]', char)) else False

    @classmethod
    def isRelationalOperator(self,char):
        p = re.compile('(=|!|>|<)')
        return True if p.match(char) is not None else False

    @classmethod
    def isLogicOperator(self, char):
        p = re.compile('(&|[|]|!)')
        return True if p.match(char) is not None else False

