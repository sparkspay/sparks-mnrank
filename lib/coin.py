import json
import subprocess
from collections import OrderedDict
from pathlib import Path
import time
import os
import datetime
import sys
import tempfile
from lib.arguments import largs


class Coin:
    # PARAMETERS #
    cache_time_min = 3
    coin_cli = 'sparks-cli'
    std_conf_file = 'mn_conf.json'
    tdir = tempfile.gettempdir()

    # Config_file = tdir+'/mn.conf'
    list_file = tdir + '/mn_list.json'

    # output_file = tdir+'/mn_output.json'
    _now_ = int(datetime.datetime.now().strftime("%s"))

    conf_file = largs.evaluateargs()['f']
    #exit()


    @classmethod
    def checkmnsync(cls):
        check = cls.clicmd('mnsync status')

        if not check['IsSynced']:
            print('you need to wait till mn is synced')
            quit()

        return True

    @classmethod
    def buildfiles(cls):

        cls.checkmnsync()
        if not cls.conf_file:
            cls.conf_file = 'mn_conf.json'

        if cls.conf_file != cls.std_conf_file and cls.fileage(cls.conf_file) == 0:
            cls.stdconf(cls.conf_file)

        if cls.fileage(cls.conf_file) == 0:
            cls.writefile(cls.conf_file, Coin.clicmd(
                'masternode list-conf', hook='conf-hook'))



        if cls.fileage(cls.list_file) == 0 or cls.fileage(cls.list_file) >= cls.cache_time_min:
            cls.writefile(cls.list_file, Coin.clicmd('masternode list'))

    @classmethod
    def stdconf(cls, filename=''):

        if filename == '':
            filename = cls.list_file

        _stdconf_dict = {
            'seed1_mn': '80.211.65.29',
            'seed2_mn': '80.211.57.4',
            'seed3_mn': '51.15.112.11',
            'seed4_mn': '94.177.176.181',
        }

        cls.writefile(filename, _stdconf_dict)

    @classmethod
    def clicmd(cls, cmd, hook=''):
        try:
            cli_output = subprocess.check_output(
                cls.coin_cli + ' ' + cmd, shell=True).decode("utf-8")

            if hook == 'conf-hook':
                iter_num = 0
                output = ""
                iter_string = ""
                mnconf_json = {}
                # masternode list-conf INDEX HOOK makes name-ip json
                for i in cli_output.split('\"masternode\"'):
                    if iter_num != 0:
                        iter_string = '\"' + str(iter_num) + '\"'

                    output = "".join([output, iter_string + ' ' + i])
                    iter_num = iter_num + 1

                output_json = json.loads(output, object_pairs_hook=OrderedDict)

                for i in output_json:
                    mnconf_json[output_json[i]['alias']] = output_json[i]['address'].split(':')[
                        0]
                return mnconf_json

            cli_output = json.loads(cli_output, object_pairs_hook=OrderedDict)
            return cli_output
        except subprocess.CalledProcessError:
            quit()

    @staticmethod
    def fileage(filename):
        exists = Path(filename)
        if exists.is_file():
            age = time.time() - os.path.getmtime(filename)
        else:
            age = 0
        # returns age in minutes
        return age / 60

    @classmethod
    def writefile(cls, filename, data, sort_keys=True, indent=4):

        file_age = cls.fileage(filename)
        if file_age > cls.cache_time_min or file_age == 0:
            Path(filename).write_text(json.dumps(
                data, sort_keys=sort_keys, indent=indent))
        return ()

    @classmethod
    def rankcalc(cls, lastpaidtime, activeseconds):
        if int(lastpaidtime) == 0:
            rank = activeseconds
        else:
            delta = cls._now_ - lastpaidtime
            if delta >= int(activeseconds):
                rank = activeseconds
            else:
                rank = delta
        return rank

    @classmethod
    def filteranks(cls, dictdata, mndata):
        r_data = {}
        pos_data = {}
        mn_conf_ips = []
        for i in mndata:
            mn_conf_ips.append(mndata[i].split(':')[0])

        for i in dictdata:
            status = dictdata[i]['status']
            ip = dictdata[i]['address'].split(':')[0]

            if ip in mn_conf_ips:
                r_data[i] = dictdata[i]
                pos_data[i] = cls.rankcalc(
                    dictdata[i]['lastpaidtime'], dictdata[i]['activeseconds'])
            elif status == 'ENABLED' or status == 'SENTINEL_PING_EXPIRED':
                r_data[i] = dictdata[i]
                pos_data[i] = cls.rankcalc(
                    dictdata[i]['lastpaidtime'], dictdata[i]['activeseconds'])

        # sort pos_data to get position
        sorted_pos_data = sorted(
            pos_data.items(), key=lambda kv: kv[1], reverse=True)

        sorted_list = []
        for i in sorted_pos_data:
            sorted_list.append(i[0])

        for i in sorted_list:
            r_data[i] = dictdata[i]
            r_data[i]['pos'] = sorted_list.index(i)

        return r_data

    @staticmethod
    def openfile(filename):
        exists = Path(filename)
        if exists.is_file():
            _file = open(filename, 'r')
            _file_dic = json.load(_file, object_pairs_hook=OrderedDict)
            _file.close()
            return _file_dic

        return dict()

    @classmethod
    def ip2txid(cls, list_dict, conf_dict):
        ip_name = {}
        ip_pos = {}
        ip_txid = {}
        r_data = {}

        for i in conf_dict:
            ip_name[conf_dict[i]] = i

        for i in list_dict:
            ip_txid[list_dict[i]['address'].split(':')[0]] = i
            ip_pos[list_dict[i]['address'].split(':')[0]] = list_dict[i]['pos']

        for i in ip_name:
            if i in ip_pos:
                r_data[ip_pos[i]] = [ip_txid[i], ip_name[i]]
            else:
                print('WARNING the IP <' + i + '> is not in mnlist')

        return r_data

    @staticmethod
    def timeCalc(time):
        if time > 0:
            day = time // (24 * 3600)
            time = time % (24 * 3600)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            return str(str(day).zfill(2) + 'd ' + str(hour).zfill(2) + ':' + str(minutes).zfill(2))
        else:
            return str('00d 00:00')
