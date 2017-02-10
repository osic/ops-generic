import sys
sys.path.append('../common/')

from ArgParser import ArgParser

class childArgParser(ArgParser):
   #Overridden method
   def validate():
      print "Validating environment"

parser = ArgParser()
parser.validate()

auth = Authentication()
