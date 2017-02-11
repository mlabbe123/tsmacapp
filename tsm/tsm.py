import ac
import traceback
import os

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

try:
    from tsm.steam_utils.steam_info import get_steam_username, get_steam_id
except:
    ac.log('TheSetupMarket logs | error loading get_steam_username, get_steam_id: ' + traceback.format_exc())
    raise

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

#######################################
# Functions for setups download section
#######################################
def getSetups(car_code, currentTrackBaseName, currentTrackLayout):
    try:
        resp = requests.get('http://thesetupmarket.com/api/get-setups-for-app/')
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | error requesting setups from tsm api: ' + str(e))

    try:
        setups = resp.json()
    except Exception as e:
        ac.log('TheSetupMarket logs | error  resp.json(): ' + str(e))


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
def downloadSetup(setup_id, setup_file_name, car_ac_code, track_baseName, track_layout, refreshSetupsListingTable):
    url = "http://thesetupmarket.com/setup_files/55c2cddddebcbba924bb2a34/" + setup_id + "/"

    path_to_save = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName + '\\' + setup_file_name

    try:
        r = requests.get(url)
    except:
        ac.log('TheSetupMarket logs | downloadSetup failed at r = requests.get(url)')
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

    refreshSetupsListingTable()


#######################################
# Functions for setups upload section
#######################################
def getAllSetupsFromFolder(car_ac_code, track_baseName):
    # List setup files in current track folder
    try:
        allSetupFiles = os.listdir(get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName)
        ac.log('TheSetupMarket logs | getAllSetupsFromFolder: all setups in folder = ' + str(allSetupFiles))
    except:
        ac.log('TheSetupMarket logs | getAllSetupsFromFolder failed at allSetupFiles = os.listdir')
        return []

    # Build a new list without all files downloaded by the app (files starting with TSM)
    allSetupFilesNotTSM = []

    for setupFile in allSetupFiles:
        if 'TSM-ac' not in setupFile:
            allSetupFilesNotTSM.append(setupFile)

    ac.log('TheSetupMarket logs | all setups in folder not TSM: ' + str(allSetupFilesNotTSM))

    return allSetupFilesNotTSM


# def filterSetups(setupList, predicateName, predicateValue):
#     filteredSetupList = []
#
#     for setup in setupList:
#         if setup[predicateName] == predicateValue:
#             filteredSetupList.append(setup)
#
#     return filteredSetupList

def uploadSetup(userTSMId, ac_version, user_steamId, filename, trim, baseline, car_id, track_id, car_ac_code, track_baseName, track_layout):

    if track_layout != '':
        track_ac_code = track_baseName + '-' + track_layout
    else:
        track_ac_code = track_baseName

    ac.log('TheSetupMarket logs | uploadSetup params: ' + str(filename) + ', ' + str(trim) + ', ' +  str(baseline) + ', ' + str(car_id) + ', ' + str(track_id))

    filepath = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName + '\\' + filename
    ac.log('TheSetupMarket logs | uploadSetup filepath: ' + str(filepath))

    # params for API call
    url = 'http://thesetupmarket.com/api/create-setup/'
    file = {'file': open(filepath, 'rb')}
    sim_id = '55c2cddddebcbba924bb2a34'

    if baseline:
        track_id = '55db6db13cc3a26dcae7116d'
    else:
        track_id = track_id

    trim = trim.lower()

    try:
        r = requests.post(url, files=file, data={'file_name': filename, 'sim_id': sim_id, 'sim_version': ac_version,
        'user_id': userTSMId, 'car_id': car_id, 'track_id': track_id, 'trim': trim, 'best_laptime': '', 'comments': ''})
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | uploadSetup request failed! Status code: ' + str(e))


    if r.status_code == 200:
        ac.log('TheSetupMarket logs | upload request success! Status code: ' + str(r.status_code))
        return True
    else:
        ac.log('TheSetupMarket logs | upload request failed! Status code: ' + str(r.status_code))
        ac.log('TheSetupMarket logs | upload request failed! text: ' + str(r.text))
        ac.log('TheSetupMarket logs | upload request failed! content: ' + str(r.content))
        return False


def getUserSetups(userTSMId, car_id, track_id):
    try:
        resp = requests.get('http://thesetupmarket.com/api/get-setups-by-user/' + userTSMId)
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | getUserSetups error request!: ' + str(e))

    try:
        setups = resp.json()
    except Exception as e:
        ac.log('TheSetupMarket logs | getUserSetups error resp.json(): ' + str(e))
        setups = []

    trackSpecificSetups = []
    otherTrackSetups = []

    for setup in setups:
        if setup['car']['_id'] == car_id:
            if setup['track']['_id'] == track_id or setup['track']['_id'] == '55db6db13cc3a26dcae7116d':
                trackSpecificSetups.append(setup)
            else:
                otherTrackSetups.append(setup)

    categorizedSetupsObj = {}
    categorizedSetupsObj['trackSpecific'] = list(reversed(trackSpecificSetups))
    categorizedSetupsObj['otherTracks'] = list(reversed(otherTrackSetups))

    return categorizedSetupsObj


