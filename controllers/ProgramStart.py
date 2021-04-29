from controllers.Lexical import Lexical
from controllers.Syntactic import Syntactic

import glob

class ProgramStart:
    '''
        ProgramStart: módulo que a depender dos arquivos de entrada irá instanciar
        um objeto de analizador sintático.
    '''
    def __init__(self):
        self.txtfiles = []
        for file in glob.glob("entradas/entrada*.txt"):
            self.txtfiles.append(file)
    def analyze(self):
        for file in self.txtfiles:
            print("----------- Analisando o arquivo {} -----------".format(file))
            lexical = Lexical(file)
            syntactic = Syntactic(lexical)
            syntactic.run()

