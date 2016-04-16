import ac
import traceback

try:
    import ctypes.wintypes
except:
    ac.log('TheSetupMarket logs | error loading ctypes.wintypes: ' + traceback.format_exc())
    raise

from ctypes.wintypes import MAX_PATH

# TODO: read from config file for filters | IMPORTS
from os.path import dirname, realpath
#import configparser

import functools
import threading


def async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t
    return wrapper


try:
    from tsm_libraries import requests
except Exception as e:
    ac.log('TheSetupMarket logs | error loading requests: ' + traceback.format_exc())
    raise


# TODO: read from config file for filters
#config_path = dirname(realpath(__file__))

#config_ini_file = config_path + '/../config/config.ini'

#config = configparser.ConfigParser()
#config.read(config_ini_file, encoding='utf-8')
#config.sections()
#sim_versions = config['filters']['SimVersion']


def getSetups(car_code, currentTrackBaseName, currentTrackLayout):
    try:
        resp = requests.get('http://thesetupmarket.com/api/get-setups-for-app/')
        setups = resp.json()
    except Exception as e:
        ac.log('TheSetupMarket logs | error requesting setups from tsm api: ' + traceback.format_exc())

    trackSpecificSetups = []
    anyTracksSetups = []
    otherTrackSetups = []

    # TODO: sort and filter setups with config file
    #ac.log(str(setups.sort(key=extract_sim_version)))

    for setup in setups:

        if setup['car']['ac_code'] == car_code:
            if currentTrackBaseName in setup['track']['ac_code']:
                trackSpecificSetups.append(setup)
            elif setup['track']['_id'] == '55db6db13cc3a26dcae7116d':
                anyTracksSetups.append(setup)
            elif not currentTrackBaseName in setup['track']['ac_code'] and setup['track']['_id'] != '55db6db13cc3a26dcae7116d':
                otherTrackSetups.append(setup)

    categorizedSetupsObj = {}
    categorizedSetupsObj['trackSpecific'] = list(reversed(trackSpecificSetups))
    categorizedSetupsObj['anyTracks'] = list(reversed(anyTracksSetups))
    categorizedSetupsObj['otherTracks'] = list(reversed(otherTrackSetups))

    return categorizedSetupsObj


@async
def downloadSetup(setup_id, setup_file_name, car_ac_code, track_baseName, track_layout):
    url = "http://thesetupmarket.com/setup_files/55c2cddddebcbba924bb2a34/" + setup_id + "/"

    path_to_save = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName + '\\' + setup_file_name

    try:
        r = requests.get(url)
    except:
        ac.console('TheSetupMarket logs | failed at r = requests.get(url)')
        r = {}
        r['status_code'] = ''

    if r.status_code == 200:
        try:
            with open(path_to_save, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=1):
                    fd.write(chunk)
        except:
            ac.log('TheSetupMarket logs | could not find folder to save')

    else:
        ac.log('TheSetupMarket logs | setupid: ' + setup_id + 'error while downloading')


# Thank you rivali tempo devs...
def get_personal_folder():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        return buf.value
    else:
        raise Exception('Could not find "Documents" folder')


# def filterSetups(setupList, predicateName, predicateValue):
#     filteredSetupList = []
#
#     for setup in setupList:
#         if setup[predicateName] == predicateValue:
#             filteredSetupList.append(setup)
#
#     return filteredSetupList


# def extract_sim_version(setup):
#     try:
#         return setup['sim_version']
#     except KeyError:
#         return 0