@async
def getSetupDetails(setupId, callback):
    try:
        resp = requests.get('http://thesetupmarket.com/api/get-setup/' + setupId)
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | error requesting user setup details from tsm api: ' + str(e))

    try:
        setupDetail = resp.json()
    except Exception as e:
        ac.log('TheSetupMarket logs | error requesting user setups from tsm api: ' + str(e))

    callback(setupDetail)

    return setupDetail

# Setup.update({_id: request.body.setup_id}, {sim_version: request.body.sim_version, type: request.body.trim, best_time: request.body.best_laptime, comments: request.body.comments}, function(err, numAffected) {
@async
def updateSetup(car_ac_code, track_baseName, file_name, setup_id, car_id, track_id, sim_version, trim, baseline, best_time, comments, callback):
    filepath = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName + '\\' + file_name
    ac.log('TheSetupMarket logs | updateSetup filepath: ' + str(filepath))

    # params for API call
    url = 'http://thesetupmarket.com/api/update-setup-with-file/'
    file = {'file': open(filepath, 'rb')}
    sim_id = '55c2cddddebcbba924bb2a34'

    if baseline:
        track_id = '55db6db13cc3a26dcae7116d'

    trim = trim.lower()

    try:
        r = requests.post(url, files=file,
                          data={'sim_id': sim_id, 'setup_id': setup_id, 'file_name': file_name, 'sim_version': sim_version,
                                'car_id': car_id, 'track_id': track_id, 'trim': trim, 'best_laptime': best_time, 'comments': comments})
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | updateSetup error request!: ' + str(e))


    if r.status_code == 200:
        ac.log('TheSetupMarket logs | update request success! Status code: ' + str(r.status_code))
        returnMessage = 'Setup successfully updated'
    else:
        ac.log('TheSetupMarket logs | update request failed! Status code: ' + str(r.status_code))
        ac.log('TheSetupMarket logs | update request failed! text: ' + str(r.text))
        ac.log('TheSetupMarket logs | update request failed! content: ' + str(r.content))
        returnMessage = 'Error updating setup'

    callback(returnMessage)


@async
def sendSetupRating(userSteamId, setupId, userRating):
    url = 'http://thesetupmarket.com/api/update-setup-rating-from-app/'

    try:
        r = requests.post(url, data={'userSteamId': userSteamId, 'userRating': userRating, 'setupId': setupId})
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | sendSetupRating error request!: ' + str(e))

    if r.status_code == 200:
        ac.log('TheSetupMarket logs | sendSetupRating request success! Status code: ' + str(r.status_code))
    else:
        ac.log('TheSetupMarket logs | sendSetupRating request failed! Status code: ' + str(r.status_code))
        ac.log('TheSetupMarket logs | sendSetupRating request failed! text: ' + str(r.text))
        ac.log('TheSetupMarket logs | sendSetupRating request failed! content: ' + str(r.content))


#######################################
# Utilitary functions
#######################################
def get_personal_folder():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        return buf.value
    else:
        raise Exception('TheSetupMarket logs | Could not find "Documents" folder')


# def extract_sim_version(setup):
#     try:
#         return setup['sim_version']
#     except KeyError:
#         return 0

def get_ac_version_from_api():
    url = 'http://thesetupmarket.com/api/get-sim-infos/Assetto%20Corsa'

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | get_ac_version_from_api error request!: ' + str(e))


    if r.status_code == 200:
        try:
            request_json = r.json()
            ac_versions = request_json['versions']
            ac_current_version = ac_versions[-1]
        except:
            ac.log('TheSetupMarket logs | get_ac_version_from_api failed at request_json = r.json()')
            ac_current_version = False
    else:
        ac.log('TheSetupMarket logs | get_ac_version_from_api failed. status_code = ' + str(r.status_code))
        ac_current_version = False

    return ac_current_version


def get_carid_from_api(ac_code):
    url = 'http://thesetupmarket.com/api/get-car-by-accode/' + ac_code

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | get_carid_from_api error request!: ' + str(e))

    if r.status_code == 200:
        try:
            request_json = r.json()
            carId = request_json['_id']
        except:
            carId = False

    else:
        ac.log('TheSetupMarket logs | get_carid_from_api failed. status_code = ' + str(r.status_code))
        carId = False

    return carId


def get_trackid_from_api(ac_code):
    url = 'http://thesetupmarket.com/api/get-track-by-accode/' + ac_code

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | get_trackid_from_api error request!: ' + str(e))

    if r.status_code == 200:
        try:
            request_json = r.json()
            trackId = request_json['_id']
        except:
            trackId = False
    else:
        ac.log('TheSetupMarket logs | get_trackid_from_api failed. status_code = ' + str(r.status_code))
        trackId = False

    return trackId


def getUserTSMIdWithSteamID(steamID):
    url = 'http://thesetupmarket.com/api/get-user-by-steamId/' + str(steamID)
    userTSMId = False

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        ac.log('TheSetupMarket logs | getUserTSMIdWithSteamID error request!: ' + str(e))

    if r.status_code == 200:
        try:
            request_json = r.json()
            userTSMId = request_json['_id']
        except:
            ac.log('TheSetupMarket logs | getUserTSMIdWithSteamID failed at request_json = r.json() = ')
    else:
        ac.log('TheSetupMarket logs | getUserTSMIdWithSteamID failed. status_code = ' + str(r.status_code))
        return '502'

    return userTSMId


def getUserSteamId():
    return get_steam_id()


def getUserSteamUsername():
    return get_steam_username()