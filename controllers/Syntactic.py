import re 
class Syntactic:
    def __init__(self, lexical):
        self.lexical = lexical
        self.token = ''    

    def run(self):
        self.getNextToken()
        self.inicio()


    def getNextToken(self):
        self.token = self.lexical.nextToken()


    def inicio(self):
        if(self.token.getValue() == 'typedef'):
            print(self.typedefDeclaration())
            self.inicio()
        elif(self.token.getValue() == 'struct'):
            print(self.structDeclaration())
        elif(self.token.getValue() == 'var'):
            print("var")
            self.header1()
        elif(self.token.getValue() == 'const'):
            print("const")
            self.header2()
        elif(self.token.getValue() == 'function'):
            print('function')
        elif(self.token.getValue() == 'procedure'):
            print('procedure')
        else:
            print("Invalid Token")

    def header1(self):
        if self.token.getValue() == 'typedef':
            self.typedefDeclaration()
            self.header1()
        elif self.token.getValue() == 'struct':
            print(self.structDeclaration())
            self.header1()
        elif self.token.getValue() == 'const':
            print('const')
            self.header3()
        elif self.token.getValue() == 'function':
            print('function')
        elif self.token.getValue() == 'procedure':
            print('procedure')    

    def header2(self):
        if self.token.getValue() == 'typedef':
            self.typedefDeclaration()
            self.header2()  
        elif self.token.getValue() == 'struct':
            print(self.structDeclaration())
            self.header2()
        elif self.token.getValue() == 'const':
            print('const')
            self.header3()
        elif self.token.getValue() == 'function':
            print('function')
        elif self.token.getValue() == 'procedure':
            print('procedure')
        else: 
            print("Invalid Token")

    def header3(self):
        if self.token.getValue() == 'typedef':
            self.typedefDeclaration()
            self.header3()  
        elif self.token.getValue() == 'struct':
            print(self.structDeclaration())
            self.header3()
        elif self.token.getValue() == 'function':
            print('function')
        elif self.token.getValue() == 'procedure':
            print('procedure')
        else: 
            print("Invalid Token")
                
    def typedefDeclaration(self):
        first = 'typedef'
        if(self.token.getValue() == first):
            self.getNextToken()
        else:
            return "Expecting typedef token"
        return self.contTypedefDeclaration()
        
    def contTypedefDeclaration(self):
        if self.dataType():
            self.getNextToken()
            if self.token.getType()=="ID":
                self.getNextToken()
                if self.token.getValue() == ';':
                    self.getNextToken()
                    return 'typedef created successfully'
                else:
                    return "Expecting ; token"
            else:
                return 'Expecting identifier token'
        elif self.token.getValue() == 'struct':
            self.getNextToken()
            if self.token.getType()=="ID":
                self.getNextToken()
                if self.token.getType()=="ID":
                    self.getNextToken()
                    return True
                return 'Expecting identifier token'
            return 'Expecting Identifier token'
        return "Expecting struct token"


    def structDeclaration(self):
        if(self.token.getValue() == 'struct'):
            self.getNextToken()
            if(self.token.getType()=="ID"):
                self.getNextToken()
                return self.structVars()
            return 'Expecting identifier token'
        return 'Expecting struct token'
        
    def structVars(self):
        if(self.token.getValue() =='{'):
            self.getNextToken()
            if(self.token.getValue() == 'var'):
                self.getNextToken()
                if(self.token.getValue() =='{'):
                    self.getNextToken()
                    return self.firstStructVar()
                else:
                    return 'Expecting { token'
            return  'Expecting var token'
        elif(self.token.getValue() == 'extends'):
            self.getNextToken()
            if(self.token.getType()=="ID"):
                self.getNextToken()
                if(self.token.getValue() == '{'):
                    self.getNextToken()
                    if(self.token.getValue() == 'var'):
                        self.getNextToken()
                        if(self.token.getValue() == '{'):
                            self.getNextToken()
                            return self.firstStructVar()
                        return 'Expecting { token'
                    return 'Expecting var token'
                return 'Expecting { token'
            return 'Expecting identifier token'
        return 'Expecting extends token'

        
    def firstStructVar(self):
        if(self.dataType()):
            self.getNextToken()
            return self.structVarId()
        return 'Expecting a data type token'

    def structVarId(self):
        if(self.token.getType()=="ID"):
            self.getNextToken()
            return self.structVarExp()
        return 'Expecting an identifier token'
    
    def structVarExp(self):
        if(self.token.getValue() == ','):
            self.getNextToken()
            return self.structVarId()
        elif(self.token.getValue() == ';'):
            self.getNextToken()
            return self.proxStructVar()
        elif(self.token.getValue() == '['):
            self.getNextToken()
            if(self.inteiro(self.token.getValue())):
                self.getNextToken()
                if(self.token.getValue() == ']'):
                    self.getNextToken()
                    return self.structMatriz()
                return 'Expecting ] token'
            return 'Expecting int token'
        return 'Expecting , ; or [ token'
    

    def structMatriz(self):
        if(self.token.getValue() == '['):
            self.getNextToken()
            if(self.inteiro(self.token.getValue())):
                self.getNextToken()
                if(self.token.getValue() == ']'):
                    self.getNextToken()
                    return self.contStructMatriz()
                return 'Expecting ] token'
            return 'Expecting int token'
        elif(self.token.getValue() ==','):
            self.getNextToken()
            return self.structVarId()
        elif(self.token.getValue() == ';'):
            self.getNextToken()
            return self.proxStructVar()


    def proxStructVar(self):
        if(self.dataType()):
            self.getNextToken()
            self.structVarId()
        elif(self.token.getValue() == "}"):
            self.getNextToken()
            if(self.token.getValue() == "}"):
                return "struct created successfully"
            else:
                return "Expecting } token"
        
        return "Expecting } or datatype  token"


    def methods(self):
        if(self.token.getValue()) == "function":
            print("function")
            self.methods()
        elif(self.token.getValue() == "procedure"):
            print("procedure")
            self.methods()

    def function(self):
        if(self.token.getValue() == "function"):
            self.getNextToken()
            if(self.dataType()):
                self.getNextToken()
                if(self.token.getType() == "ID"):
                    self.getNextToken()
                    if(self.token.getValue() == "("):
                        self.getNextToken()
                        return self.continueFunction()
                    return "Expecting ( token"
                return "Expecting identifier token"
            return "Expecting datatype token"
        return "Expecting function token"


    def continueFunction(self):
        return "continue function"
                

    



    def dataType(self):
        first = ['int','real','string','boolean']
        return True if (self.token.getValue() in first or self.token.getType()=="ID") else False


    def inteiro(self, token):
        p = re.compile('[0-9]+')
        return True if p.match(token) is not None else False

        
   



