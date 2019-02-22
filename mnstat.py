#!/usr/bin/python3

from mnrank import Coin
import collections

mn_dict = Coin.clicmd('masternode list')

mn_list = []
for i in mn_dict:
    mn_list.append(mn_dict[i]['status'])

version_list = []
for i in mn_dict:
    version_list.append(mn_dict[i]['daemonversion'])

protocol_list = []
for i in mn_dict:
    protocol_list.append(mn_dict[i]['protocol'])

count_mn = collections.Counter(mn_list)
count_version = collections.Counter(version_list)
count_protocol = collections.Counter(protocol_list)


def summns(collection):
    sum = 0
    for i in collection:
        sum = sum + collection[i]

    return sum


sum_mn = summns(count_mn)


print('{:<40s}'.format('STATUS'), end='\n')
print('{:=<40s}'.format(''), end='\n')

for i in count_mn:
    print('{:<25s}'.format(i), end=': ')
    print('{:>5s}'.format(str(count_mn[i])), end=' ')
    print('{:>5s}'.format(str(int(round(count_mn[i]/sum_mn*100, 0)))), end='%\n')

print('{:-<40s}'.format(''), end='\n\n')
print('{:<40s}'.format('VERSION'), end='\n')
print('{:=<40s}'.format(''), end='\n')

for i in count_version:
    print('{:<25s}'.format(i), end=': ')
    print('{:>5s}'.format(str(count_version[i])), end=' ')
    print('{:>5s}'.format(str(int(round(count_version[i]/sum_mn*100, 0)))), end='%\n')

print('{:-<40s}'.format(''), end='\n\n')
print('{:<40s}'.format('PROTOCOL'), end='\n')
print('{:=<40s}'.format(''), end='\n')

for i in count_protocol:
    print('{:<25s}'.format(str(i)), end=': ')
    print('{:>5s}'.format(str(count_protocol[i])), end=' ')
    print('{:>5s}'.format(str(int(round(count_protocol[i]/sum_mn*100, 0)))), end='%\n')

print('{:-<40s}'.format(''), end='\n\n')
