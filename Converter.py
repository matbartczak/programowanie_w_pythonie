import os 
import subprocess

class Converter():
    
    def __init__(self):
        self.input_file = ''

    def set(self, value):
        self.input_file = value

    def get(self):
        return self.input_file

    def from_mobi(self, out_format = 'epub'):
        if not "mobi" in self.input_file:
            return "This in not a mobi format."
        if not out_format in ('epub','pdf'):
            return "Output file can only by pdf or epub."
        file_name = os.path.split(self.input_file)[1]
        file_name = file_name.split(".")[0]

        subprocess.run(["ebook-convert", self.input_file, os.path.join( os.getcwd(),f'{file_name}.{out_format}') ])

    def from_epub(self, out_format = 'mobi'):
        if not "epub" in self.input_file:
            return "This in not a epub format."
        if not out_format in ('mobi','pdf'):
            return "Output file can only by pdf or mobi."
        
        file_name = os.path.split(self.input_file)[1]
        file_name = file_name.split(".")[0]

        subprocess.run(["ebook-convert", self.input_file, os.path.join( os.getcwd(),f'{file_name}.{out_format}') ])

    def from_pdf(self, out_format = 'mobi'):
        if not "pdf" in self.input_file:
            return "This in not a pdf format."
        if not out_format in ('mobi','epub'):
            return "Output file can only by epub or mobi."
        
        file_name = os.path.split(self.input_file)[1]
        file_name = file_name.split(".")[0]

        subprocess.run(["ebook-convert", self.input_file, os.path.join( os.getcwd(),f'{file_name}.{out_format}') ])
