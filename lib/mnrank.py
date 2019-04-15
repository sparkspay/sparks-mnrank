#!/usr/bin/python3

from lib.coin import Coin
from collections import OrderedDict
import datetime
from lib.colors import bcolors



def printoutput(aindex = False):
    list_dict = Coin.openfile(Coin.list_file)
    conf_dict = Coin.openfile(Coin.conf_file)
    list_dict_filtered = Coin.filteranks(list_dict, conf_dict)

    list_dict_txid = Coin.ip2txid(list_dict_filtered, conf_dict)
    list_dict_txid_reversed = OrderedDict(
        reversed(list(list_dict_txid.items())))

    # rename for easy lines
    _output = list_dict_txid_reversed
    _list = list_dict_filtered
    _max_rank = len(_list)
    now = int(datetime.datetime.now().strftime("%s"))


    print (Coin.getaddressbalance('GSR6AY8GCW8KUf7N5FGz4xxdZpZ3sWkfrR'))

    # BEGIN
    print('{:-<169}'.format(bcolors.HEADER + '' + bcolors.ENDC), end=' \n')

    # HEADER
    print('{:<1s}'.format(bcolors.ENDC + '|'), end=' ')
    print('{:<25}'.format(bcolors.BOLD + bcolors.HEADER + 'Masternode' + bcolors.ENDC), end=' ')
    print('{:<25}'.format(bcolors.BOLD + 'IP-Address' + bcolors.ENDC), end=' ')
    print('{:>4s}'.format('MAX'), end=' ')
    print('{:1s}'.format('|'), end=' ')
    print('{:>4s}'.format('PO'), end=' ')
    print('{:>3s}'.format(''), end='')
    print('{:<1s}'.format('%'), end=' ')
    print('{:>3s}'.format('|'), end=' ')
    print('{:>15s}'.format(bcolors.OKGREEN + 'Proto' + bcolors.ENDC), end=' ')
    print('{:>1s}'.format('|'), end=' ')
    print('{:<18s}'.format(bcolors.OKGREEN + 'sentinel' + bcolors.ENDC), end=' ')
    print('{:1s}'.format('|'), end=' ')
    print('{:<18s}'.format(bcolors.OKGREEN + 'daemon' + bcolors.ENDC), end=' ')
    print('{:1s}'.format('|'), end=' ')
    print('{:<18s}'.format(bcolors.OKBLUE + 'lastpaid' + bcolors.ENDC), end=' ')
    print('{:1s}'.format('|'), end=' ')
    print('{:<31s}'.format(bcolors.OKBLUE + 'status' + bcolors.ENDC), end=' ')
    print('{:1s}'.format('|'), end=' ')
    print('{:<43s}'.format(bcolors.OKBLUE + 'payee' + bcolors.ENDC), end=' |\n')

    # END
    print('{:-<169}'.format(bcolors.HEADER + bcolors.ENDC), end='\n')

    for line in sorted(_output, reverse=False):
        txid = _output[line][0]
        _name = _output[line][1]
        _out = _list[txid]

        position = _out['pos'] / _max_rank * 100
        pcol = _out['protocol'] > 20208 and bcolors.OKGREEN or bcolors.FAIL
        scol = _out['sentinelversion'] == '1.2.0' and bcolors.OKGREEN or bcolors.FAIL
        stcol = _out['status'] == 'ENABLED' and bcolors.OKGREEN or bcolors.FAIL
        dcol = bcolors.FAIL

        if _out['daemonversion'] == '0.12.4':
            dcol = bcolors.OKGREEN
        elif _out['daemonversion'] == '0.12.3.6':
            dcol = bcolors.OKBLUE

        paycol = bcolors.OKBLUE

        last_paid_time_h = Coin.timeCalc(now - _out['lastpaidtime'])
        balance = float(Coin.getaddressbalance(_out['payee'])['balance']/100000000)


        print('{:<1s}'.format(bcolors.ENDC + '|'), end=' ')
        print('{:<25}'.format(bcolors.BOLD + bcolors.OKBLUE + _name + bcolors.ENDC), end=' ')
        print('{:<25}'.format(bcolors.BOLD + _out['address'].split(':')[0] + bcolors.ENDC), end=' ')
        print('{:4d}'.format(_max_rank), end=' ')
        print('{:1s}'.format('|'), end=' ')
        print('{:>4d}'.format(_out['pos']), end=' ')
        print('{:>3d}'.format(round(position)), end='')
        print('{:<1s}'.format('%'), end=' ')
        print('{:>3s}'.format('|'), end=' ')
        print('{:>15s}'.format(pcol + str(_out['protocol']) + bcolors.ENDC), end=' ')
        print('{:>1s}'.format('|'), end=' ')
        print('{:<18s}'.format(scol + str(_out['sentinelversion']) + bcolors.ENDC), end=' ')
        print('{:1s}'.format('|'), end=' ')
        print('{:<18s}'.format(dcol + str(_out['daemonversion']) + bcolors.ENDC), end=' ')
        print('{:1s}'.format('|'), end=' ')
        print('{:<18s}'.format(paycol + last_paid_time_h + bcolors.ENDC), end=' ')
        print('{:1s}'.format('|'), end=' ')
        print('{:<28s}'.format(stcol + str(_out['status'])), end=bcolors.ENDC + '')
        print('{:1s}'.format('|'), end=' ')
        print('{:<32s}'.format(stcol + str(_out['payee'])), end=bcolors.ENDC + '')
        print('{:1s}'.format('|'), end=' ')
        print('{:<32s}'.format(stcol + str(balance)), end=bcolors.ENDC + ' | \n')

    print('{:-<169}'.format(bcolors.HEADER + bcolors.ENDC), end='\n')
    print('amountof listed MASTERNODES [' + str(len(conf_dict)) + ']')


def main():
    #Coin.buildfiles()
    printoutput()


if __name__ == "__main__":
    main()
