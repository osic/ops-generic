import argparse

class ArgParser(object):

    def __init__(self,Description=None):
          if Description is None:
               self.parser = argparse.ArgumentParser()
          else:
               self.parser = argparse.ArgumentParser(description=Description)

    def addRule(self,arg,ifrequired,help_msg):
          self.parser.add_argument(arg,required=ifrequired,help=help_msg)

    def parseArgs(self):
          self.args = self.parser.parse_args()

    def validate(self):
          print "Override this method"

    def getArgs(self):
          return self.args
