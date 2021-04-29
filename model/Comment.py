from model.Token import Token

class Comment(Token):
    def __init__(self, value):
        Token.__init__(self,value)

    def isInlineComment(self):
        return (self.value=='//')
    
    def isBlockComment(self):
        return (self.value=='/*')
    
    def isEndInlineComment(self, currentChar):
        return self.isBreakLine(currentChar)

    def isEndBlockComment(self, term):
        return (term=='*/')
    '''
        Retorno: 
                 inválido -  CoMF - Comentário Mal Formado
    '''
    
    def returnValue(self, current_line):
        self.type = 'CoMF'
        self.current_line = current_line
        return self.getToken()