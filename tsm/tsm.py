import ac
import os
import traceback
import ctypes.wintypes
from ctypes.wintypes import MAX_PATH
from os.path import dirname, realpath
import configparser
from operator import itemgetter, attrgetter, methodcaller

try: 
    import requests
except Exception as e:
    ac.log('TheSetupMarket logs | error loading requests: '+traceback.format_exc())

config_path = dirname(realpath(__file__))

config_ini_file = config_path + '/../config/config.ini'

config = configparser.ConfigParser()
config.read(config_ini_file, encoding='utf-8')
config.sections()
sim_versions = config['filters']['SimVersion']

def getSetups(car_code, track_code):

    try:
        resp = requests.get('http://thesetupmarket.com/api/get-setups-for-app/')
        setups = resp.json()
    except Exception as e:
        ac.log('TheSetupMarket logs | error requesting setups from tsm api: '+traceback.format_exc())

    trackSpecificSetups = []
    anyTracksSetups = []
    otherTrackSetups = []

    #ac.log(str(setups.sort(key=extract_sim_version)))

    for setup in setups:
        # trackSpecificSetups.append(setup)
        # anyTracksSetups.append(setup)
        # otherTrackSetups.append(setup)

        if setup['car']['ac_code'] == car_code:
            if setup['track']['ac_code'] == track_code:
                trackSpecificSetups.append(setup)
            elif setup['track']['_id'] == '55db6db13cc3a26dcae7116d':
                anyTracksSetups.append(setup)
            elif setup['track']['ac_code'] != track_code and setup['track']['_id'] != '55db6db13cc3a26dcae7116d':
                otherTrackSetups.append(setup)

    categorizedSetupsObj = {}
    categorizedSetupsObj['trackSpecific'] = filterSetups(trackSpecificSetups, 'sim_version', '1.3')
    categorizedSetupsObj['anyTracks'] = filterSetups(anyTracksSetups, 'sim_version', '1.3')
    categorizedSetupsObj['otherTracks'] = filterSetups(otherTrackSetups, 'sim_version', '1.3')

    return categorizedSetupsObj


def downloadSetup(setup_id, setup_file_name, car_ac_code, track_ac_code):

    url = "http://thesetupmarket.com/setup_files/55c2cddddebcbba924bb2a34/" + setup_id + "/"

    # Other very akward and non working ways to get Documents folder
    #path_to_save = os.path.expanduser(r'~\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_ac_code + '\\' + setup_file_name)

    # CSIDL_PERSONAL = 5       # My Documents
    # SHGFP_TYPE_CURRENT = 1   # Get current, not default value
    # buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    # ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    # path_to_save = buf.value + r'~\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_ac_code + '\\' + setup_file_name

    #path_to_save = 'E:/Mes documents/Assetto Corsa/setups/ferrari_458_gt2/spa/'+setup_file_name

    # Thank you rivali tempo devs...
    path_to_save = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_ac_code + '\\' + setup_file_name

    r = requests.get(url)

    if r.status_code == 200:
        ac.console('TheSetupMarket logs | setupid: ' + setup_id + ' downloaded')
        with open(path_to_save, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1):
                fd.write(chunk)
    else:
        ac.log('TheSetupMarket logs | setupid: ' + setup_id + 'error while downloading')

def get_personal_folder():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        return buf.value
    else:
        raise Exception('Could not find "Documents" folder')

def filterSetups(setupList, predicateName, predicateValue):
    filteredSetupList = []

    for setup in setupList:
        if setup[predicateName] == predicateValue:
            filteredSetupList.append(setup)

    return filteredSetupList

def extract_sim_version(setup):
    try:
        return setup['sim_version']
    except KeyError:
        return 0