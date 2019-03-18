#!/bin/python3

import lib.mnrank
from lib.coin import Coin
from lib.arguments import largs
import lib.mnstat as mnstat

arguments = largs.evaluateargs()
print(arguments)

if 'na' in arguments or False != arguments['f']:
    Coin.buildfiles()
    lib.mnrank.printoutput()

if 's' in arguments:
    mnstat.printoutputs()


