import re 
class Syntactic:
    def __init__(self, lexical):
        self.lexical = lexical
        self.token = ''    

    def run(self):
        self.token = self.getNextToken()
        print(self.token)
        self.inicio()


    def getNextToken(self):
        new_token = self.lexical.nextToken()
        if new_token != None:
            self.token = new_token.split()[2]
        else:
            self.token = None


    def inicio(self):
        if(self.token == 'typedef'):
            print(self.typedefDeclaration())
            self.inicio()
        elif(self.token == 'struct'):
            print(self.structDeclaration())
        elif(self.token == 'var'):
            print("var")
            self.header1()
        elif(self.token == 'const'):
            print("const")
            self.header2()
        elif(self.token == 'function'):
            print('function')
        elif(self.token == 'procedure'):
            print('procedure')
        else:
            print("Invalid Token")

    def header1(self):
        if self.token == 'typedef':
            self.typedefDeclaration()
            self.header1()
        elif self.token == 'struct':
            print(self.structDeclaration())
            self.header1()
        elif self.token == 'const':
            print('const')
            self.header3()
        elif self.token == 'function':
            print('function')
        elif self.token == 'procedure':
            print('procedure')    

    def header2(self):
        if self.token == 'typedef':
            self.typedefDeclaration()
            self.header2()  
        elif self.token == 'struct':
            print(self.structDeclaration())
            self.header2()
        elif self.token == 'const':
            print('const')
            self.header3()
        elif self.token == 'function':
            print('function')
        elif self.token == 'procedure':
            print('procedure')
        else: 
            print("Invalid Token")

    def header3(self):
        if self.token == 'typedef':
            self.typedefDeclaration()
            self.header3()  
        elif self.token == 'struct':
            print(self.structDeclaration())
            self.header3()
        elif self.token == 'function':
            print('function')
        elif self.token == 'procedure':
            print('procedure')
        else: 
            print("Invalid Token")
                
    def typedefDeclaration(self):
        first = 'typedef'
        if(self.token == first):
            self.getNextToken()
        else:
            return "Expecting typedef token"
        return self.contTypedefDeclaration()
        
    def contTypedefDeclaration(self):
        if self.dataType():
            self.getNextToken()
            if self.identificador(self.token):
                self.getNextToken()
                if self.token == ';':
                    return 'typedef created successfully'
                else:
                    return "Expecting ; token"
            else:
                return 'Expecting identifier token'
        elif self.token == 'struct':
            self.getNextToken()
            if self.identificador(self.token):
                self.getNextToken()
                if self.identificador(self.token):
                    self.getNextToken()
                    return True
                return 'Expecting identifier token'
            return 'Expecting Identifier token'
        return "Expecting struct token"


    def structDeclaration(self):
        if(self.token == 'struct'):
            self.getNextToken()
            if(self.identificador(self.token)):
                self.getNextToken()
                return self.structVars()
            return 'Expecting identifier token'
        return 'Expecting struct token'
        
    def structVars(self):
        if(self.token =='{'):
            self.getNextToken()
            if(self.token == 'var'):
                self.getNextToken()
                if(self.token =='{'):
                    return self.firstStructVar()
                else:
                    return 'Expecting { token'
            return  'Expecting var token'
        elif(self.token == 'extends'):
            self.getNextToken()
            if(self.identificador(self.token)):
                self.getNextToken()
                if(self.token == '{'):
                    self.getNextToken()
                    if(self.token == 'var'):
                        self.getNextToken()
                        if(self.token == '{'):
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
        if(self.identificador(self.token)):
            self.getNextToken()
            return self.structVarExp()
        return 'Expecting an identifier token'
    
    def structVarExp(self):
        if(self.token == ','):
            self.getNextToken()
            return self.structVarId()
        elif(self.token == ';'):
            self.getNextToken()
            return self.proxStructVar()
        elif(self.token == '['):
            self.getNextToken()
            if(self.inteiro(self.token)):
                self.getNextToken()
                if(self.token == ']'):
                    self.getNextToken()
                    return self.structMatriz()
                return 'Expecting ] token'
            return 'Expecting int token'
        return 'Expecting , ; or [ token'
    

    def structMatriz(self):
        if(self.token == '['):
            self.getNextToken()
            if(self.inteiro(self.token)):
                self.getNextToken()
                if(self.token == ']'):
                    self.getNextToken()
                    return self.contStructMatriz()
                return 'Expecting ] token'
            return 'Expecting int token'
        elif(self.token ==','):
            self.getNextToken()
            return self.structVarId()
        elif(self.token == ';'):
            self.getNextToken()
            return self.proxStructVar()

    def dataType(self):
        first = ['int','real','string','boolean', 'identificador']
        return True if (self.token in first or identificador(self.token)) else False

    def identificador(self, token):
        p = re.compile('([a-z]|[A-Z])(([a-z]|[A-Z])|[0-9]|_)*')
        return True if p.match(token) is not None else False

    def inteiro(self, token):
        p = re.compile('[0-9]+')
        return True if p.match(token) is not None else False

        
   



