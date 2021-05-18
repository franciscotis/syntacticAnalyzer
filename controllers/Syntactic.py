import re 
class Syntactic:
    def __init__(self, lexical, firstSet, followSet):
        self.lexical = lexical
        self.token = ''    
        self.firstSet  = firstSet
        self.followSet = followSet
        self.token_list = []

    def run(self):
        self.getNextToken()
        self.inicio()
        self.lexical.file.print_file(self.token_list)


    def getNextToken(self):
        self.token = self.lexical.nextToken()
        if self.token is not None:
            self.token_list.append(self.token.toString())
    
    def getError(self, sync_tokens:list):
        while(self.token is not None):
            for follow in sync_tokens:
                if(self.token.getValue()==follow): return
                if(self.token.getType()==follow):  return
            self.getNextToken()

    def inicio(self):
        if self.token is not None:
            if(self.token.getValue() in self.firstSet["TYPEDEFDECLARATION"]):
                self.typedefDeclaration()
                self.inicio()
            elif(self.token.getValue() in self.firstSet["STRUCTDECLARATION"]):
                self.structDeclaration()
                self.inicio()
            elif(self.token.getValue() in self.firstSet["VARDECLARATION"]):
                self.varDeclaration()
                self.header1()
            elif(self.token.getValue() in self.firstSet["CONSTDECLARATION"]):
                self.constDeclaration()
                self.header2()
            elif(self.token.getValue() in self.firstSet["METHODS"]):
                self.methods()
            else:
                self.token_list.append("ERROR on INICIO. Expecting ", self.firstSet["INICIO"], " got: " +self.token.getValue()) 

    def header1(self):
        if self.token is not None:
            if self.token.getValue() in self.firstSet["TYPEDEFDECLARATION"]:
                self.typedefDeclaration()
                self.header1()
            elif self.token.getValue() in self.firstSet["STRUCTDECLARATION"]:
                self.structDeclaration()
                self.header1()
            elif self.token.getValue() in self.firstSet["CONSTDECLARATION"]:
                self.constDeclaration()
                self.header3()
            elif self.token.getValue() in self.firstSet["METHODS"]:
                self.methods()
            else:
                self.token_list.append("ERROR on HEADER1. Expecting ", self.firstSet["HEADER1"], " got: " +self.token.getValue())


    def header2(self):
        if self.token is not None:
            if self.token.getValue() in self.firstSet["TYPEDEFDECLARATION"]:
                self.typedefDeclaration()
                self.header2()  
            elif self.token.getValue() in self.firstSet["STRUCTDECLARATION"]:
                self.structDeclaration()
                self.header2()
            elif self.token.getValue() in self.firstSet["VARDECLARATION"]:
                self.varDeclaration()
                self.header3()
            elif self.token.getValue() in self.firstSet["METHODS"]:
                self.methods()
            else: 
                self.token_list.append("ERROR on HEADER2. Expecting ", self.firstSet["HEADER2"], " got: " +self.token.getValue())

    def header3(self):
        if self.token.getValue() in self.firstSet["TYPEDEFDECLARATION"]:
            self.typedefDeclaration()
            self.header3()  
        elif self.token.getValue() in self.firstSet["STRUCTDECLARATION"]:
            self.structDeclaration()
            self.header3()
        elif self.token.getValue() in self.firstSet["METHODS"]:
            self.methods()
        else: 
            self.token_list.append(f"ERROR on HEADER3 line {self.token.current_line}: Expecting ", self.firstSet["HEADER3"], " got: " +self.token.getValue())

    def methods(self):
        if self.token is not None:
            if self.token.getValue() in self.firstSet["FUNCTION"]:
                self.function()
                self.methods()
            elif self.token.getValue() in self.firstSet["PROCEDURE"]:
                if self.token.getValue() == 'procedure':
                    self.getNextToken()
                    self.procedure()
                    self.methods()


    def value(self):
        if self.token.getValue() == 'true' or self.token.getValue()=='false':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["BOOLOPERATIONS2"] or self.token.getType() in self.firstSet["BOOLOPERATIONS2"]:
                self.boolOperations2()
        elif self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
            self.aritimeticOp()
            if self.token.getValue() in self.firstSet["BOOLOPERATIONS2"] or self.token.getType() in self.firstSet["BOOLOPERATIONS2"]:
                self.boolOperations2()
            if self.token.getValue() == '(':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["CONTFCALL"] or self.token.getType() in self.firstSet["CONTFCALL"]:
                    self.contFCall()
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTFCALL"], " got: " +self.token.getValue())
        elif self.token.getType() in self.firstSet["FUNCTIONCALL"]:
            self.functionCall()
        elif self.token.getValue() == '(':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["LOGICALOP"] or self.token.getType() in self.firstSet["LOGICALOP"]:
                self.logicalOp()
                if self.token.getValue() == ')':
                    self.getNextToken()
                else:
                    self.token_list.append("ERROR expecting ')' GOT "+ self.token.getValue())
            else:
                self.token_list.append("ERROR expecting ", self.firstSet["LOGICALOP"] + "GOT "+ self.token.getValue())
    
                
    
    def variavel(self):
        if self.token.getType() == "IDE":
            self.identificador()
        elif self.token.getValue() in self.firstSet["GLOBAL"]:
            self.globalFunction()
        elif self.token.getValue() in self.firstSet["LOCAL"]:
            self.local()

    def identificador(self):
        if self.token.getType()=="IDE":
            self.getNextToken()
            if self.token.getValue() in self.firstSet["CONTIDENTIFICADOR"]:
                self.contIdentificador()
        else:
            print("Error, expecting identifier token")


    def contIdentificador(self):
        if self.token.getValue() in self.firstSet["CONTELEMENTO"]:
            self.contElemento()
    
    def globalFunction(self):
        if self.token.getValue() == 'global':
            self.getNextToken()
            if self.token.getValue() == '.':
                self.getNextToken()
                if self.token.getType() == "IDE":
                    self.identificador()
                else:
                    self.token_list.append("ERROR expecting ", self.firstSet["IDENTIFICADOR"] + "GOT "+ self.token.getValue())
            else:
                self.token_list.append("ERROR expecting '.' GOT" + self.token.getValue())
        else:
            self.token_list.append("ERROR expecting 'global' GOT "+ self.token.getValue())

    def local(self):
            if self.token.getValue() == 'local':
                self.getNextToken()
                if self.token.getValue() == '.':
                    self.getNextToken()
                    if self.token.getType() == "IDE":
                        self.identificador()
                    else:
                        self.token_list.append("ERROR expecting ", self.firstSet["IDENTIFICADOR"] + "GOT "+ self.token.getValue())
                else:
                    self.token_list.append("ERROR expecting '.' GOT" + self.token.getValue())
            else:
                self.token_list.append("ERROR expecting 'local' GOT "+ self.token.getValue())

    def aritmeticValue(self):
        if self.token.getType() =="IDE":
            self.identificador()
        elif self.token.getType() == "NRO":
            self.getNextToken()
        elif self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"] :
            self.variavel()
        elif self.token.getType() == "CAD":
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expection aritmetic value")

    def dataType(self):
        return True if (self.token.getValue() in self.firstSet["DATATYPE"] or self.token.getType()=="IDE") else False

    def contElemento(self):
        if self.token.getValue() in self.firstSet["STRUCTE1"]:
            self.structE1()
        elif self.token.getValue() in self.firstSet["VETORE1"]:
            self.vetorE1()
        elif self.token.getValue() in self.firstSet["MATRIZE1"]:
            self.matrizE1()
        else:
            print('ERROR')

    
    def structE1(self):
        if self.token.getValue() == '.':
            self.getNextToken()
            if self.token.getType() == "IDE":
                self.identificador()
                if self.token.getValue() in self.firstSet["CONTIDENTIFICADOR"]:
                    self.contIdentificador()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Identifier expected")
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: '.' token expected")

    def vetorE1(self):
        if self.token.getValue() =='[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
                self.aritimeticOp()
                if self.token.getValue() == ']':
                    self.getNextToken()
                    if self.token.getValue() in self.firstSet["VETORE2"]:
                        self.vetorE2()
                if self.token.getValue() == '[':
                    self.vetorE1()
                    self.matrizE2()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"]," got: "+ self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '[' token. got: "+self.token.getValue())
        
    def vetorE2(self):
        if self.token.getValue() in self.firstSet["STRUCTE1"]:
            self.structE1()
        
    def matrizE1(self):
        if self.token.getValue() in self.firstSet["VETORE1"]:
            self.vetorE1()
            if self.token.getValue() in self.firstSet["VETORE1"]:
                self.vetorE1()
                if self.token.getValue() in self.firstSet["MATRIZE2"]:
                    self.matrizE2()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VETORE1"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VETORE1"], " got: " +self.token.getValue())

    def matrizE2(self):
        if self.token.getValue() in self.firstSet["STRUCTE1"]:
            self.structE1()

    def varDeclaration(self):
        if self.token.getValue() == "var":
            self.getNextToken()
            if self.token.getValue() =="{":
                self.getNextToken()
                if self.token.getValue() in self.firstSet["PRIMEIRAVAR"] or self.token.getType() in self.firstSet["PRIMEIRAVAR"]:
                    self.primeiraVar()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PRIMEIRAVAR"], " got: " +self.token.getValue()) 
                    self.getError(self.followSet["VARDECLARATION"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} "+ " got: " +self.token.getValue()) 
                self.getError(self.followSet["VARDECLARATION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'var' "+ " got: " +self.token.getValue())           
            self.getError(self.followSet["VARDECLARATION"])

    def primeiraVar(self):
        if self.token.getValue() in self.firstSet["CONTINUESOS"] or self.token.getType() in self.firstSet["CONTINUESOS"]:
            self.continueSos()
            if self.token.getType() in self.firstSet["VARID"]:
                self.varId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARID"], " got: " +self.token.getValue())
                self.getError(self.followSet["VARDECLARATION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTINUESOS"], " got: " +self.token.getValue())
            self.getError(self.followSet["VARDECLARATION"])

    def continueSos(self):
        if self.token.getValue() == 'struct':
            self.getNextToken()
            if self.dataType():
                self.getNextToken()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting datatype token"+" got: " +self.token.getValue())
                self.getError(self.followSet["VARDECLARATION"])
        elif self.dataType():
            self.getNextToken()
        else:
            print("Error")
    
    def proxVar(self):
        if self.token.getValue() in self.firstSet["CONTINUESOS"] or self.token.getType() in self.firstSet["CONTINUESOS"]:
            self.continueSos()
            if self.token.getType() in self.firstSet["VARID"]:
                self.varId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARID"], " got: " +self.token.getValue())
                self.getError(self.followSet["VARDECLARATION"])
        elif self.token.getValue() == '}':
            self.getNextToken()
        else:
            print("Error")

    def varId(self):
        if self.token.getType() == "IDE":
            self.identificador()
            if self.token.getValue() in self.firstSet["VAREXP"]:
                self.varExp()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VAREXP"], " got: " +self.token.getValue())
                self.getError(self.followSet["VARDECLARATION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: IDE expected")
            self.getError(self.followSet["VARDECLARATION"])

    def varExp(self):
        if self.token.getValue() ==',':
            self.getNextToken()
            if self.token.getType() in self.firstSet["VARID"]:
                self.varId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARID"], " got: " +self.token.getValue())   
                self.getError(self.followSet["VARDECLARATION"])
        elif self.token.getValue() == '=':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                self.verifVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
                self.getError(self.followSet["VARDECLARATION"])
        elif self.token.getValue() == ';':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXVAR"] or self.token.getType() in self.firstSet["PROXVAR"]:
                self.proxVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXVAR"], " got: " +self.token.getValue())
                self.getError(self.followSet["VARDECLARATION"])
        elif self.token.getValue() == '[':
            self.getNextToken()
            if(self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]):
                self.aritmeticOp()
                if self.token.getValue() == ']':
                    self.getNextToken()
                    if self.token.getValue() in self.firstSet["ESTRUTURA"]:
                        self.estrutura()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ESTRUTURA"], " got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ']' "" got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}")

    
    def estrutura(self):
        if self.token.getValue()== '[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["ARITMETICOP"] or  self.token.getType() in self.firstSet["ARITMETICOP"]:
                self.aritmeticOp()
                if self.token.getValue() == ']':
                    self.getNextToken()
                    if self.token.getValue() in self.firstSet["CONTMATRIZ"]:
                        self.contMatriz()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTMATRIZ"], " got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ] "+ " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"], " got: " +self.token.getValue())
        elif self.token.getValue() =='=':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["INITVETOR"]:
                self.initVetor()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["INITVETOR"], " got: " +self.token.getValue())
        elif self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getType() in self.firstSet["VARID"]:
                self.varId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARID"], " got: " +self.token.getValue())
        elif self.token.getValue() == ';':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXVAR"] or self.token.getType() in self.firstSet["PROXVAR"]:
                self.proxVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXVAR"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}")

    def initVetor(self):
        if self.token.getValue() == '[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["PROXVETOR"]:
                    self.proxVetor()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXVETOR"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '['  got: " +self.token.getValue())

    
    def proxVetor(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["PROXVETOR"]:
                    self.proxVetor()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXVETOR"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() ==']':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VERIFVAR"]:
                self.verifVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VERIFVAR"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ',' or ']' got: " +self.token.getValue())

    def contMatriz(self):
        if self.token.getValue() == '=':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["INITMATRIZ"]:
                self.initMatriz()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["INITMATRIZ"], " got: " +self.token.getValue())
        elif self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getType() in self.firstSet["VARID"]:
                self.varId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARID"], " got: " +self.token.getValue())
        elif self.token.getValue() == ';':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXVAR"] or self.token.getType() in self.firstSet["PROXVAR"]:
                self.proxVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXVAR"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}:")

    def initMatriz(self):
        if self.token.getValue() == '[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["MATRIZVALUE"]:
                self.matrizValue()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["MATRIZVALUE"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '[' got: " +self.token.getValue())

    def matrizValue(self):
        if self.token.getValue() == '[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXMATRIZ"]:
                self.proxMatriz()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXMATRIZ"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '[' got: " +self.token.getValue())
    
    def proxMatriz(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["PROXMATRIZ"]:
                    self.proxMatriz()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXMATRIZ"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() == ']':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["NEXT"]:
                self.next()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["NEXT"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def next(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["MATRIZVALUE"]:
                self.matrizValue()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["MATRIZVALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() == ']':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VERIFVAR"]:
                self.verifVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VERIFVAR"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def verifVar(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getType() in self.firstSet["VARID"]:
                self.varId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARID"], " got: " +self.token.getValue())
        elif self.token.getValue() ==';':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXVAR"] or self.token.getType() in self.firstSet["PROXVAR"]:
                self.proxVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXVAR"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def constDeclaration(self):
        if self.token.getValue() =='const':
            self.getNextToken()
            if self.token.getValue() =='{':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["PRIMEIRACONST"] or self.token.getType() in self.firstSet["PRIMEIRACONST"]:
                    self.primeiraConst()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PRIMEIRACONST"], " got: " +self.token.getValue())
                    self.getError(self.followSet["PRIMEIRACONST"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: {self.token.getValue()}")
                self.getError(self.followSet["PRIMEIRACONST"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'const' got: {self.token.getValue()}")
            self.getError(self.followSet["PRIMEIRACONST"])


    def primeiraConst(self):
        if self.token.getValue() in self.firstSet["CONTINUECONSTSOS"] or self.token.getType() in self.firstSet["CONTINUECONSTSOS"]:
            self.continueConstSos()
            if self.token.getType() == "IDE":
                self.constId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONSTID"], " got: " +self.token.getValue())
                self.getError(self.followSet["PRIMEIRACONST"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTINUECONSTSOS"], " got: " +self.token.getValue())
            self.getError(self.followSet["PRIMEIRACONST"])
    
    def continueConstSos(self):
        if self.token.getValue() =='struct':
            self.getNextToken()
            if self.dataType():
                self.getNextToken()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting a datatype token")
        elif self.dataType():
            self.getNextToken()
        else:
            self.token_list.append("ERROR")

    def proxConst(self):
        if self.token.getValue() in self.firstSet["CONTINUECONSTSOS"] or self.token.getType() in self.firstSet["CONTINUECONSTSOS"]:
            self.continueConstSos()
            if self.token.getType() in self.firstSet["CONSTID"]:
                self.constId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONSTID"], " got: " +self.token.getType())
                self.getError(self.followSet["PRIMEIRACONST"])
        elif self.token.getValue() == '}':
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXCONST"], " got: " +self.token.getValue())
    
    def constId(self):
        if self.token.getType() == "IDE":
            self.identificador()
            if self.token.getValue() in self.firstSet["CONSTEXP"]:
                self.constExp()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONSTEXP"], " got: " +self.token.getValue())
                self.getError(self.followSet["PRIMEIRACONST"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token")
    

    def constExp(self):
        if self.token.getValue() =='=':
            self.getNextToken()
            if self.token.getType() in self.firstSet["VALUE"] or self.token.getValue() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["VERIFCONST"]:
                    self.verifConst()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VERIFCONST"], " got: " +self.token.getValue())
                    self.getError(self.followSet["PRIMEIRACONST"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
                self.getError(self.followSet["PRIMEIRACONST"])
        elif self.token.getValue() =='[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
                self.aritimeticOp()
                if self.token.getValue() == ']':
                    self.getNextToken()
                    if self.token.getValue() in self.firstSet["ESTRUTURACONST"]:
                        self.estruturaConst()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ESTRUTURACONST"], " got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ']' token")
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}")

    def estruturaConst(self):
        if self.token.getValue() == '[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
                self.aritimeticOp()
                if self.token.getValue() ==']':
                    self.getNextToken()
                    if self.token.getValue() == '=':
                        self.getNextToken()
                        if self.token.getValue() in self.firstSet["INITCONSTMATRIZ"]:
                            self.initConstMatriz()
                        else:
                            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["INITCONSTMATRIZ"], " got: " +self.token.getValue())
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '=' got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ']' got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"], " got: " +self.token.getValue())
        elif self.token.getValue() == '=':
            self.getNextToken()
            if self.token.getValue() == '[':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                    self.value()
                    if self.token.getValue() in self.firstSet["PROXCONSTVETOR"]:
                        self.proxConstVetor()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXCONSTVETOR"], " got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '[' got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def proxConstVetor(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["PROXCONSTVETOR"]:
                    self.proxConstVetor()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXCONSTVETOR"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() == ']':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VERIFCONST"]:
                self.verifConst()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VERIFCONST"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def initConstMatriz(self):
        if self.token.getValue() =='[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["MATRIZCONSTVALUE"]:
                self.matrizConstValue()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["MATRIZCONSTVALUE"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '[' got: " +self.token.getValue())

    def matrizConstValue(self):
        if self.token.getValue() =='[':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["PROXCONSTMATRIZ"]:
                    self.proxConstMatriz()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXCONSTMATRIZ"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '[' got: " +self.token.getValue())
    
    def proxConstMatriz(self):
        if self.token.getValue() ==',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["PROXCONSTMATRIZ"]:
                    self.proxConstMatriz()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXCONSTMATRIZ"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() == ']':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["NEXTCONST"]:
                self.nextConst()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["NEXTCONST"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def nextConst(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["MATRIZCONSTVALUE"]:
                self.matrizConstValue()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["MATRIZCONSTVALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() == ']':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VERIFCONST"]:
                self.verifConst()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VERIFCONST"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR")

    def verifConst(self):
        if self.token.getValue() ==',':
            self.getNextToken()
            if self.token.getType() in self.firstSet["CONSTID"]:
                self.constId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONSTID"], " got: " +self.token.getValue())
                self.getError(self.followSet["PRIMEIRACONST"])

        elif self.token.getValue() == ';':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXCONST"] or self.token.getType() in self.firstSet["PROXCONST"]:
                self.proxConst()
            else:
                self.token_list.append("ERROR verifConst. Expecting ", self.firstSet["PROXCONST"], " got: " +self.token.getValue())
        else:
            self.token_list.append("ERROR verifConst. Expecting ", self.firstSet["VERIFCONST"], " got: " +self.token.getValue())

    
    def function(self):
        if self.token.getValue() == 'function':
            self.getNextToken()
            if self.dataType():
                self.getNextToken()
                if self.token.getType() == 'IDE':
                    self.getNextToken()
                    if self.token.getValue() =='(':
                        self.getNextToken()
                        if self.token.getValue() in self.firstSet["CONTINUEFUNCTION"] or self.token.getType() in self.firstSet["CONTINUEFUNCTION"]:
                            self.continueFunction()
                        else:
                            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTINUEFUNCTION"], " got: " +self.token.getValue())
                            self.getError(self.followSet["FUNCTION"])
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())
                        self.getError(self.followSet["FUNCTION"])
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting identifier token got: " +self.token.getValue())
                    self.getError(self.followSet["FUNCTION"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting datatype token")
                self.getError(self.followSet["FUNCTION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'function' got: " +self.token.getValue())
            self.getError(self.followSet["FUNCTION"])

    def continueFunction(self):
        if self.token.getValue() in self.firstSet["PARAMETERS"] or self.token.getType() in self.firstSet["PARAMETERS"]:
            self.parameters()
            if self.token.getValue() in self.firstSet["BlockFunction"]:
                self.blockFunction()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BlockFunction"], " got: " +self.token.getValue())
                self.getError(self.followSet["FUNCTION"])
        elif self.token.getValue() == ")":
            self.getNextToken()
            if self.token.getValue() in self.firstSet["BlockFunction"]:
                self.blockFunction()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BlockFunction"], " got: " +self.token.getValue())
                self.getError(self.followSet["FUNCTION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTINUEFUNCTION"], " got: " +self.token.getValue())
            self.getError(self.followSet["FUNCTION"])

    def parameters(self):
        if self.dataType():
            self.getNextToken()
            if self.token.getType() == "IDE":
                self.identificador()
                if self.token.getValue() in self.firstSet["PARAMLOOP"]:
                    self.paramLoop()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PARAMLOOP"], " got: " +self.token.getValue())
                    self.getError(self.followSet["PARAMETERS"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting IDE token, got: " +self.token.getValue())
                self.getError(self.followSet["PARAMETERS"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting datatype token, got: " +self.token.getValue())
            self.getError(self.followSet["PARAMETERS"])
    
    def paramLoop(self):
        if self.token.getValue() == ',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PARAMETERS"] or self.token.getType() in self.firstSet["PARAMETERS"]:
                self.parameters()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PARAMETERS"], " got: " +self.token.getValue())
                self.getError(self.followSet["PARAMETERS"])
        elif self.token.getValue() ==")":
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PARAMLOOP"], " got: " +self.token.getValue())
            self.getError(self.followSet["PARAMETERS"])

    def blockFunction(self):
        if self.token.getValue() =='{':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["BlockFuncContent"] or self.token.getType() in self.firstSet["BlockFuncContent"]:
                self.blockFuncContent()
                if self.token.getValue() == ';':
                    self.getNextToken()
                    if self.token.getValue() == '}':
                        self.getNextToken()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
                        self.getError(self.followSet["FUNCTION"])
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue())
                    self.getError(self.followSet["FUNCTION"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BlockFuncContent"], " got: " +self.token.getValue())
                self.getError(self.followSet["FUNCTION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BlockFunction"], " got: " +self.token.getValue())
            self.getError(self.followSet["FUNCTION"])

    def blockFuncContent(self):
        if self.token.getValue() in self.firstSet["VARDECLARATION"]:
            self.varDeclaration()
            if self.token.getValue() in self.firstSet["CONTENT1"] or self.token.getType() in self.firstSet["CONTENT1"]:
                self.content1()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT1"], " got: " +self.token.getValue())
                self.getError(self.followSet["BlockFuncContent"])
        elif self.token.getValue() in self.firstSet["CONSTDECLARATION"]:
            self.constDeclaration()
            if self.token.getValue() in self.firstSet["CONTENT2"] or self.token.getType() in self.firstSet["CONTENT2"]:
                self.content2()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT2"], " got: " +self.token.getValue())
                self.getError(self.followSet["BlockFuncContent"])
        elif self.token.getValue() in self.firstSet["FUNCCONTENT"] or self.token.getType() in self.firstSet["FUNCCONTENT"]:
            self.funcContent()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BlockFuncContent"], " got: " +self.token.getValue())
            self.getError(self.followSet["BlockFuncContent"])
                        
    def funcContent(self):
        if self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"] :
            self.codigo()
            if self.token.getValue() == "return":
                self.getNextToken()
                if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                    self.value()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}:. Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'return' got: " +self.token.getValue())
                self.getError(self.followSet["FUNCCONTENT"])
        elif self.token.getValue() == "return":
                self.getNextToken()
                if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                    self.value()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
                    self.getError(self.followSet["FUNCCONTENT"])
        else: 
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FUNCCONTENT"], " got: " +self.token.getValue())
            self.getError(self.followSet["FUNCCONTENT"])

    def content1(self):
        if self.token.getValue() in self.firstSet["CONSTDECLARATION"]:
            self.constDeclaration()
            if self.token.getValue() in self.firstSet["CONTENT3"] or self.token.getType() in self.firstSet["CONTENT3"]:
                self.content3()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT3"], " got: " +self.token.getValue())
                self.getError(self.followSet["CONTENT1"])
        elif self.token.getValue() in self.firstSet["FUNCCONTENT"] or self.token.getType() in self.firstSet["FUNCCONTENT"]:
            self.funcContent()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT1"], " got: " +self.token.getValue())
            self.getError(self.followSet["CONTENT1"])

    def content2(self):
        if self.token.getValue() in self.firstSet["VARDECLARATION"]:
            self.varDeclaration()
            if self.token.getValue() in self.firstSet["CONTENT3"] or self.token.getType() in self.firstSet["CONTENT3"]:
                self.content3()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT3"], " got: " +self.token.getValue())
                self.getError(self.followSet["CONTENT2"])     
        elif self.token.getValue() in self.firstSet["FUNCCONTENT"] or self.token.getType() in self.firstSet["FUNCCONTENT"]:
            self.funcContent()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT2"], " got: " +self.token.getValue())
            self.getError(self.followSet["CONTENT2"])


    def content3(self):
        if self.token.getValue() in self.firstSet["FUNCCONTENT"] or self.token.getType() in self.firstSet["FUNCCONTENT"]:
            self.funcContent()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTENT3"], " got: " +self.token.getValue())

    

    def structDeclaration(self):
        if(self.token.getValue() == 'struct'):
            self.getNextToken()
            if(self.token.getType()=="IDE"):
                self.getNextToken()
                if self.token.getValue() in self.firstSet["STRUCTVARS"]:
                    self.structVars()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTVARS"], " got: " +self.token.getValue())
                    self.getError(self.firstSet["INICIO"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token, got: " +self.token.getType())
                self.getError(self.firstSet["INICIO"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTDECLARATION"], " got: " +self.token.getValue())
            self.getError(self.firstSet["INICIO"])
        
    def structVars(self):
        if(self.token.getValue() =='{'):
            self.getNextToken()
            if(self.token.getValue() == 'var'):
                self.getNextToken()
                if(self.token.getValue() =='{'):
                    self.getNextToken()
                    if self.token.getValue() in self.firstSet["FIRSTSTRUCTVAR"] or self.token.getType() in self.firstSet["FIRSTSTRUCTVAR"]:
                        self.firstStructVar()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FIRSTSTRUCTVAR"], " got: " +self.token.getValue())
                        self.getError(self.firstSet["INICIO"])
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: {self.token.getValue()}")
                    self.getError(self.firstSet["INICIO"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'var' got: {self.token.getValue()}")
                self.getError(self.firstSet["INICIO"])

        elif(self.token.getValue() == 'extends'):
            self.getNextToken()
            if(self.token.getType()=="IDE"):
                self.getNextToken()
                if(self.token.getValue() == '{'):
                    self.getNextToken()
                    if(self.token.getValue() == 'var'):
                        self.getNextToken()
                        if(self.token.getValue() == '{'):
                            self.getNextToken()
                            if self.token.getValue() in self.firstSet["FIRSTSTRUCTVAR"] or self.token.getType() in self.firstSet["FIRSTSTRUCTVAR"]:
                                 self.firstStructVar()
                            else:
                                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FIRSTSTRUCTVAR"], " got: " +self.token.getValue())
                                self.getError(self.firstSet["INICIO"])
                        else:
                            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())
                            self.getError(self.firstSet["INICIO"])
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'var' got: " +self.token.getValue())
                        self.getError(self.firstSet["INICIO"])
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())
                    self.getError(self.firstSet["HEADER3"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token,  got: " +self.token.getType())
                self.getError(self.firstSet["INICIO"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTVARS"], " got: " +self.token.getValue())
            self.getError(self.firstSet["INICIO"])

        
    def firstStructVar(self):
        if(self.dataType()):
            self.getNextToken()
            if self.token.getType() == 'IDE':
                self.structVarId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTVARID"], " got: " +self.token.getValue())
                self.getError(self.firstSet["INICIO"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FIRSTSTRUCTVAR"], " got: " +self.token.getValue())
            self.getError(self.firstSet["INICIO"])

    def structVarId(self):
        if(self.token.getType()=="IDE"):
            self.getNextToken()
            if self.token.getValue() in self.firstSet["STRUCTVAREXP"]:
                self.structVarExp()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTVAREXP"], " got: " +self.token.getValue())
                self.getError(self.firstSet["INICIO"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token, got: " +self.token.getType())
            self.getError(self.firstSet["INICIO"])
    
    def structVarExp(self):
        if(self.token.getValue() == ','):
            self.getNextToken()
            if self.token.getType() in self.firstSet["STRUCTVARID"]:
                self.structVarId()
            else:
                self.token_list.append("ERROR structVarExp1. Expecting ", self.firstSet["STRUCTVARID"], " got: " +self.token.getValue())
        elif(self.token.getValue() == ';'):
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXSTRUCTVAR"] or self.token.getType() in self.firstSet["PROXSTRUCTVAR"]:
                self.proxStructVar()
            else:
                self.token_list.append("ERROR structVarExp2. Expecting ", self.firstSet["PROXSTRUCTVAR"], " got: " +self.token.getValue())
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
                    if self.token.getValue() in self.firstSet["CONTSTRUCTMATRIZ"]:
                        self.contStructMatriz()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTSTRUCTMATRIZ"], " got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ']' token got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting integer token, got: " +self.token.getValue())
        elif(self.token.getValue() ==','):
            self.getNextToken()
            if self.token.getType() in self.firstSet["STRUCTVARID"]:
                self.structVarId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTVARID"], " got: " +self.token.getType())
        elif(self.token.getValue() == ';'):
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PROXSTRUCTVAR"] or self.token.getType() in self.firstSet["PROXSTRUCTVAR"]:
                self.proxStructVar()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXSTRUCTVAR"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTMATRIZ"], " got: " +self.token.getValue())


    def proxStructVar(self):
        if(self.dataType()):
            self.getNextToken()
            if self.token.getType() in self.firstSet["STRUCTVARID"]:
                self.structVarId()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["STRUCTVARID"], " got: " +self.token.getValue())
                self.getError(self.firstSet["INICIO"])
        elif(self.token.getValue() == "}"):
            self.getNextToken()
            if(self.token.getValue() == "}"):
                self.getNextToken()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
                self.getError(self.firstSet["INICIO"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROXSTRUCTVAR"], " got: " +self.token.getValue())
            self.getError(self.firstSet["INICIO"])
    
    def opNegate(self):
        if self.token.getValue() == '-':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["ARITMETICVALUE"] or self.token.getType() in self.firstSet["ARITMETICVALUE"]:
                self.aritmeticValue()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICVALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["ARITMETICVALUE"] or self.token.getType() in self.firstSet["ARITMETICVALUE"]:
            self.aritmeticValue()
        elif self.token.getValue() == '(':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
                self.aritimeticOp()
                if self.token.getValue() == ")":
                    self.getNextToken()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ')' got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OpNegate"], " got: " +self.token.getValue())  

    def opMult(self):
        if self.token.getValue() in self.firstSet["OpNegate"] or self.token.getType() in self.firstSet["OpNegate"]:
            self.opNegate()
            if self.token.getValue() in self.firstSet["AUXSTATE2"]:
                self.auxState2()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPMULT"], " got: " +self.token.getValue())
    
    def auxState2(self):
        if self.token.getValue() in self.firstSet["MULTSYMBOL"]:
            self.multSymbol()
            if self.token.getValue() in self.firstSet["Opmult"] or self.token.getType() in self.firstSet["Opmult"]:
                self.opMult()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["Opmult"], " got: " +self.token.getValue())
    
    def multSymbol(self):
        if self.token.getValue() == '*':
            self.getNextToken()
        elif self.token.getValue() == '/':
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["MULTSYMBOL"], " got: " +self.token.getValue())

    def aritimeticOp(self):
        if self.token.getValue() in self.firstSet["Opmult"] or self.token.getType() in self.firstSet["Opmult"]:
            self.opMult()
            if self.token.getValue() in self.firstSet["OPMULT2"]:
                self.opMult2()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITIMETICOP"], " got: " +self.token.getValue())

    def opMult2(self):
        if self.token.getValue() in self.firstSet["ARITSYMBOL"]:
            self.aritSymbol()
            if self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
                self.aritimeticOp()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITMETICOP"], " got: " +self.token.getValue())

    def aritSymbol(self):
        if self.token.getValue() =="+":
            self.getNextToken()
        elif self.token.getValue =='-':
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ARITSYMBOL"], " got: " +self.token.getValue())
    
    def opBoolValue(self):
        if self.token.getValue() in self.firstSet["ARITMETICOP"] or self.token.getType() in self.firstSet["ARITMETICOP"]:
            self.aritimeticOp()
        elif self.token.getValue() == 'true' or self.token.getValue() =='false':
            self.getNextToken()
        elif self.token.getValue() =='(':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["LOGICALOP"] or self.token.getType() in self.firstSet["LOGICALOP"]:
                self.logicalOp()
                if self.token.getValue() ==')':
                    self.getNextToken()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ')' got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["LOGICALOP"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE"], " got: " +self.token.getValue())

    def relacionalOp(self):
        if self.token.getValue() in self.firstSet["OPBOOLVALUE"] or self.token.getType() in self.firstSet["OPBOOLVALUE"]:
            self.opBoolValue()
            if self.token.getValue() in self.firstSet["RELSYMBOL"]:
                self.relSymbol()
                if self.token.getValue() in self.firstSet["OPBOOLVALUE"] or self.token.getType() in self.firstSet["OPBOOLVALUE"]:
                    self.opBoolValue()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["RELSYMBOL"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["RELACIONALOP"], " got: " +self.token.getValue())

    def relSymbol(self):
        if self.token.getValue() =='<':
            self.getNextToken()
        elif self.token.getValue() == '>':
            self.getNextToken()
        elif self.token.getValue() == '==':
            self.getNextToken()
        elif self.token.getValue() == '<=':
            self.getNextToken()
        elif self.token.getValue() == '>=':
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["RELSYMBOL"], " got: " +self.token.getValue())
    
    def opBoolValue2(self):
        if self.token.getValue() in self.firstSet["OPBOOLVALUE"] or self.token.getType() in self.firstSet["OPBOOLVALUE"]:
            self.opBoolValue()
            if self.token.getValue() in self.firstSet["OPBOOLVALUE3"]:
                self.opBoolValue3()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE2"], " got: " +self.token.getValue())
    
    def opBoolValue3(self):
        if self.token.getValue() in self.firstSet["RELSYMBOL"]:
            self.relSymbol()
            if self.token.getValue() in self.firstSet["OPBOOLVALUE"] or self.token.getType() in self.firstSet["OPBOOLVALUE"]:
                self.opBoolValue()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE"], " got: " +self.token.getValue())

    def logicSymbol(self):
        if self.token.getValue() =="!=":
            self.getNextToken()
        elif self.token.getValue() =="&&":
            self.getNextToken()
        elif self.token.getValue()=="||":
            self.getNextToken()
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["LOGICSYMBOL"], " got: " +self.token.getValue())

    def logicalOp(self):
        if self.token.getValue() in self.firstSet["OPBOOLVALUE2"] or self.token.getType() in self.firstSet["OPBOOLVALUE2"]:
            self.opBoolValue2()
            if self.token.getValue() in self.firstSet["LOGICSYMBOL"]:
                self.logicSymbol()
                if self.token.getValue() in self.firstSet["OPBOOLVALUE2"] or self.token.getType() in self.firstSet["OPBOOLVALUE2"]:
                    self.opBoolValue2()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE2"], " got: " +self.token.getValue())
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["LOGICSYMBOL"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["LOGICALOP"], " got: " +self.token.getValue())

    def negBoolValue(self):
        if self.token.getValue() == "!":
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"]:
                self.variavel()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARIAVEL"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["NEGBOOLVALUE"], " got: " +self.token.getValue())

    def incrementOp(self, variavel=True):
        enter = False
        if not variavel:
            enter = True
        if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"] or enter:
            if variavel:
                self.variavel()
            if self.token.getValue() =="++":
                self.getNextToken()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '++' got: " +self.token.getValue())
        elif self.token.getValue() =="++":
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"]:
                self.variavel()
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARIAVEL"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["INCREMENTOP"], " got: " +self.token.getValue())

    def decrementOp(self, variavel = True):
        enter = False
        if not variavel:
            enter = True
        if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"] or enter:
            if variavel:
                self.variavel()
            if self.token.getValue() =="--":
                self.getNextToken()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '--' got: " +self.token.getValue())
        elif self.token.getValue() =="--":
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"]:
                self.variavel()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VARIAVEL"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["DECREMENTOP"], " got: " +self.token.getValue())

    def boolOperations(self):
        if self.token.getValue() in self.firstSet["OPBOOLVALUE"] or self.token.getType() in self.firstSet["OPBOOLVALUE"]:
            self.opBoolValue()
            if self.token.getValue() in self.firstSet["BOOLOPERATIONS2"]:
                self.boolOperations2()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BOOLOPERATIONS2"], " got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["NEGBOOLVALUE"]:
            self.negBoolValue()
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BOOLOPERATIONS"], " got: " +self.token.getValue())

    def boolOperations2(self):
        if self.token.getValue() in self.firstSet["BOOLOPERATIONS3"]:
            self.boolOperations3()
            if self.token.getValue() in self.firstSet["BOOLOPERATIONS4"]:
                self.boolOperations4()
        elif self.token.getValue() in self.firstSet["LOGICSYMBOL"]:
            self.logicSymbol()
            if self.token.getValue() in self.firstSet["OPBOOLVALUE2"] or self.token.getType() in self.firstSet["OPBOOLVALUE2"]:
                self.opBoolValue2()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE2"], " got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BOOLOPERATIONS2"], " got: " +self.token.getValue())

    def boolOperations3(self):
        if self.token.getValue() in self.firstSet["RELSYMBOL"]:
            self.relSymbol()
            if self.token.getValue() in self.firstSet["OPBOOLVALUE"] or self.token.getType() in self.firstSet["OPBOOLVALUE"]:
                self.opBoolValue()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE"], " got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BOOLOPERATIONS3"], " got: " +self.token.getValue())
    
    def boolOperations4(self):
        if self.token.getValue() in self.firstSet["LOGICSYMBOL"]:
            self.logicSymbol()
            if self.token.getValue() in self.firstSet["OPBOOLVALUE2"] or self.token.getType() in self.firstSet["OPBOOLVALUE2"]:
                self.opBoolValue2()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["OPBOOLVALUE2"], " got: " +self.token.getValue())

    
    def typedefDeclaration(self):
        if self.token.getValue() == "typedef":
            self.getNextToken()
            if self.token.getValue() in self.firstSet["CONTTYPEDEFDEC"] or self.token.getType() in self.firstSet["CONTTYPEDEFDEC"]:
                self.contTypedefDeclaration()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTTYPEDEFDEC"], " got: " +self.token.getValue())
                self.getError(self.followSet["TYPEDEFDECLARATION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["TYPEDEFDECLARATION"], " got: " +self.token.getValue())
            self.getError(self.followSet["TYPEDEFDECLARATION"])

    def contTypedefDeclaration(self):
        if self.dataType():
            self.getNextToken()
            if self.token.getType()=="IDE":
                self.getNextToken()
                if self.token.getValue() == ';':
                    self.getNextToken()
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue())
                    self.getError(self.followSet["TYPEDEFDECLARATION"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token, got: " +self.token.getType())
                self.getError(self.followSet["TYPEDEFDECLARATION"])
        elif self.token.getValue() == 'struct':
            self.getNextToken()
            if self.token.getType()=="IDE":
                self.getNextToken()
                if self.token.getType()=="IDE":
                    self.getNextToken()
                    if self.token.getValue() == ';':
                        self.getNextToken()
                    else:
                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue())
                        self.getError(self.followSet["TYPEDEFDECLARATION"])
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token, got: " +self.token.getType())
                    self.getError(self.followSet["TYPEDEFDECLARATION"])
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'IDE' token,' got: " +self.token.getType())
                self.getError(self.followSet["TYPEDEFDECLARATION"])
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTTYPEDEFDEC"], " got: " +self.token.getValue())
            self.getError(self.followSet["TYPEDEFDECLARATION"])


    def procedure(self):
        if self.token.getType() == "IDE":
            self.identificador()
            if self.token.getValue() =="(":
                self.getNextToken()
                if self.token.getValue() in self.firstSet["PROCPARAM"] or self.token.getType() in self.firstSet["PROCPARAM"]:
                    self.procParam()
                    if self.token.getValue() == '{':
                        self.getNextToken()
                        if self.token.getValue() in self.firstSet["PROCCONTENT"] or self.token.getType() in self.firstSet["PROCCONTENT"]:
                            self.procContent()
                        else:
                             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT"], " got: " +self.token.getValue())
                    else:
                         self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCPARAM"], " got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())
        elif self.token.getValue() =='start':
            self.getNextToken()
            if self.token.getValue() == '(':
                self.getNextToken()
                if self.token.getValue() ==')':
                    self.getNextToken()
                    if self.token.getValue() == '{':
                        self.getNextToken()
                        if self.token.getValue() in self.firstSet["PROCCONTENT"] or self.token.getType() in self.firstSet["PROCCONTENT"]:
                            self.procContent()
                        else:
                             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT"], " got: " +self.token.getValue())
                    else:
                         self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())
                else:
                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ')' got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCEDURE"], " got: " +self.token.getValue())

    def procParam(self):
        if self.token.getValue() in self.firstSet["PARAMETERS"] or self.token.getType() in self.firstSet["PARAMETERS"]:
            self.parameters()
        elif self.token.getValue() == ')':
            self.getNextToken()
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCPARAM"], " got: " +self.token.getValue())   

    def procContent(self):
        if self.token.getValue() in self.firstSet["VARDECLARATION"]:
            self.varDeclaration()
            if self.token.getValue() in self.firstSet["PROCCONTENT2"] or self.token.getType() in self.firstSet["PROCCONTENT2"]:
                self.procContent2()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT2"], " got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["CONSTDECLARATION"]:
            self.constDeclaration()
            if self.token.getValue() in self.firstSet["PROCCONTENT3"] or self.token.getType() in self.firstSet["PROCCONTENT3"]:
                self.procContent3()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT3"], " got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
            self.codigo()
            if self.token.getValue() =='}':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT"], " got: " +self.token.getValue())

    def procContent2(self):
        if self.token.getValue() in self.firstSet["CONSTDECLARATION"]:
            self.constDeclaration()
            if self.token.getValue() in self.firstSet["PROCCONTENT4"] or self.token.getType() in self.firstSet["PROCCONTENT4"]:
                self.procContent4()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT4"], " got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
            self.codigo()
            if self.token.getValue() == "}":
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT2"], " got: " +self.token.getValue())

    def procContent3(self):
        if self.token.getValue() in self.firstSet["VARDECLARATION"]:
            self.varDeclaration()
            if self.token.getValue() in self.firstSet["PROCCONTENT4"] or self.token.getType() in self.firstSet["PROCCONTENT4"]:
                self.procContent4()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT4"], " got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
            self.codigo()
            if self.token.getValue() == '}':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT3"], " got: " +self.token.getValue())

    def procContent4(self):
        if self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
            self.codigo()
            if self.token.getValue() == '}':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PROCCONTENT4"], " got: " +self.token.getValue())

    def codigo(self):
        if self.token.getValue() in self.firstSet["COMANDO"] or self.token.getType() in self.firstSet["COMANDO"]:
            self.comando()
            if self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
                self.codigo()

    def comando(self):
        if self.token.getValue() in self.firstSet["PRINT"]:
            self.printFunction()
        elif self.token.getType() in self.firstSet["FUNCTIONCALL"] and self.token.getType() in self.firstSet["ATRIBUICAO"]:
            self.preFuncionAtribuicao()
        elif self.token.getValue() in self.firstSet["ATRIBUICAO"]:
            self.atribuicao()
        elif self.token.getValue() in self.firstSet["READ"]:
            self.read()
        elif self.token.getValue() in self.firstSet["INCREMENTOP"]:
            self.incrementOp()
            if self.token.getValue() ==';':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["DECREMENTOP"] :
            self.decrementOp()
            if self.token.getValue() ==';':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue())
        elif self.token.getValue() in self.firstSet["WHILE"]:
            self.whileFunction()
        elif self.token.getValue() in self.firstSet["CONDITIONAL"]:
            self.conditional()
        elif self.token.getValue() in self.firstSet["TYPEDEFDECLARATION"]:
            self.typedefDeclaration()
        elif self.token.getValue() in self.firstSet["STRUCTDECLARATION"]:
            self.structDeclaration()
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["COMANDO"], " got: " +self.token.getValue())

    def preFuncionAtribuicao(self):
        if self.token.getType() == "IDE":
            self.identificador()
            if self.token.getValue() == '(':
                self.functionCall()
            elif self.token.getValue() == '=':
                self.atribuicao(False)
            elif self.token.getValue() == '++':
                self.incrementOp(False)
                if self.token.getValue() ==';':
                    self.getNextToken()
            elif self.token.getValue() == '--':
                self.decrementOp(False)
                if self.token.getValue() ==';':
                    self.getNextToken()
            


    def printFunction(self):
        if self.token.getValue() == "print":
            self.getNextToken()
            if self.token.getValue() =="(":
                self.getNextToken()
                if self.token.getValue() in self.firstSet["PRINTABLELIST"] or self.token.getType() in self.firstSet["PRINTABLELIST"]:
                    self.printableList()
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PRINTABLELIST"], " got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PRINT"], " got: " +self.token.getValue())
        
    
    def printableList(self):
        if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
            self.value()
            if self.token.getValue() in self.firstSet["NEXTPRINTVALUE"]:
                self.nextPrintValue()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["NEXTPRINTVALUE"], " got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PRINTABLELIST"], " got: " +self.token.getValue())

    def nextPrintValue(self):
        if self.token.getValue() ==',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["PRINTABLELIST"] or self.token.getType() in self.firstSet["PRINTABLELIST"]:
                self.printableList()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["PRINTABLELIST"], " got: " +self.token.getValue())
        elif self.token.getValue() ==')':
            self.getNextToken()
            if self.token.getValue() ==';':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["NEXTPRINTVALUE"], " got: " +self.token.getValue())

    
    def atribuicao(self, variavel=True):
        enter = False
        if not variavel:
            enter = True
        if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"] or enter:
            if variavel:
                self.variavel()
            if self.token.getValue() == '=':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                    self.value()
                    if self.token.getValue() == ';':
                        self.getNextToken()
                    else:
                         self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ';' got: " +self.token.getValue()) 
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
            else: 
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '=' got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["ATRIBUICAO"], " got: " +self.token.getValue())

    def functionCall(self):
        if self.token.getValue() == '(':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["CONTFCALL"] or self.token.getType() in self.firstSet["CONTFCALL"]:
                self.contFCall()
                if self.token.getValue() == ';':
                    self.getNextToken()
            else:
                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTFCALL"], " got: " +self.token.getValue())
        else:
            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())

    def contFCall(self):
        if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
            self.value()
            if self.token.getValue() in self.firstSet["FCALLPARAMS"]:
                self.fCallParams()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FCALLPARAMS"], " got: " +self.token.getValue())
        elif self.token.getValue() == ')':
            self.getNextToken()
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONTFCALL"], " got: " +self.token.getValue())

    def fCallParams(self):
        if self.token.getValue() ==',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["VALUE"] or self.token.getType() in self.firstSet["VALUE"]:
                self.value()
                if self.token.getValue() in self.firstSet["FCALLPARAMS"]:
                    self.fCallParams()
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FCALLPARAMS"], " got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["VALUE"], " got: " +self.token.getValue())
        elif self.token.getValue() == ')':
            self.getNextToken()
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["FCALLPARAMS"], " got: " +self.token.getValue())

    def read(self):
        if self.token.getValue() == 'read':
            self.getNextToken()
            if self.token.getValue() == '(':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["READPARAMS"] or self.token.getType() in self.firstSet["READPARAMS"]:
                    self.readParams()
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["READPARAMS"], " got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["READ"], " got: " +self.token.getValue())

    def readParams(self):
        if self.token.getValue() in self.firstSet["VARIAVEL"] or self.token.getType() in self.firstSet["VARIAVEL"]:
            self.variavel()
            if self.token.getValue() in self.firstSet["READLOOP"]:
                self.readLoop()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["READLOOP"], " got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["READPARAMS"], " got: " +self.token.getValue())
    
    def readLoop(self):
        if self.token.getValue() ==',':
            self.getNextToken()
            if self.token.getValue() in self.firstSet["READPARAMS"] or self.token.getType() in self.firstSet["READPARAMS"]:
                self.readParams()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["READPARAMS"], " got: " +self.token.getValue())
        elif self.token.getValue() ==')':
            self.getNextToken()
            if self.token.getValue() ==';':
                self.getNextToken()
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '; got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["READLOOP"], " got: " +self.token.getValue())


    def whileFunction(self):
        if self.token.getValue() =='while':
            self.getNextToken()
            if self.token.getValue() =='(':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["BOOLOPERATIONS"] or self.token.getType() in self.firstSet["BOOLOPERATIONS"]:
                    self.boolOperations()
                    if self.token.getValue() == ')':
                        self.getNextToken()
                        if self.token.getValue() == '{':
                            self.getNextToken()
                            if self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
                                self.codigo()
                                if self.token.getValue() == '}':
                                    self.getNextToken()
                                else:
                                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
                            else:
                                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CODIGO"], " got: " +self.token.getValue())
                        else:
                             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())
                    else:
                         self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ')' got: " +self.token.getValue())
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BOOLOPERATIONS"], " got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["WHILE"], " got: " +self.token.getValue())
    
    def conditional(self):
        if self.token.getValue() =='if':
            self.getNextToken()
            if self.token.getValue() =='(':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["BOOLOPERATIONS"] or self.token.getType() in self.firstSet["BOOLOPERATIONS"]:
                    self.boolOperations()
                    if self.token.getValue() == ')':
                        self.getNextToken()
                        if self.token.getValue() == 'then':
                            self.getNextToken()
                            if self.token.getValue() == '{':
                                self.getNextToken()
                                if self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
                                    self.codigo()
                                    if self.token.getValue() =='}':
                                        self.getNextToken()
                                    else:
                                        self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
                                else:
                                    self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CODIGO"], " got: " +self.token.getValue())
                            else:
                                self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())
                        else:
                            self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting 'then' got: " +self.token.getValue())

                    else:
                         self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ')' got: " +self.token.getValue())
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["BOOLOPERATIONS"], " got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting '(' got: " +self.token.getValue())
        else:
             self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CONDITIONAL"], " got: " +self.token.getValue())


    def elsePart(self):
        if self.token.getValue() =='else':
            self.getNextToken()
            if self.token.getValue() =='{':
                self.getNextToken()
                if self.token.getValue() in self.firstSet["CODIGO"] or self.token.getType() in self.firstSet["CODIGO"]:
                    self.codigo()
                    if self.token.getValue() == '}':
                        self.getNextToken()
                    else:
                         self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'}'} got: " +self.token.getValue())
                else:
                     self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting ", self.firstSet["CODIGO"], " got: " +self.token.getValue())
            else:
                 self.token_list.append(f"ERROR on line {self.token.current_line}: Expecting {'{'} got: " +self.token.getValue())


    def inteiro(self, token):
        p = re.compile('[0-9],')
        return True if p.match(token) is not None else False

        
   



