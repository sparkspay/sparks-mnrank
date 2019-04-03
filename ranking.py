#!/bin/python3

import lib.mnrank
from lib.coin import Coin
from lib.arguments import largs
import lib.mnstat as mnstat

arguments = largs.evaluateargs()

if 'na' in arguments or arguments['f'] is not False or 'q' in arguments:
    Coin.buildfiles()
    lib.mnrank.printoutput()

if 's' in arguments:
    mnstat.printoutputs()


