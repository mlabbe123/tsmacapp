import ac
import os
import traceback
import ctypes.wintypes
from ctypes.wintypes import MAX_PATH
from os.path import dirname, realpath
#import configparser
from operator import itemgetter, attrgetter, methodcaller
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
    import requests
except Exception as e:
    ac.log('TheSetupMarket logs | error loading requests: '+traceback.format_exc())

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
    ac.log('TheSetupMarket logs | car_code: '+car_code)
    ac.log('TheSetupMarket logs | track_code: '+currentTrackBaseName + '-' + currentTrackLayout)

    try:
        resp = requests.get('http://thesetupmarket.com/api/get-setups-for-app/')
        setups = resp.json()
    except Exception as e:
        ac.log('TheSetupMarket logs | error requesting setups from tsm api: ' + traceback.format_exc())

    trackSpecificSetups = []
    anyTracksSetups = []
    otherTrackSetups = []

    # Get current track full name, matching the DB ac_code.
    # if ac.getTrackConfiguration(0) != '':
    #     currentTrackFullName = currentTrackBaseName + '-' + currentTrackLayout
    # else:
    #     currentTrackFullName = currentTrackBaseName

    #ac.log(str(setups.sort(key=extract_sim_version)))

    for setup in setups:

        if setup['car']['ac_code'] == car_code:
            if currentTrackBaseName in setup['track']['ac_code']:
                trackSpecificSetups.append(setup)
            elif setup['track']['_id'] == '55db6db13cc3a26dcae7116d':
                anyTracksSetups.append(setup)
            elif not currentTrackBaseName in setup['track']['ac_code'] and setup['track']['_id'] != '55db6db13cc3a26dcae7116d':
                otherTrackSetups.append(setup)

    ac.log('TheSetupMarket logs | trackSpecificSetups count: ' + str(len(trackSpecificSetups)))
    ac.log('TheSetupMarket logs | anyTracksSetups count: ' + str(len(anyTracksSetups)))
    ac.log('TheSetupMarket logs | otherTrackSetups count: ' + str(len(otherTrackSetups)))

    categorizedSetupsObj = {}
    categorizedSetupsObj['trackSpecific'] = list(reversed(trackSpecificSetups))
    categorizedSetupsObj['anyTracks'] = list(reversed(anyTracksSetups))
    categorizedSetupsObj['otherTracks'] = list(reversed(otherTrackSetups))

    return categorizedSetupsObj


@async
def downloadSetup(setup_id, setup_file_name, car_ac_code, track_baseName, track_layout):
    ac.log('Download --> setupId: ' + str(setup_id) + ' | filename: ' + setup_file_name)

    url = "http://thesetupmarket.com/setup_files/55c2cddddebcbba924bb2a34/" + setup_id + "/"

    # Thank you rivali tempo devs...
    path_to_save = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName + '\\' + setup_file_name

    r = requests.get(url)

    if r.status_code == 200:
        ac.console('TheSetupMarket logs | setupid: ' + setup_id + ' downloaded')
        try:
            ac.log('TheSetupMarket logs | trying path_to_save: ' + path_to_save)
            with open(path_to_save, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=1):
                    fd.write(chunk)
        except:
            ac.log('TheSetupMarket logs | could not find folder to save')

    else:
        ac.log('TheSetupMarket logs | setupid: ' + setup_id + 'error while downloading')


def filterSetups(setupList, predicateName, predicateValue):
    filteredSetupList = []

    for setup in setupList:
        if setup[predicateName] == predicateValue:
            filteredSetupList.append(setup)

    return filteredSetupList


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


