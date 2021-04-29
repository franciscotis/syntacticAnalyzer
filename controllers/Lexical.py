import re 
from controllers.FileManagement import FileManagement
from model.Token import Token
from model.Identifier import Identifier
from model.Digit import Digit
from model.Arithmetic import Arithmetic
from model.Relational import Relational
from model.Logic import Logic
from model.Delimiter import Delimiter
from model.Comment import Comment
from model.String import String

class Lexical:
    def __init__(self,filename):
        self.file = FileManagement(filename)
        self.content = list(self.file.read_file())
        self.content.append(' ')
        self.current_state = 0
        self.array_pointer = 0
        self.real_number = False
        self.current_token = None
        self.current_line = 1
        self.token_list = []
        self.can_read = True


    def run(self):
        result = self.nextToken()
        while(result!= None):
            result = self.nextToken()
        self.file.print_file(self.token_list)


    '''
        Máquina de estados que irá ler os caracteres
        Estado 00 - Estado Ocioso (espera de novos caracteres)
        Estado 01 - Estado Identificador (leitura de um caractere que irá formar um identificador ou uma palavra reservada)
        Estado 02 - Estado Digito (leitura de um caractere que irá formar um dígito)
        Estado 03 - Estado de Operador Aritmético (leitura de um caractere que irá formar um operador artimético) ou em alguns casos um delimitador de comentário (Estado 07)
        Estado 04 - Estado Relacional (leitura de um caractere que irá formar um operador relacional)
        Estado 05 - Estado de Operador Lógico (leitura de um caractere que irá formar um operador lógico)
        Estado 06 - Estado Delimitador (leitura de um caractere que irá formar um delimitador)
        Estado 08 - Estado Cadeia de Caracteres (leitura de um caractere que irá formar uma cadeia de caracteres)
    '''

    def nextToken(self):
        if(self.array_pointer <= len(self.content)):
            while(True):
                currentChar = self.getNextChar()
                if(currentChar is not None):
                    if self.current_state==0:
                        self.current_token = None
                        if(Token.isChar(currentChar)):
                            self.current_state = 1
                            self.current_token = Identifier(currentChar)
                        elif(Token.isNumber(currentChar)):
                            self.current_state = 2
                            self.current_token = Digit(currentChar)
                        elif(Token.isArithmeticOperator(currentChar)):
                            nextChar = self.content[self.array_pointer]
                            if(Token.isCommentDelimiter(currentChar, nextChar)):
                                self.current_state = 7
                                self.current_token = Comment(currentChar+nextChar)
                            else:
                                self.current_state = 3
                                self.current_token = Arithmetic(currentChar)
                        elif(Token.isRelationalOperator(currentChar)):
                            self.current_state = 4
                            self.current_token = Relational(currentChar)
                        elif(Token.isLogicOperator(currentChar)):
                            self.current_state = 5
                            self.current_token = Logic(currentChar)
                        elif(Token.isDelimiter(currentChar)):
                            self.current_state = 6
                            self.current_token = Delimiter(currentChar)
                        elif(Token.isStringDelimeter(currentChar)):
                            self.current_state = 8
                            self.current_token = String(currentChar)
                        elif(currentChar == '\n'):
                            self.current_line+=1
                        else:
                            if(not Token.isSpace(currentChar)):
                                self.current_state = 1
                                self.current_token = Identifier(currentChar)
                                self.current_token.error = True
                    elif(self.current_state ==1):
                        if(self.current_token.isValid(currentChar) and not Token.isSpace(currentChar)):
                            self.current_token.setValue(currentChar)
                            self.current_state = 1
                        else:
                            if(not self.current_token.validNeighbors(currentChar) and not Token.isSpace(currentChar)):
                                self.current_token.setValue(currentChar)
                                self.current_state = 1
                            else:
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                    elif(self.current_state==2):
                        if(self.current_token.isValid(currentChar) and not Token.isSpace(currentChar)):
                            self.current_token.setValue(currentChar)
                            self.current_state = 2
                        else:
                            if(not self.current_token.validNeighbors(currentChar) and not Token.isSpace(currentChar)):
                                self.current_token.setValue(currentChar)
                                self.current_state = 2
                            else:
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                    elif self.current_state ==3:
                        if(self.current_token.isValid(currentChar) and not Token.isSpace(currentChar)):
                            self.current_token.setValue(currentChar)
                            self.current_state = 3
                        else:
                            if(not self.current_token.validNeighbors(currentChar) and not Token.isSpace(currentChar)):
                                self.current_token.setValue(currentChar)
                                self.current_state = 3
                            elif Token.isSpace(currentChar):
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                            else:
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                    elif self.current_state ==4:
                        if(self.current_token.isValid(currentChar) and not Token.isSpace(currentChar)):
                            self.current_token.setValue(currentChar)
                            self.current_state = 3
                        else:
                            if(not self.current_token.validNeighbors(currentChar) and not Token.isSpace(currentChar)):
                                self.current_token.setValue(currentChar)
                                self.current_state = 3
                            elif Token.isSpace(currentChar):
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                            else:
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                    elif self.current_state==5:
                        if(self.current_token.isValid(currentChar) and not Token.isSpace(currentChar)):
                            self.current_token.setValue(currentChar)
                            self.current_state = 5
                        else:
                            if(not self.current_token.validNeighbors(currentChar) and not Token.isSpace(currentChar)):
                                self.current_token.setValue(currentChar)
                                self.current_state = 5
                            elif Token.isSpace(currentChar):
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                            else:
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                    elif self.current_state==6:
                        if(self.current_token.isValid(currentChar) and not Token.isSpace(currentChar)):
                            self.current_token.setValue(currentChar)
                            self.current_state = 6
                        else:
                            if(not self.current_token.validNeighbors(currentChar) and not Token.isSpace(currentChar)):
                                self.current_token.setValue(currentChar)
                                self.current_state = 6
                            elif Token.isSpace(currentChar):
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                            else:
                                self.current_state = 0
                                self.back()
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                    elif self.current_state==7:
                        if(self.current_token.isInlineComment()):
                            if(self.current_token.isEndInlineComment(currentChar)):
                                self.current_state = 0
                                self.back()

                        elif(self.current_token.isBlockComment()):
                            if(self.current_token.isBreakLine(currentChar)): self.current_line+=1
                            elif(self.array_pointer < len(self.content)):
                                nextChar = self.content[self.array_pointer]
                                if(self.current_token.isEndBlockComment(currentChar+nextChar)):      
                                    self.array_pointer+=1
                                    self.current_state = 0
                        
                    elif self.current_state==8:
                        self.current_token.setValue(currentChar)
                        if(self.current_token.isBreakLine(currentChar)):
                            self.back()
                            self.current_state = 0
                            self.token_list.append(self.current_token.returnValue(self.current_line))
                            return self.current_token.returnValue(self.current_line)
                        elif(self.current_token.isValid(currentChar)): pass
                        elif(Token.isStringDelimeter(currentChar)):
                            prevChar = self.content[self.array_pointer-2]
                            if(not self.current_token.isEscapedDelimeter(prevChar+currentChar)):
                                self.current_token.setError()
                                self.current_state = 0
                                self.token_list.append(self.current_token.returnValue(self.current_line))
                                return self.current_token.returnValue(self.current_line)
                        elif(not Token.isSymbol(currentChar)):
                            self.current_token.unknown_symbol = True
            
                else:
                    if(self.current_token and self.current_token.value!="//"):
                        token = self.current_token.returnValue(self.current_line)
                        self.current_token = None
                        self.token_list.append(token)
                        return token
                    return
        else:
            return None
                    
              
    def getNextChar(self):
        if self.array_pointer < len(self.content):
            next_char = self.content[self.array_pointer]
            self.array_pointer+=1
            return next_char
        return None

    def back(self):
        self.array_pointer-=1
