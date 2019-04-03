import getopt
import sys
from lib.colors import bcolors


class largs:


    @classmethod
    def evaluateargs(cls):
        fullCmdArguments = sys.argv
        argumentList = fullCmdArguments[1:]
        unixOptions = "hf:slq"
        gnuOptions = ["help", "file=", "stats", "listconf"]
        args = {'f': False}

        try:
            arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
            if not arguments:
                args = {'f': False, 'na': True}
                return args

        except getopt.error as err:
            # output error, and return with an error code
            cls.printhelp()
            sys.exit(2)

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                cls.printhelp()
                sys.exit(2)
            elif currentArgument in ("-l", "--listconf"):
                cls.printconf()
                sys.exit(2)
            elif currentArgument in ("-s", "--stats"):
                args.update({'s': True})
            elif currentArgument in ("-f", "--file"):
                args['f'] = currentValue
            elif currentArgument in ("-q", "--query"):
                args.update({'q': True})

        return args

    @classmethod
    def printhelp(cls):
        print('{:<25}'.format(bcolors.BOLD + '-h / --help' + bcolors.ENDC), end=' ')
        print('{:<25}'.format(bcolors.BOLD + ': this help' + bcolors.ENDC), end=' \n')
        print('{:<25}'.format(bcolors.BOLD + '-f / --file' + bcolors.ENDC), end=' ')
        print('{:<25}'.format(bcolors.BOLD + ': config file [mn_conf.json]' + bcolors.ENDC), end=' \n')
        print('{:<25}'.format(bcolors.BOLD + '-s / --stats' + bcolors.ENDC), end=' ')
        print('{:<25}'.format(bcolors.BOLD + ': mnstats' + bcolors.ENDC), end=' \n')
        print('{:<25}'.format(bcolors.BOLD + '-l / --listconf' + bcolors.ENDC), end=' ')
        print('{:<25}'.format(bcolors.BOLD + ': list configfile' + bcolors.ENDC), end=' \n')
        print('{:<25}'.format(bcolors.BOLD + '-q / --query' + bcolors.ENDC), end=' ')
        print('{:<25}'.format(bcolors.BOLD + ': list masternodes' + bcolors.ENDC), end=' \n')


    @classmethod
    def printconf(cls):
        file = open("./config/coin.conf","r")
        print(file.read())