def uploadSetup(filename, trim, baseline, car_ac_code, track_baseName, track_layout):

    if track_layout != '':
        track_ac_code = track_baseName + '-' + track_layout
    else:
        track_ac_code = track_baseName

    ac.log('TheSetupMarket logs | uploadSetup params: ' + str(filename) + ', ' + str(trim) + ', ' +  str(baseline) + ', ' + str(car_ac_code) + ', ' + str(track_ac_code))

    filepath = get_personal_folder() + r'\Assetto Corsa\setups' + '\\' + car_ac_code + '\\' + track_baseName + '\\' + filename
    ac.log('TheSetupMarket logs | uploadSetup filepath: ' + str(filepath))

    # params for API call
    url = 'http://thesetupmarket.com/api/create-setup/'
    file = {'file': open(filepath, 'rb')}
    sim_id = '55c2cddddebcbba924bb2a34'
    # TODO: Find a way to find current sim version
    sim_version = '1.5'
    # TODO: Find the user steamID, then map it to a user_id
    user_id = '55c2cba1a39491a1247e72df'
    # TODO: Get the car_id from the car_ac_code
    car_id = '5617c467314a9b764c43d3c9' # This is the car_id for the R8 LMS Ultra
    # TODO: Get the track_id from the track_ac_code
    if baseline:
        track_id = '55db6db13cc3a26dcae7116d'
    else:
        track_id = '55c370982fd0d7166d97cf99' # This is the track_id for Nordschleife Endurance
    trim = trim.lower()

    r = requests.post(url, files=file, data={'file_name': filename, 'sim_id': sim_id, 'sim_version': sim_version, 'user_id': user_id, 'car_id': car_id, 'track_id': track_id, 'trim': trim, 'best_laptime': '', 'comments': ''})

    if r.status_code == 200:
        ac.log('TheSetupMarket logs | upload request success! Status code: ' + str(r.status_code))
    else:
        ac.log('TheSetupMarket logs | upload request failed! Status code: ' + str(r.status_code))
        ac.log('TheSetupMarket logs | upload request failed! text: ' + str(r.text))
        ac.log('TheSetupMarket logs | upload request failed! content: ' + str(r.content))

    # API is expecting:
    # -------
    # fd.append('file', setup.file);
    # fd.append('file_name', setup.file.name);
    # fd.append('sim_id', setup.sim.id)
    # fd.append('sim_version', setup.sim.versions[setup.sim.versions.length - 1]);
    # fd.append('user_id', setup.author_userid);
    # fd.append('car_id', setup.car._id);
    # fd.append('track_id', setup.track._id);
    # fd.append('trim', setup.trim);
    # fd.append('best_laptime', setup.best_laptime || '');
    # fd.append('comments', setup.comments || '');


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


def extract_sim_version(setup):
    try:
        return setup['sim_version']
    except KeyError:
        return 0

def get_ac_version_from_api():
    url = 'http://thesetupmarket.com/api/get-sim-infos/Assetto%20Corsa'

    r = requests.get(url)

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

    r = requests.get(url)

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

    r = requests.get(url)

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


def getUserSteamCommunityIDFromLog():
    logFilePath = get_personal_folder() + r'\Assetto Corsa\logs\log.txt'

    userSteamCommunityID = False

    with open(logFilePath) as infile:
        for line in infile:
            if 'Steam Community ID' in line:
                userSteamCommunityID = str(line).replace('Steam Community ID: ', '')

    return userSteamCommunityID


def checkIfUserExistsOnTSM(userSteamCommunityID):
    ac.log('TheSetupMarket logs | checkIfUserExistsOnTSM top')
    userExists = False

    url = 'http://thesetupmarket.com/api/get-user-by-sci/' + userSteamCommunityID

    r = requests.get(url)

    if r.status_code == 200:
        ac.log('TheSetupMarket logs | checkIfUserExistsOnTSM status = 200')
        try:
            ac.log('TheSetupMarket logs | checkIfUserExistsOnTSM try request_json = r.json()' + str(r))
            request_json = r.json()

            if len(request_json) == 1:
                userExists = True
        except:
            ac.log('TheSetupMarket logs | checkIfUserExistsOnTSM failed at request_json = r.json()')

    return userExists
