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

mn_counter=collections.Counter(mn_list)
count_version = collections.Counter(version_list)
count_protocol = collections.Counter(protocol_list)

print(mn_counter)
print(count_version)
print(count_protocol)

