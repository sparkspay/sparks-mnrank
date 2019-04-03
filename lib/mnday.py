import requests

calculate_days = 10


def getstat():
    r = requests.get('https://stats.masternode.me/network-report/latest/json')
    return r.json()


def selection_probability(mns, blocks):
    p_pool = mns / 10
    p_prob = 1.0 - ((float(p_pool - 1) / float(p_pool)) ** float(blocks))
    return "{:0.4f}%".format(p_prob * 100)


if __name__ == '__main__':
    print()
    print('getting current masternode count...')
    try:
        api = getstat()
        r = api['raw']
        masternode_count = r['mn_count_enabled']
        block_year = r['block_date'][:4]
        blocks_per_hour = r['avg_blocktimes'][block_year]['per_hr']
    except (requests.ConnectionError, KeyError):
        print('stats api down.')
        print('using made up masternode count of 5000')
        masternode_count = 5000
    print()
    print('using %d current active masternodes' % masternode_count)
    print('estimated proababilities of selection are')
    print()
    print('{0:>5} {1:>5} {2:>8} {3:>8}'.format("days", "hours", "blocks", "prob"))
    for hour in [1, 2, 3, 4, 6, 8, 10, 12, 18, 24, 30, 36, 42, 48] + range(72, 72 + (24 * (calculate_days - 2)), 24):
        blocks = int(blocks_per_hour * hour)
        day = float(hour) / float(24)
        print('{0:>5.2f} {1:>5} {2:>8} {3:>8}'.format(day, hour, blocks, selection_probability(masternode_count, blocks)))