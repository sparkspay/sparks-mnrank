#!/usr/bin/python3

from mnrank import Coin
import collections


mn_dict = Coin.clicmd('masternode list')

inter_list = []
for i in mn_dict:
    inter_list.append(mn_dict[i]['status'])

counter=collections.Counter(inter_list)

print(counter)

