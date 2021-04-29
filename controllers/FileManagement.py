import re
class FileManagement:
    def __init__(self, filename):
        self.filename = filename
        self.filecontent = ''

    def read_file(self):
        with open(self.filename, 'r', encoding='utf-8') as arquivo:
            for line in arquivo:
                if line=='\n':
                    self.filecontent+='\n'
                else:
                    self.filecontent+=line
        return self.filecontent

    def print_file(self,content):
        file_number = re.findall(r'\d+',self.filename)
        with open('saida/saida{}.txt'.format(file_number[0]),'w',encoding='utf-8') as arquivo:
            for cont in content:
                arquivo.write(cont.strip())
                arquivo.write('\n')
            

        
    
        