# Import de builtin modules, and insert them into the os path.
import sys
import os
import platform
if platform.architecture()[0] == "64bit":
  sysdir = "stdlib64"
else:
  sysdir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tsm", sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import ac
import traceback
import math
import time
import functools
import threading
from collections import OrderedDict

importError = False

try:
	from tsm import tsm
except Exception as e:
    ac.log('TheSetupMarket logs | error loading tsm module: ' + traceback.format_exc())
    importError = True

try:
	from tsm import GUIhelpers
except Exception as e:
    ac.log('TheSetupMarket logs | error loading tsm GUIhelpers module: ' + traceback.format_exc())
    importError = True

try:
    from config import GUIConfig
except Exception as e:
    ac.log('TheSetupMarket logs | error loading GUIConfig module: ' + traceback.format_exc())
    importError = True


def async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t
    return wrapper


@async
def checkIfServerDown():
    global setups

    if tsm.getUserTSMIdWithSteamID('0') == '502':
        ac.log('TheSetupMarket logs | Server is down')
        initAppWithError('SERVER_DOWN')
        return "The Setup Market"
    else:
        ac.log('TheSetupMarket logs | Server is up!')
        ac.setVisible(fetchingServerLabel, 0)

        # Set the base GUI
        initGUI(appWindow)

        # Init upload section variables
        initUploadSection()

        # Get setups for current car and track.
        setups = tsm.getSetups(currentCarName, currentTrackBaseName, currentTrackLayout)

        refreshSetupsListingTable()


def acMain(ac_version):
    global appWindow, currentCarName, currentTrackBaseName, currentTrackLayout, activeSetupType

    appWindow = ac.newApp("The Setup Market")
    ac.setSize(appWindow, 800, 420)

    if importError:
        ac.log('TheSetupMarket logs | errors in imports')
        initAppWithError()
        return "The Setup Market"

    checkIfServerDown()

    # Get current c\/track/layout.
    currentCarName = ac.getCarName(0)
    currentTrackBaseName = ac.getTrackName(0)
    currentTrackLayout = ac.getTrackConfiguration(0)
    # Set the default active setup type
    activeSetupType = 'trackSpecific'

    initAppWithLoadingState()


def initUploadSection():
    global userSteamId, userTSMId, allSetupsFileNamesInFolder, currentUploadFileName, currentUpdateFileName, currentUploadTrim, currentUploadBaseline, uploadAvailability, current_ac_version, current_carId, current_trackId, userTSMSetups

    ##########################
    # Set the static variables
    ##########################
    uploadAvailability = True
    currentUploadTrim = 'Qualy'
    currentUploadBaseline = False

    if currentTrackLayout != '':
        track_ac_code = currentTrackBaseName + '-' + currentTrackLayout
    else:
        track_ac_code = currentTrackBaseName

    ##########################
    # Set the dynamic variables
    ##########################

    # Get the user steamID
    userSteamId = tsm.getUserSteamId()
    ac.log('TheSetupMarket logs | userSteamId = ' + str(userSteamId))

    # Get the user TSM id
    userTSMId = tsm.getUserTSMIdWithSteamID(userSteamId)
    ac.log('TheSetupMarket logs | userTSMId = ' + str(userTSMId))

    # Get the active AC version
    current_ac_version = tsm.get_ac_version_from_api()
    ac.log('TheSetupMarket logs | current_ac_version = ' + str(current_ac_version))

    # Get the carID for the currentCarName
    current_carId = tsm.get_carid_from_api(currentCarName)
    ac.log('TheSetupMarket logs | current_carId = ' + str(current_carId))

    # Get the trackID for the track_ac_code
    current_trackId = tsm.get_trackid_from_api(track_ac_code)
    ac.log('TheSetupMarket logs | current_trackId = ' + str(current_trackId))

    # Get all the files names in the current track folder
    allSetupsFileNamesInFolder = tsm.getAllSetupsFromFolder(currentCarName, currentTrackBaseName)

    # Set the current upload filename
    if len(allSetupsFileNamesInFolder) > 0:
        currentUploadFileName = allSetupsFileNamesInFolder[0]
        currentUpdateFileName = allSetupsFileNamesInFolder[0]
    else:
        currentUploadFileName = 'No file in track folder'
        currentUpdateFileName = 'No file in track folder'

    # Check if we have errors that would break the upload function. If so, disable uploading.
    if not current_ac_version or not current_carId or not current_trackId or len(allSetupsFileNamesInFolder) == 0 or not userSteamId or not userTSMId:
        ac.log('TheSetupMarket logs | disabling uploading...')
        uploadAvailability = False
        userTSMSetups = []
    else:
        # Get all users uploaded setups
        userTSMSetups = tsm.getUserSetups(userTSMId, current_carId, current_trackId)

    # Prepare the upload section GUI.
    initUploadSectionGUI()

    # Put the right GUI config and values.
    refreshUploadSection()


def acUpdate(delta_t):
    doNothing = 1


def initAppWithError(state='IMPORT_ERROR'):
    ac.setVisible(fetchingServerLabel, 0)

    if state=='IMPORT_ERROR':
        appImportErrorLabel = ac.addLabel(appWindow, 'There has been an error loading the app.')
        ac.setPosition(appImportErrorLabel, 0, 90)
        ac.setSize(appImportErrorLabel, 800, 22)
        ac.setFontAlignment(appImportErrorLabel, 'center')

        appImportErrorLabel2 = ac.addLabel(appWindow, 'You can look in "Documents/Assetto Corsa/logs/py_log.txt", search for "TheSetupMarket logs"')
        ac.setPosition(appImportErrorLabel2, 0, 150)
        ac.setSize(appImportErrorLabel2, 800, 22)
        ac.setFontAlignment(appImportErrorLabel2, 'center')

        appImportErrorLabel3 = ac.addLabel(appWindow, 'and post the results in The Setup Market App thread on the AC forums, section apps.')
        ac.setPosition(appImportErrorLabel3, 0, 172)
        ac.setSize(appImportErrorLabel3, 800, 22)
        ac.setFontAlignment(appImportErrorLabel3, 'center')

        appImportErrorLabel4 = ac.addLabel(appWindow, 'Sorry for the inconvenience.')
        ac.setPosition(appImportErrorLabel4, 0, 232)
        ac.setSize(appImportErrorLabel4, 800, 22)
        ac.setFontAlignment(appImportErrorLabel4, 'center')
    elif state=='SERVER_DOWN':
        appImportErrorLabel = ac.addLabel(appWindow, 'The server is down, sorry for the inconvenience.')
        ac.setPosition(appImportErrorLabel, 0, 172)
        ac.setSize(appImportErrorLabel, 800, 22)
        ac.setFontAlignment(appImportErrorLabel, 'center')


def initAppWithLoadingState():
    global fetchingServerLabel

    fetchingServerLabel = ac.addLabel(appWindow, 'Fetching server...')
    ac.setPosition(fetchingServerLabel, 0, 172)
    ac.setSize(fetchingServerLabel, 800, 22)
    ac.setFontAlignment(fetchingServerLabel, 'center')

def initGUI(appWindow):
    global section1Title, listingTable, listingTableMisc, listingTablePageSpinner, listingTableSetupTypeButton, activeSetupType, updateListingTable, listingUpdateTableMisc, uploadSectionGeneralElements, uploadSectionElements, updateSectionElements, currentUploadTrim, currentUploadBaseline, userSetupListingTable

    # Initialize the listing tables empty and loading labels.
    listingTableMisc = {
        'emptyRowLabel': {
            'label': ac.addLabel(appWindow, ''),
            'text': 'No setups for current car and track'
        },
        'loadingLabel': {
            'label': ac.addLabel(appWindow, ''),
            'text': 'Loading...'
        }
    }

    # Initialize the listing tables.
    listingTable = OrderedDict([
        (1, {
            'dl_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'author_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'bestlap_cell': ac.addLabel(appWindow, ''),
            'rating_cell': ac.addLabel(appWindow, ''),
            'downloads_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (2, {
            'dl_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'author_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'bestlap_cell': ac.addLabel(appWindow, ''),
            'rating_cell': ac.addLabel(appWindow, ''),
            'downloads_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (3, {
            'dl_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'author_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'bestlap_cell': ac.addLabel(appWindow, ''),
            'rating_cell': ac.addLabel(appWindow, ''),
            'downloads_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (4, {
            'dl_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'author_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'bestlap_cell': ac.addLabel(appWindow, ''),
            'rating_cell': ac.addLabel(appWindow, ''),
            'downloads_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (5, {
            'dl_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'author_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'bestlap_cell': ac.addLabel(appWindow, ''),
            'rating_cell': ac.addLabel(appWindow, ''),
            'downloads_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        })
    ])

    # Set the GUI elements for the general upload section
    uploadSectionGeneralElements = {
        'uploadTypeSwitcherButton': ac.addLabel(appWindow, ''),
        'updateTypeSwitcherButton': ac.addLabel(appWindow, '')
        # 'deleteTypeSwitcherButton': ac.addLabel(appWindow, '')
    }

    # Set the GUI elements for the upload NEW setup section
    uploadSectionElements = {
        'refreshUploadGUIButton': ac.addButton(appWindow, ''),
        'fileSelectorButtonLabel': ac.addLabel(appWindow, ''),
        'fileSelectorButton': ac.addButton(appWindow, ''),
        'trimSelectorButtonLabel': ac.addLabel(appWindow, ''),
        'trimSelectorButton': ac.addButton(appWindow, ''),
        'baselineSelectorButtonLabel': ac.addLabel(appWindow, ''),
        'baselineSelectorButton': ac.addButton(appWindow, ''),
        'uploadButton': ac.addButton(appWindow, ''),
        'uploadMessageLabel': ac.addLabel(appWindow, '')
    }

    # Set the GUI elements for the upload UPDATE existing setup section
    updateSectionElements = {
        'refreshUpdateGUIButton': ac.addButton(appWindow, ''),
        'listingTableFilenameHeader': ac.addLabel(appWindow, ''),
        'listingTableTrackHeader': ac.addLabel(appWindow, ''),
        'listingTableTrimHeader': ac.addLabel(appWindow, ''),
        'listingTableAcVersionHeader': ac.addLabel(appWindow, ''),
        'listingTableSetupVersionHeader': ac.addLabel(appWindow, ''),
        'fileSelectorButton': ac.addButton(appWindow, ''),
        'trimSelectorRaceButton': ac.addButton(appWindow, ''),
        'trimSelectorQualyButton': ac.addButton(appWindow, ''),
        'trimSelectorBaseButton': ac.addButton(appWindow, ''),
        'baselineSelectorButton': ac.addButton(appWindow, ''),
        'uploadButton': ac.addButton(appWindow, ''),
        'uploadMessageLabel': ac.addLabel(appWindow, ''),
        'updateMessageLabel': ac.addLabel(appWindow, ''),
        'updateOptionsMessageLabel': ac.addLabel(appWindow, 'Select a setup on the left.')
    }

    # Initialize the listing tables.
    updateListingTable = OrderedDict([
        (1, {
            'select_cell': ac.addLabel(appWindow, ''),
            'file_name_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (2, {
            'select_cell': ac.addLabel(appWindow, ''),
            'file_name_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (3, {
            'select_cell': ac.addLabel(appWindow, ''),
            'file_name_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (4, {
            'select_cell': ac.addLabel(appWindow, ''),
            'file_name_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        }),
        (5, {
            'select_cell': ac.addLabel(appWindow, ''),
            'file_name_cell': ac.addLabel(appWindow, ''),
            'track_cell': ac.addLabel(appWindow, ''),
            'trim_cell': ac.addLabel(appWindow, ''),
            'acversion_cell': ac.addLabel(appWindow, ''),
            'version_cell': ac.addLabel(appWindow, '')
        })
    ])

    listingUpdateTableMisc = {
        'emptyRowLabel': {
            'label': ac.addLabel(appWindow, ''),
            'text': 'No setups for current car and track'
        },
        'loadingLabel': {
            'label': ac.addLabel(appWindow, ''),
            'text': 'Loading...'
        }
    }

    ###################################
    ### Download section            ###
    ###################################

    ### Current track section ###
    section1Title = ac.addLabel(appWindow, "Download")
    ac.setPosition(section1Title, 30, 31)

    # Setting up the refresh setups button
    refreshSetupsButton = ac.addButton(appWindow, '')
    ac.setPosition(refreshSetupsButton, 725, 30)
    ac.setSize(refreshSetupsButton, 70, 20)
    ac.setText(refreshSetupsButton, 'Refresh')
    ac.setVisible(refreshSetupsButton, 1)
    ac.setBackgroundColor(refreshSetupsButton, 1, 1, 1)
    ac.setFontColor(refreshSetupsButton, 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(refreshSetupsButton, 1)
    ac.drawBackground(refreshSetupsButton, 1)
    ac.drawBorder(refreshSetupsButton, 0)
    ac.addOnClickedListener(refreshSetupsButton, onRefreshSetupsButtonClick)

    # Add header row for track specific setups table
    addTableCell('Track', 250, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 30, 53, 'center', False)
    addTableCell('Author', 185, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 275, 53, 'center', False)
    addTableCell('Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 460, 53, 'center', False)
    addTableCell('Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 510, 53, 'center', False)
    addTableCell('Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 595, 53, 'center', False)
    addTableCell('Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 665, 53, 'center', False)
    addTableCell('AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 705, 53, 'center', False)
    addTableCell('Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 735, 53, 'center', False)

    # Init the setups listing table with empty labels
    yPos = GUIConfig.GUIConstants['tableLayout']['startingYPosition']
    rowNumber = 1

    for key, cells in listingTable.items():

        for cellId, label in cells.items():
            ac.setPosition(label, GUIConfig.GUIConstants['tableLayout']['xPos'][cellId], yPos)
            ac.setText(label, '')
            ac.setSize(label, GUIConfig.GUIConstants['tableLayout']['cellXSize'][cellId], GUIConfig.GUIConstants['tableLayout']['cellHeight'])
            ac.setBackgroundColor(label, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'B'])
            ac.setBackgroundOpacity(label, 1)
            ac.drawBackground(label, 1)
            ac.drawBorder(label, 0)
            ac.setVisible(label, 0)
            ac.setFontAlignment(label, 'center')

            if cellId == 'dl_cell':
                if rowNumber == 1:
                    ac.addOnClickedListener(label, onDownloadButton1Clicked)
                elif rowNumber == 2:
                    ac.addOnClickedListener(label, onDownloadButton2Clicked)
                elif rowNumber == 3:
                    ac.addOnClickedListener(label, onDownloadButton3Clicked)
                elif rowNumber == 4:
                    ac.addOnClickedListener(label, onDownloadButton4Clicked)
                elif rowNumber == 5:
                    ac.addOnClickedListener(label, onDownloadButton5Clicked)


        yPos += GUIConfig.GUIConstants['tableLayout']['cellHeight'] + 1
        rowNumber += 1

    for labelName, labelConfig in listingTableMisc.items():
        labelCtrl = labelConfig['label']
        labelText = labelConfig['text']

        ac.setText(labelCtrl, labelText)
        ac.setPosition(labelCtrl, 5, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + GUIConfig.GUIConstants['tableLayout']['cellHeight'] * 2)
        ac.setSize(labelCtrl, 780, GUIConfig.GUIConstants['tableLayout']['cellHeight'])
        ac.drawBorder(labelCtrl, 0)
        ac.setVisible(labelCtrl, 0)
        ac.setFontAlignment(labelCtrl, 'center')

    # Setting up the setups listing setup type button
    listingTableSetupTypeButton = ac.addButton(appWindow, '')
    ac.setPosition(listingTableSetupTypeButton, 5, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + 115)
    ac.setSize(listingTableSetupTypeButton, 140, 22)
    ac.setText(listingTableSetupTypeButton, 'Current Track')
    ac.setBackgroundColor(listingTableSetupTypeButton, 1, 1, 1)
    ac.setFontColor(listingTableSetupTypeButton, 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(listingTableSetupTypeButton, 1)
    ac.drawBackground(listingTableSetupTypeButton, 1)
    ac.drawBorder(listingTableSetupTypeButton, 0)
    ac.addOnClickedListener(listingTableSetupTypeButton, onListingTableSetupTypeButtonClick)

    # Setting up the setups listing table page spinner
    listingTablePageSpinner = ac.addSpinner(appWindow, '')
    ac.setPosition(listingTablePageSpinner, 735, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + 114)
    ac.setSize(listingTablePageSpinner, 60, 20)
    ac.setVisible(listingTablePageSpinner, 0)

    # SEPARATOR
    separator = ac.addLabel(appWindow, '')
    ac.setSize(separator, 800, 2)
    ac.setBackgroundColor(separator, 1, 1, 1)
    ac.setBackgroundOpacity(separator, 1)
    ac.drawBackground(separator, 1)
    ac.drawBorder(separator, 0)
    ac.setVisible(separator, 1)
    ac.setPosition(separator, 0, 218)

    # Add upload section title
    # section4Title = ac.addLabel(appWindow, "/Upload setup")
    # ac.setPosition(section4Title, 10, 235)

    # Add reset upload section button
    ac.setPosition(uploadSectionElements['refreshUploadGUIButton'], 720, 226)
    ac.setSize(uploadSectionElements['refreshUploadGUIButton'], 70, 22)
    ac.setText(uploadSectionElements['refreshUploadGUIButton'], 'Refresh')
    ac.setBackgroundColor(uploadSectionElements['refreshUploadGUIButton'], 1, 1, 1)
    ac.setFontColor(uploadSectionElements['refreshUploadGUIButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(uploadSectionElements['refreshUploadGUIButton'], 1)
    ac.drawBackground(uploadSectionElements['refreshUploadGUIButton'], 1)
    ac.drawBorder(uploadSectionElements['refreshUploadGUIButton'], 0)
    ac.addOnClickedListener(uploadSectionElements['refreshUploadGUIButton'], onRefreshUploadSectionButtonClick)
    ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 0)


def initUploadSectionGUI():
    global updateListingTablePageSpinner

    ac.log('TheSetupMarket logs | initUploadSectionGUI: Init the upload section GUI')

    # Configure the button to switch to Upload
    ac.setPosition(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 336, 226)
    ac.setSize(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 60, 22)
    ac.setText(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 'Upload')
    ac.setBackgroundColor(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 1, 1, 1)
    ac.setFontColor(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 1)
    ac.drawBackground(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 1)
    ac.drawBorder(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 0)
    ac.addOnClickedListener(uploadSectionGeneralElements['uploadTypeSwitcherButton'], onUploadTypeSwitcherButtonClick)
    ac.setFontAlignment(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 'center')

    if uploadAvailability:
        ac.setVisible(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 1)
    else:
        ac.setVisible(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 0)

    # Configure the button to switch to Update
    ac.setPosition(uploadSectionGeneralElements['updateTypeSwitcherButton'], 396, 226)
    ac.setSize(uploadSectionGeneralElements['updateTypeSwitcherButton'], 60, 22)
    ac.setText(uploadSectionGeneralElements['updateTypeSwitcherButton'], 'Update')
    ac.setBackgroundColor(uploadSectionGeneralElements['updateTypeSwitcherButton'], 0, 0, 0)
    ac.setFontColor(uploadSectionGeneralElements['updateTypeSwitcherButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(uploadSectionGeneralElements['updateTypeSwitcherButton'], 1)
    ac.drawBackground(uploadSectionGeneralElements['updateTypeSwitcherButton'], 1)
    ac.drawBorder(uploadSectionGeneralElements['updateTypeSwitcherButton'], 0)
    ac.addOnClickedListener(uploadSectionGeneralElements['updateTypeSwitcherButton'], onUpdateTypeSwitcherButtonClick)
    ac.setFontAlignment(uploadSectionGeneralElements['updateTypeSwitcherButton'], 'center')

    if uploadAvailability:
        ac.setVisible(uploadSectionGeneralElements['updateTypeSwitcherButton'], 1)
    else:
        ac.setVisible(uploadSectionGeneralElements['updateTypeSwitcherButton'], 0)

    # Configure the button to switch to Delete
    # ac.setPosition(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 426, 226)
    # ac.setSize(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 60, 22)
    # ac.setText(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 'Delete')
    # ac.setBackgroundColor(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 0, 0, 0)
    # ac.setFontColor(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 0.25098, 0.66274, 0.66274, 1)
    # ac.setBackgroundOpacity(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 1)
    # ac.drawBackground(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 1)
    # ac.drawBorder(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 0)
    # ac.addOnClickedListener(uploadSectionGeneralElements['deleteTypeSwitcherButton'], onUpdateTypeSwitcherButtonClick)
    # ac.setFontAlignment(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 'center')
    # ac.setVisible(uploadSectionGeneralElements['deleteTypeSwitcherButton'], 1)

    ###################################
    ### Upload new section          ###
    ###################################

    # Configure the error message label
    ac.setPosition(uploadSectionElements['uploadMessageLabel'], 0, 275)
    ac.setSize(uploadSectionElements['uploadMessageLabel'], 800, 22)
    ac.setFontAlignment(uploadSectionElements['uploadMessageLabel'], 'center')
    ac.setVisible(uploadSectionElements['uploadMessageLabel'], 0)

    # Configure the file selector label
    ac.setPosition(uploadSectionElements['fileSelectorButtonLabel'], 5, 290)
    ac.setSize(uploadSectionElements['fileSelectorButtonLabel'], 300, 22)
    ac.setText(uploadSectionElements['fileSelectorButtonLabel'], 'Select a file to upload (click to cycle files)')
    ac.setVisible(uploadSectionElements['fileSelectorButtonLabel'], 0)

    # Configure the file selector button
    ac.setPosition(uploadSectionElements['fileSelectorButton'], 5, 312)
    ac.setSize(uploadSectionElements['fileSelectorButton'], 300, 22)
    ac.setText(uploadSectionElements['fileSelectorButton'], currentUploadFileName)
    ac.addOnClickedListener(uploadSectionElements['fileSelectorButton'], onFileSelectorButtonClick)
    ac.setVisible(uploadSectionElements['fileSelectorButton'], 0)

    # Configure the setup trim selector label
    ac.setPosition(uploadSectionElements['trimSelectorButtonLabel'], 350, 290)
    ac.setSize(uploadSectionElements['trimSelectorButtonLabel'], 75, 22)
    ac.setText(uploadSectionElements['trimSelectorButtonLabel'], 'Select a trim:')
    ac.setVisible(uploadSectionElements['trimSelectorButtonLabel'], 0)

    # Configure the upload setup trim selector
    ac.setPosition(uploadSectionElements['trimSelectorButton'], 350, 312)
    ac.setSize(uploadSectionElements['trimSelectorButton'], 75, 22)
    ac.setText(uploadSectionElements['trimSelectorButton'], currentUploadTrim)
    ac.setBackgroundColor(uploadSectionElements['trimSelectorButton'], 1, 1, 1)
    ac.setFontColor(uploadSectionElements['trimSelectorButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(uploadSectionElements['trimSelectorButton'], 1)
    ac.drawBackground(uploadSectionElements['trimSelectorButton'], 1)
    ac.drawBorder(uploadSectionElements['trimSelectorButton'], 0)
    ac.addOnClickedListener(uploadSectionElements['trimSelectorButton'], onTrimSelectorButtonClick)
    ac.setVisible(uploadSectionElements['trimSelectorButton'], 0)

    # Configure the setup baseline selector label
    ac.setPosition(uploadSectionElements['baselineSelectorButtonLabel'], 450, 290)
    ac.setSize(uploadSectionElements['baselineSelectorButtonLabel'], 75, 22)
    ac.setText(uploadSectionElements['baselineSelectorButtonLabel'], 'Track Specific?')
    ac.setVisible(uploadSectionElements['baselineSelectorButtonLabel'], 0)

    # Configure the baseline selector button
    ac.setPosition(uploadSectionElements['baselineSelectorButton'], 450, 312)
    ac.setSize(uploadSectionElements['baselineSelectorButton'], 75, 22)
    ac.setText(uploadSectionElements['baselineSelectorButton'], 'Yes')
    ac.setBackgroundColor(uploadSectionElements['baselineSelectorButton'], 1, 1, 1)
    ac.setFontColor(uploadSectionElements['baselineSelectorButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(uploadSectionElements['baselineSelectorButton'], 1)
    ac.drawBackground(uploadSectionElements['baselineSelectorButton'], 1)
    ac.drawBorder(uploadSectionElements['baselineSelectorButton'], 0)
    ac.addOnClickedListener(uploadSectionElements['baselineSelectorButton'], onBaselineSelectorButtonClick)
    ac.setVisible(uploadSectionElements['baselineSelectorButton'], 0)

    # Configure the upload button
    ac.setPosition(uploadSectionElements['uploadButton'], 720, 312)
    ac.setSize(uploadSectionElements['uploadButton'], 70, 22)
    ac.setText(uploadSectionElements['uploadButton'], 'Upload')
    ac.setBackgroundColor(uploadSectionElements['uploadButton'], 0.25098, 0.66274, 0.66274)
    ac.setFontColor(uploadSectionElements['uploadButton'], 1, 1, 1, 1)
    ac.setBackgroundOpacity(uploadSectionElements['uploadButton'], 1)
    ac.drawBackground(uploadSectionElements['uploadButton'], 1)
    ac.drawBorder(uploadSectionElements['uploadButton'], 0)
    ac.addOnClickedListener(uploadSectionElements['uploadButton'], onUploadButtonClick)
    ac.setVisible(uploadSectionElements['uploadButton'], 0)

    ###################################
    ### Update section              ###
    ###################################

    # Configure the update setup message label
    ac.setPosition(updateSectionElements['updateMessageLabel'], 0, 300)
    ac.setSize(updateSectionElements['updateMessageLabel'], 800, 22)
    ac.setFontAlignment(updateSectionElements['updateMessageLabel'], 'center')
    ac.setVisible(updateSectionElements['updateMessageLabel'], 0)

    # Set the listing table header
    addTableCell('File name', 145, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 55, 255, 'center', updateSectionElements['listingTableFilenameHeader'])
    addTableCell('Track', GUIConfig.GUIConstants['tableLayout']['cellXSize']['track_cell'], GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 200, 255, 'center', updateSectionElements['listingTableTrackHeader'])
    addTableCell('Trim', GUIConfig.GUIConstants['tableLayout']['cellXSize']['trim_cell'], GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 450, 255, 'center', updateSectionElements['listingTableTrimHeader'])
    addTableCell('AC', GUIConfig.GUIConstants['tableLayout']['cellXSize']['acversion_cell'], GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 255, 'center', updateSectionElements['listingTableAcVersionHeader'])
    addTableCell('Version', GUIConfig.GUIConstants['tableLayout']['cellXSize']['version_cell'], GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 255, 'center', updateSectionElements['listingTableSetupVersionHeader'])

    # Set the refresh update section button
    ac.setSize(updateSectionElements['refreshUpdateGUIButton'], 70, 22)
    ac.setPosition(updateSectionElements['refreshUpdateGUIButton'], 720, 226)
    ac.setText(updateSectionElements['refreshUpdateGUIButton'], 'Refresh')
    ac.setBackgroundColor(updateSectionElements['refreshUpdateGUIButton'], 1, 1, 1)
    ac.setFontColor(updateSectionElements['refreshUpdateGUIButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(updateSectionElements['refreshUpdateGUIButton'], 1)
    ac.drawBackground(updateSectionElements['refreshUpdateGUIButton'], 1)
    ac.drawBorder(updateSectionElements['refreshUpdateGUIButton'], 0)
    ac.addOnClickedListener(updateSectionElements['refreshUpdateGUIButton'], onRefreshUpdateSectionButtonClick)
    ac.setVisible(updateSectionElements['refreshUpdateGUIButton'], 0)

    # Set the update race trim selector button
    ac.setPosition(updateSectionElements['trimSelectorRaceButton'], 600, 255)
    ac.setSize(updateSectionElements['trimSelectorRaceButton'], 63, 22)
    ac.setText(updateSectionElements['trimSelectorRaceButton'], 'Race')
    ac.setBackgroundColor(updateSectionElements['trimSelectorRaceButton'], 1, 1, 1)
    ac.setFontColor(updateSectionElements['trimSelectorRaceButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(updateSectionElements['trimSelectorRaceButton'], 1)
    ac.drawBackground(updateSectionElements['trimSelectorRaceButton'], 1)
    ac.drawBorder(updateSectionElements['trimSelectorRaceButton'], 0)
    ac.addOnClickedListener(updateSectionElements['trimSelectorRaceButton'], onUpdateTrimSelectorRaceButtonClick)
    ac.setVisible(updateSectionElements['trimSelectorRaceButton'], 0)

    # Set the update qualy trim selector button
    ac.setPosition(updateSectionElements['trimSelectorQualyButton'], 663, 255)
    ac.setSize(updateSectionElements['trimSelectorQualyButton'], 64, 22)
    ac.setText(updateSectionElements['trimSelectorQualyButton'], 'Qualy')
    ac.setBackgroundColor(updateSectionElements['trimSelectorQualyButton'], 1, 1, 1)
    ac.setFontColor(updateSectionElements['trimSelectorQualyButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(updateSectionElements['trimSelectorQualyButton'], 1)
    ac.drawBackground(updateSectionElements['trimSelectorQualyButton'], 1)
    ac.drawBorder(updateSectionElements['trimSelectorQualyButton'], 0)
    ac.addOnClickedListener(updateSectionElements['trimSelectorQualyButton'], onUpdateTrimSelectorQualyButtonClick)
    ac.setVisible(updateSectionElements['trimSelectorQualyButton'], 0)

    # Set the update base trim selector button
    ac.setPosition(updateSectionElements['trimSelectorBaseButton'], 727, 255)
    ac.setSize(updateSectionElements['trimSelectorBaseButton'], 63, 22)
    ac.setText(updateSectionElements['trimSelectorBaseButton'], 'Base')
    ac.setBackgroundColor(updateSectionElements['trimSelectorBaseButton'], 1, 1, 1)
    ac.setFontColor(updateSectionElements['trimSelectorBaseButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(updateSectionElements['trimSelectorBaseButton'], 1)
    ac.drawBackground(updateSectionElements['trimSelectorBaseButton'], 1)
    ac.drawBorder(updateSectionElements['trimSelectorBaseButton'], 0)
    ac.addOnClickedListener(updateSectionElements['trimSelectorBaseButton'], onUpdateTrimSelectorBaseButtonClick)
    ac.setVisible(updateSectionElements['trimSelectorBaseButton'], 0)

    # Set the update track specific button
    ac.setPosition(updateSectionElements['baselineSelectorButton'], 600, 285)
    ac.setSize(updateSectionElements['baselineSelectorButton'], 190, 22)
    ac.setText(updateSectionElements['baselineSelectorButton'], 'Track Specific')
    ac.setBackgroundColor(updateSectionElements['baselineSelectorButton'], 1, 1, 1)
    ac.setFontColor(updateSectionElements['baselineSelectorButton'], 0.25098, 0.66274, 0.66274, 1)
    ac.setBackgroundOpacity(updateSectionElements['baselineSelectorButton'], 1)
    ac.drawBackground(updateSectionElements['baselineSelectorButton'], 1)
    ac.drawBorder(updateSectionElements['baselineSelectorButton'], 0)
    ac.addOnClickedListener(updateSectionElements['baselineSelectorButton'], onUpdateBaselineSelectorButtonClick)
    ac.setVisible(updateSectionElements['baselineSelectorButton'], 0)

    # Set the update file selector button
    ac.setPosition(updateSectionElements['fileSelectorButton'], 600, 315)
    ac.setSize(updateSectionElements['fileSelectorButton'], 190, 22)
    ac.setText(updateSectionElements['fileSelectorButton'], currentUpdateFileName)
    ac.addOnClickedListener(updateSectionElements['fileSelectorButton'], onUpdateFileSelectorButtonClick)
    ac.setVisible(updateSectionElements['fileSelectorButton'], 0)

    # Set the update button
    ac.setPosition(updateSectionElements['uploadButton'], 630, 345)
    ac.setSize(updateSectionElements['uploadButton'], 130, 22)
    ac.setText(updateSectionElements['uploadButton'], 'Update')
    ac.setBackgroundColor(updateSectionElements['uploadButton'], 0.25098, 0.66274, 0.66274)
    ac.setFontColor(updateSectionElements['uploadButton'], 1, 1, 1, 1)
    ac.setBackgroundOpacity(updateSectionElements['uploadButton'], 1)
    ac.drawBackground(updateSectionElements['uploadButton'], 1)
    ac.drawBorder(updateSectionElements['uploadButton'], 0)
    ac.addOnClickedListener(updateSectionElements['uploadButton'], onUpdateUploadButtonClick)
    ac.setVisible(updateSectionElements['uploadButton'], 0)

    yPos = GUIConfig.GUIConstants['updateTableLayout']['startingYPosition']
    rowNumber = 1

    for key, cells in updateListingTable.items():

        for cellId, label in cells.items():
            ac.setPosition(label, GUIConfig.GUIConstants['updateTableLayout']['xPos'][cellId], yPos)
            ac.setText(label, '')
            ac.setSize(label, GUIConfig.GUIConstants['updateTableLayout']['cellXSize'][cellId],
                       GUIConfig.GUIConstants['updateTableLayout']['cellHeight'])

            if cellId == 'select_cell':
                ac.setBackgroundColor(label, 1, 1, 1)
                ac.setFontColor(label, 0.25098, 0.66274, 0.66274, 1)
            else:
                ac.setBackgroundColor(label, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'R'],
                                      GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'G'],
                                      GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'B'])

            ac.setBackgroundOpacity(label, 1)
            ac.drawBackground(label, 1)
            ac.drawBorder(label, 0)
            ac.setVisible(label, 0)
            ac.setFontAlignment(label, 'center')

            if cellId == 'select_cell':
                if rowNumber == 1:
                    ac.addOnClickedListener(label, onSelectUserSetupUpdateButton1Clicked)
                elif rowNumber == 2:
                    ac.addOnClickedListener(label, onSelectUserSetupUpdateButton2Clicked)
                elif rowNumber == 3:
                    ac.addOnClickedListener(label, onSelectUserSetupUpdateButton3Clicked)
                elif rowNumber == 4:
                    ac.addOnClickedListener(label, onSelectUserSetupUpdateButton4Clicked)
                elif rowNumber == 5:
                    ac.addOnClickedListener(label, onSelectUserSetupUpdateButton5Clicked)

        yPos += GUIConfig.GUIConstants['updateTableLayout']['cellHeight'] + 1
        rowNumber += 1

    ac.setPosition(listingUpdateTableMisc['emptyRowLabel']['label'], 5, 315)
    ac.setSize(listingUpdateTableMisc['emptyRowLabel']['label'], 590, 22)
    ac.setFontAlignment(listingUpdateTableMisc['emptyRowLabel']['label'], 'center')

    ac.setPosition(updateSectionElements['updateOptionsMessageLabel'], 595, 290)
    ac.setSize(updateSectionElements['updateOptionsMessageLabel'], 200, 22)
    ac.setFontAlignment(updateSectionElements['updateOptionsMessageLabel'], 'center')

    # Setting up the setups listing table page spinner
    updateListingTablePageSpinner = ac.addSpinner(appWindow, '')
    ac.setPosition(updateListingTablePageSpinner, 529, 390)
    ac.setSize(updateListingTablePageSpinner, 60, 20)
    ac.setVisible(updateListingTablePageSpinner, 0)

    for key, element in updateSectionElements.items():
        ac.setVisible(element, 0)


def refreshUploadSection():
    if uploadAvailability:
        ac.log('TheSetupMarket logs | refreshUploadSection : if uploadAvailability:')
        # Hide the upload message label
        ac.setVisible(uploadSectionElements['uploadMessageLabel'], 0)
        # Show the upload sections switcher buttons.
        ac.setVisible(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 1)
        ac.setVisible(uploadSectionGeneralElements['updateTypeSwitcherButton'], 1)

        showUploadNewSection()
    else:
        ac.log('TheSetupMarket logs | refreshUploadSection : else uploadAvailability:')
        if not userTSMId:
            ac.log('TheSetupMarket logs | refreshUploadSection: User steamCommunityID not found in TSM DB')
            ac.setText(uploadSectionElements['uploadMessageLabel'], 'Go to thesetupmarket.com to create an account and link it with your steam account')
            ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 0)
        elif not current_carId:
            ac.log('TheSetupMarket logs | refreshUploadSection: The car is not available for uploads')
            ac.setText(uploadSectionElements['uploadMessageLabel'], 'The car is not available for upload yet')
            ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 0)
        elif not current_trackId:
            ac.log('TheSetupMarket logs | refreshUploadSection: The track is not available for uploads')
            ac.setText(uploadSectionElements['uploadMessageLabel'], 'The track is not available for uploads yet')
            ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 0)
        elif not current_ac_version:
            ac.log('TheSetupMarket logs | refreshUploadSection: The current_ac_version is not available for uploads')
            ac.setText(uploadSectionElements['uploadMessageLabel'], 'The current_ac_version is not available for uploads yet')
            ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 0)
        elif len(allSetupsFileNamesInFolder) == 0:
            ac.log('TheSetupMarket logs | refreshUploadSection: There are no files in the current track setups folder for this car')
            ac.setText(uploadSectionElements['uploadMessageLabel'], 'There are no files to upload in the current track setups folder for this car')
            ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 1)

        hideUploadNewSection()
        ac.setVisible(uploadSectionElements['uploadMessageLabel'], 1)


def refreshUpdateSection():
    # If there is no files in folder, show message.
    if len(allSetupsFileNamesInFolder) == 0:
        # SHOULD SHOW REFRESH BUTTON AND MESSAGE ONLY
        ac.log('TheSetupMarket logs | onUpdateTypeSwitcherButtonClick: no setups in folder')
        ac.setText(updateSectionElements['updateMessageLabel'], 'No setup files found in folder')
        ac.setVisible(updateSectionElements['updateMessageLabel'], 1)
        ac.setVisible(updateSectionElements['refreshUpdateGUIButton'], 1)
    else:
        # If user has no setups for current car, show message.
        if len(userTSMSetups) == 0:
            ac.log('TheSetupMarket logs | No setups found to be updated')
            ac.setText(listingUpdateTableMisc['emptyRowLabel']['label'], 'No setups found to be updated')
            ac.setVisible(listingUpdateTableMisc['emptyRowLabel']['label'], 1)
            showUpdateSection()
        else:
            # Check if there are trackSpecific setups
            if len(userTSMSetups['trackSpecific']) > 0:
                ac.log('TheSetupMarket logs | trackSpecific setups found')
                ac.setVisible(updateSectionElements['updateMessageLabel'], 0)
                ac.setVisible(listingUpdateTableMisc['emptyRowLabel']['label'], 0)
                showUpdateSection()
            else:
                ac.log('TheSetupMarket logs | NO trackSpecific setups found')
                ac.setText(listingUpdateTableMisc['emptyRowLabel']['label'], 'No setups found to be updated for this track')
                ac.setVisible(listingUpdateTableMisc['emptyRowLabel']['label'], 1)
                showUpdateSection()


def showUploadingMessage():
    ac.setText(uploadSectionElements['uploadMessageLabel'], 'Uploading...')
    ac.setVisible(uploadSectionElements['uploadMessageLabel'], 1)


def showUploadedMessage(msg):
    ac.setText(uploadSectionElements['uploadMessageLabel'], msg)
    ac.setVisible(uploadSectionElements['uploadMessageLabel'], 1)
    time.sleep(2)


def refreshSetupsListingTable():
    ac.log('TheSetupMarket logs | refreshSetupsListingTable')
    # If there is setups for the default type, update the table.
    if len(setups[activeSetupType]) > 0:
        ac.log('TheSetupMarket logs | refreshSetupsListingTable - len(setups[activeSetupType]) > 0')
        # If there is more setups than setupsPerPage, update the table with 5 first items and a spinner
        if len(setups[activeSetupType]) > GUIConfig.GUIConstants['setupsPerPage']:
            ac.log('TheSetupMarket logs | refreshSetupsListingTable - more than 5 setups')

            updateSetupsListingTable(setups[activeSetupType][:5])
            updatePageSpinner(math.ceil(len(setups[activeSetupType]) / GUIConfig.GUIConstants['setupsPerPage']), 1)
        else:
            ac.log('TheSetupMarket logs | refreshSetupsListingTable - less than 5 setups')

            updateSetupsListingTable(setups[activeSetupType])

    # if there is no setups for this type, show empty table label.
    else:
        ac.log('TheSetupMarket logs | refreshSetupsListingTable - no setups')
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        hideSetupsListingTable()
        updateSetupsListingTable(setups[activeSetupType])


def updateSetupsListingTable(setups):
    global eventInfos

    if len(setups) == 0:
        if activeSetupType == 'trackSpecific':
            ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
            ac.setText(listingTableMisc['emptyRowLabel']['label'], 'No setups for current track')
        elif activeSetupType == 'anyTracks':
            ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
            ac.setText(listingTableMisc['emptyRowLabel']['label'], 'No setups for no specific tracks')
        elif activeSetupType == 'otherTracks':
            ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
            ac.setText(listingTableMisc['emptyRowLabel']['label'], 'No setups for other tracks')
    else:
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 0)

    # Set setupIds and setupFilenames for events listeners
    eventInfos = {
        'setupIds': {},
        'setupFilenames': {}
    }

    rowNumber = 1

    for setup in setups:
        setupId = setup['_id']

        eventInfos['setupIds'][rowNumber - 1] = setupId
        eventInfos['setupFilenames'][rowNumber - 1] = 'TSM-ac' + str(setup['sim_version']) + '_' + setup['author']['display_name'].replace(' ', '') + '_' + setup['type'] + '_' + setup['track']['name'] + '_v' + str(setup['version']) + '.ini'

        for cellName, labelCtrl in listingTable[rowNumber].items():
            ac.setVisible(labelCtrl, 1)

            if cellName == 'dl_cell':
                ac.setBackgroundTexture(labelCtrl, 'apps/python/thesetupmarket/img/dl_bg_alt.png')
            elif cellName == 'track_cell':
                ac.setText(labelCtrl, setup['track']['name'])
            elif cellName == 'author_cell':
                ac.setText(labelCtrl, setup['author']['display_name'][0:20])
            elif cellName == 'trim_cell' :
                ac.setText(labelCtrl, setup['type'])
            elif cellName == 'bestlap_cell':
                bestlap = 'n/a'

                if setup['best_time'] != '':
                    bestlap = setup['best_time']

                ac.setText(labelCtrl, bestlap)
            elif cellName == 'rating_cell':
                totalRating = 0

                for rating in setup['ratings']:
                    totalRating += rating['rating']

                if totalRating == 0:
                    rating = 'n/a'
                else:
                    rating = str(totalRating)

                ac.setText(labelCtrl, str(rating))

            elif cellName == 'downloads_cell':
                ac.setText(labelCtrl, str(setup['downloads']))
            elif cellName == 'acversion_cell':
                ac.setText(labelCtrl, str(setup['sim_version']))
            elif cellName == 'version_cell':
                ac.setText(labelCtrl, 'v'+str(setup['version']))

        rowNumber += 1

    if len(setups) < GUIConfig.GUIConstants['setupsPerPage']:
        # Set all remaining rows to not visible
        for index in range(GUIConfig.GUIConstants['setupsPerPage'] - len(setups)):
           for cellName, labelCtrl in listingTable[GUIConfig.GUIConstants['setupsPerPage'] - index].items():
               ac.setVisible(labelCtrl, 0)


##################################
## Show/Hide sections functions
##################################
def showUploadNewSection():
    for key, element in uploadSectionElements.items():
        # Check also if a message should be displayed (if the user have no file in the folder for exemple)
        if key != 'uploadMessageLabel':
            ac.setVisible(element, 1)


def hideUploadNewSection():
    for key, element in uploadSectionElements.items():
        if key != 'refreshUploadGUIButton':
            ac.setVisible(element, 0)

    ac.setVisible(updateListingTablePageSpinner, 0)


def showUpdateSection():
    for key, element in updateSectionElements.items():
        # Check also if a message should be displayed (if the user have no uploaded setup to update for exemple)
        if key == 'updateMessageLabel':
            ac.setVisible(element, 0)
        else:
            ac.setVisible(element, 1)

    refreshUserSetupsListingTable()
    hideUpdateUserSetupDetails()


def hideUpdateSection():
    for key, element in updateSectionElements.items():
        ac.setVisible(element, 0)

    for key, element in listingUpdateTableMisc.items():
        ac.setVisible(element['label'], 0)

    hideUserSetupsListingTable()


def hideSetupsListingTable():
    for key, row in listingTable.items():
        for cellName, labelCtrl in row.items():
            ac.setVisible(labelCtrl, 0)


def showSetupsListingTable():
    for key, row in listingTable.items():
        for cellName, labelCtrl in row.items():
            ac.setVisible(labelCtrl, 1)


def hideUserSetupsListingTable():
    for key, rowDict in updateListingTable.items():
        for key, label in rowDict.items():
            ac.setVisible(label, 0)


def showUserSetupsListingTable():
    for key, rowDict in updateListingTable.items():
        for key, label in rowDict.items():
            ac.setVisible(label, 1)


def showUpdateUserSetupDetails(setupDetails):
    global currentUpdateTrim, currentUpdateBestlap, currentUpdateComments, currentUpdateFileName, currentUpdateBaseline

    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 0)

    if setupDetails['file_name'] in allSetupsFileNamesInFolder:
        ac.setText(updateSectionElements['fileSelectorButton'], setupDetails['file_name'])
        currentUpdateFileName = setupDetails['file_name']
    else:
        ac.setText(updateSectionElements['fileSelectorButton'], allSetupsFileNamesInFolder[0])
        currentUpdateFileName = allSetupsFileNamesInFolder[0]

    ac.setVisible(updateSectionElements['fileSelectorButton'], 1)

    if setupDetails['type'] == 'race':
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorRaceButton'], 1, 1, 1)
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorQualyButton'], 0, 0, 0)
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorBaseButton'], 0, 0, 0)
    elif setupDetails['type'] == 'qualy':
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorRaceButton'], 0, 0, 0)
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorQualyButton'], 1, 1, 1)
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorBaseButton'], 0, 0, 0)
    else:
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorRaceButton'], 0, 0, 0)
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorQualyButton'], 0, 0, 0)
        GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorBaseButton'], 1, 1, 1)

    ac.setVisible(updateSectionElements['trimSelectorRaceButton'], 1)
    ac.setVisible(updateSectionElements['trimSelectorQualyButton'], 1)
    ac.setVisible(updateSectionElements['trimSelectorBaseButton'], 1)

    currentUpdateTrim = setupDetails['type']
    currentUpdateBestlap = setupDetails['best_time']
    currentUpdateComments = setupDetails['comments']

    if setupDetails['track']['_id'] == '55db6db13cc3a26dcae7116d':
        currentUpdateBaseline = True
    else:
        currentUpdateBaseline = False


    if setupDetails['track']['_id'] == '55db6db13cc3a26dcae7116d':
        ac.setText(updateSectionElements['baselineSelectorButton'], 'Baseline setup')
        GUIhelpers.changeElementBgColor(updateSectionElements['baselineSelectorButton'], 0, 0, 0)
    else:
        ac.setText(updateSectionElements['baselineSelectorButton'], 'Track Specific')
        GUIhelpers.changeElementBgColor(updateSectionElements['baselineSelectorButton'], 1, 1, 1)
    ac.setVisible(updateSectionElements['baselineSelectorButton'], 1)

    ac.setVisible(updateSectionElements['uploadButton'], 1)


def hideUpdateUserSetupDetails():
    ac.setVisible(updateSectionElements['fileSelectorButton'], 0)
    ac.setVisible(updateSectionElements['trimSelectorRaceButton'], 0)
    ac.setVisible(updateSectionElements['trimSelectorQualyButton'], 0)
    ac.setVisible(updateSectionElements['trimSelectorBaseButton'], 0)
    ac.setVisible(updateSectionElements['baselineSelectorButton'], 0)
    ac.setVisible(updateSectionElements['uploadButton'], 0)
    ac.setText(updateSectionElements['updateOptionsMessageLabel'], 'Select a setup on the left.')
    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)


##################################
## Refresh functions
##################################
def updatePageSpinner(pageCount, currentValue):
    global listingTablePageSpinner

    if pageCount > 1:
        ac.setVisible(listingTablePageSpinner, 1)
        ac.setRange(listingTablePageSpinner, 1, pageCount)
        ac.setValue(listingTablePageSpinner, currentValue)

        ac.addOnValueChangeListener(listingTablePageSpinner, onListingTablePageSpinnerClick)
    else:
        ac.setVisible(listingTablePageSpinner, 0)


def updateUserSetupsPageSpinner(pageCount, currentValue):

    if pageCount > 1:
        ac.setVisible(updateListingTablePageSpinner, 1)
        ac.setRange(updateListingTablePageSpinner, 1, pageCount)
        ac.setValue(updateListingTablePageSpinner, currentValue)

        ac.addOnValueChangeListener(updateListingTablePageSpinner, onUpdateListingTablePageSpinnerClick)
    else:
        ac.setVisible(updateListingTablePageSpinner, 0)


def refreshUserSetupsListingTable():
    ac.log('TheSetupMarket logs | refreshUserSetupsListingTable')
    # If there is setups for the current track, update the table.
    if len(userTSMSetups) > 0 and len(userTSMSetups['trackSpecific']) > 0:
        # If there is more setups than setupsPerPage, update the table with 5 first items and a spinner
        if len(userTSMSetups['trackSpecific']) > GUIConfig.GUIConstants['setupsPerPage']:
            updateUserSetupsListingTable(userTSMSetups['trackSpecific'][:5])
            updateUserSetupsPageSpinner(math.ceil(len(userTSMSetups['trackSpecific']) / GUIConfig.GUIConstants['setupsPerPage']), 1)
        else:
            updateUserSetupsListingTable(userTSMSetups['trackSpecific'])
    else:
        # Means we dont have any setups uploaded for this user.
        ac.log('TheSetupMarket logs | refreshUserSetupsListingTable - No setups to update')
        updateUserSetupsListingTable([])
    # if there is no setups for this type, show empty table label.


def updateUserSetupsListingTable(setups):
    global updateEventInfos

    ac.log('TheSetupMarket logs | updateUserSetupsListingTable')

    if len(setups) == 0:
        ac.setVisible(listingUpdateTableMisc['emptyRowLabel']['label'], 1)
        ac.setText(listingUpdateTableMisc['emptyRowLabel']['label'], 'No setups for current track')
    else:
        ac.setVisible(listingUpdateTableMisc['emptyRowLabel']['label'], 0)
        ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)

    # Set setupIds and setupFilenames for events listeners
    updateEventInfos = {
        'setupIds': {},
        'setupFilenames': {}
    }

    rowNumber = 1

    for setup in setups:
        setupId = setup['_id']
        ac.log('TheSetupMarket logs | updateUserSetupsListingTable: setupId = ' + str(setupId))

        updateEventInfos['setupIds'][rowNumber - 1] = setupId

        for cellName, labelCtrl in updateListingTable[rowNumber].items():
            ac.setVisible(labelCtrl, 1)

            if cellName == 'select_cell':
                ac.setText(labelCtrl, 'Select')
            elif cellName == 'file_name_cell':
                ac.setText(labelCtrl, setup['file_name'])
            elif cellName == 'track_cell':
                ac.setText(labelCtrl, setup['track']['name'])
            elif cellName == 'trim_cell':
                ac.setText(labelCtrl, setup['type'])
            elif cellName == 'acversion_cell':
                ac.setText(labelCtrl, str(setup['sim_version']))
            elif cellName == 'version_cell':
                ac.setText(labelCtrl, 'v' + str(setup['version']))

        rowNumber += 1

    if len(setups) < GUIConfig.GUIConstants['setupsPerPage']:
        # Set all remaining rows to not visible
        for index in range(GUIConfig.GUIConstants['setupsPerPage'] - len(setups)):
           for cellName, labelCtrl in updateListingTable[GUIConfig.GUIConstants['setupsPerPage'] - index].items():
               ac.setVisible(labelCtrl, 0)


@async
def refreshUpdateUserSetupsAfterUpdate(msg):
    global userTSMSetups

    ac.log('TheSetupMarket logs | refreshUpdateUserSetupsAfterUpdate: msg = ' + msg)
    ac.setText(updateSectionElements['updateMessageLabel'], msg)
    ac.setVisible(updateSectionElements['updateMessageLabel'], 1)
    time.sleep(2)

    unselectAllUserUpdateSetups()

    userTSMSetups = tsm.getUserSetups(userTSMId, current_carId, current_trackId)

    showUpdateSection()


##################################
## Event listeners
##################################
def onListingTablePageSpinnerClick(x):
    global setups, activeSetupType

    fromIndex = x * GUIConfig.GUIConstants['setupsPerPage'] - GUIConfig.GUIConstants['setupsPerPage']
    toIndex = x * GUIConfig.GUIConstants['setupsPerPage']

    updateSetupsListingTable(setups[activeSetupType][fromIndex:toIndex])


def onUpdateListingTablePageSpinnerClick(x):

    fromIndex = x * GUIConfig.GUIConstants['setupsPerPage'] - GUIConfig.GUIConstants['setupsPerPage']
    toIndex = x * GUIConfig.GUIConstants['setupsPerPage']

    unselectAllUserUpdateSetups()
    hideUpdateUserSetupDetails()
    updateUserSetupsListingTable(userTSMSetups['trackSpecific'][fromIndex:toIndex])


def onListingTableSetupTypeButtonClick(*args):
    global activeSetupType

    if activeSetupType == 'trackSpecific':
        activeSetupType = 'anyTracks'
        updateSetupsListingTable(setups['anyTracks'][:5])
        ac.setText(listingTableSetupTypeButton, 'Any Tracks')
        updatePageSpinner(math.ceil(len(setups['anyTracks']) / GUIConfig.GUIConstants['setupsPerPage']), 1)
    elif activeSetupType == 'anyTracks':
        activeSetupType = 'otherTracks'
        updateSetupsListingTable(setups['otherTracks'][:5])
        ac.setText(listingTableSetupTypeButton, 'Other Tracks')
        updatePageSpinner(math.ceil(len(setups['otherTracks']) / GUIConfig.GUIConstants['setupsPerPage']), 1)
    else:
        activeSetupType = 'trackSpecific'
        updateSetupsListingTable(setups['trackSpecific'][:5])
        ac.setText(listingTableSetupTypeButton, 'Current Track')
        updatePageSpinner(math.ceil(len(setups['trackSpecific']) / GUIConfig.GUIConstants['setupsPerPage']), 1)


def onDownloadButton1Clicked(*args):
    ac.log('TheSetupMarket logs | dl button1 clicked')
    if eventInfos['setupIds'][0] != '':
        hideSetupsListingTable()

        # Show the Downloading message
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Downloading...')

        tsm.downloadSetup(eventInfos['setupIds'][0], eventInfos['setupFilenames'][0], currentCarName, currentTrackBaseName, currentTrackLayout, refreshSetupsListingTable)


def onDownloadButton2Clicked(*args):
    ac.log('TheSetupMarket logs | dl button2 clicked')
    if eventInfos['setupIds'][1] != '':
        hideSetupsListingTable()

        # Show the Downloading message
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Downloading...')

        tsm.downloadSetup(eventInfos['setupIds'][1], eventInfos['setupFilenames'][1], currentCarName, currentTrackBaseName, currentTrackLayout, refreshSetupsListingTable)


def onDownloadButton3Clicked(*args):
    ac.log('TheSetupMarket logs | dl button3 clicked')
    if eventInfos['setupIds'][2] != '':
        hideSetupsListingTable()

        # Show the Downloading message
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Downloading...')

        tsm.downloadSetup(eventInfos['setupIds'][2], eventInfos['setupFilenames'][2], currentCarName, currentTrackBaseName, currentTrackLayout, refreshSetupsListingTable)


def onDownloadButton4Clicked(*args):
    ac.log('TheSetupMarket logs | dl button4 clicked')
    if eventInfos['setupIds'][3] != '':
        hideSetupsListingTable()

        # Show the Downloading message
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Downloading...')

        tsm.downloadSetup(eventInfos['setupIds'][3], eventInfos['setupFilenames'][3], currentCarName, currentTrackBaseName, currentTrackLayout, refreshSetupsListingTable)


def onDownloadButton5Clicked(*args):
    ac.log('TheSetupMarket logs | dl button5 clicked')
    if eventInfos['setupIds'][4] != '':
        hideSetupsListingTable()

        # Show the Downloading message
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Downloading...')

        tsm.downloadSetup(eventInfos['setupIds'][4], eventInfos['setupFilenames'][4], currentCarName, currentTrackBaseName, currentTrackLayout, refreshSetupsListingTable)


@async
def onRefreshSetupsButtonClick(*args):
    global setups

    # Hide setups listing table
    hideSetupsListingTable()

    # Show the Loading message
    ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
    ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Loading...')

    # Get setups from api.
    ac.log('TheSetupMarket logs | onRefreshSetupsButtonClick - getting setups')
    setups = tsm.getSetups(currentCarName, currentTrackBaseName, currentTrackLayout)

    refreshSetupsListingTable()



def onFileSelectorButtonClick(*args):
    global currentUploadFileName
    ac.log('onFileSelectorButtonClick')

    if len(allSetupsFileNamesInFolder) > 0:

        currentIndex = allSetupsFileNamesInFolder.index(currentUploadFileName)

        if currentIndex + 1 < len(allSetupsFileNamesInFolder):
            currentUploadFileName = allSetupsFileNamesInFolder[currentIndex + 1]
        else:
            currentUploadFileName = allSetupsFileNamesInFolder[0]

        ac.setText(uploadSectionElements['fileSelectorButton'], currentUploadFileName)


def onTrimSelectorButtonClick(*args):
    global currentUploadTrim

    if currentUploadTrim == 'Qualy':
        currentUploadTrim = 'Race'
    elif currentUploadTrim == 'Race':
        currentUploadTrim = 'Base'
    else:
        currentUploadTrim = 'Qualy'

    ac.setText(uploadSectionElements['trimSelectorButton'], currentUploadTrim)


@async
def onUploadButtonClick(*args):
    ac.log('onUploadButtonClick')
    # Hide upload section GUI
    hideUploadNewSection()
    showUploadingMessage()

    isUploaded = tsm.uploadSetup(userTSMId, current_ac_version, userSteamId, currentUploadFileName, currentUploadTrim, currentUploadBaseline, current_carId, current_trackId, currentCarName, currentTrackBaseName, currentTrackLayout)

    if isUploaded:
        # Show Uploaded message
        showUploadedMessage('The setup has been uploaded successfully.')
    else:
        showUploadedMessage('There has been an error uploading the setup.')

    ac.setVisible(uploadSectionElements['uploadMessageLabel'], 0)
    showUploadNewSection()


def onBaselineSelectorButtonClick(*args):
    global currentUploadBaseline

    if currentUploadBaseline:
        ac.log('TheSetupMarket logs | onBaselineSelectorButtonClick: if currentUploadBaseline')
        currentUploadBaseline = False
        ac.setText(uploadSectionElements['baselineSelectorButton'], 'Yes')
    else:
        ac.log('TheSetupMarket logs | onBaselineSelectorButtonClick: else currentUploadBaseline')
        currentUploadBaseline = True
        ac.setText(uploadSectionElements['baselineSelectorButton'], 'No')


def onRefreshUploadSectionButtonClick(*args):
    global allSetupsFileNamesInFolder, currentUploadFileName, currentUploadFileName, uploadAvailability

    hideUploadNewSection()
    ac.setText(uploadSectionElements['uploadMessageLabel'], 'Loading...')
    ac.setVisible(uploadSectionElements['uploadMessageLabel'], 1)

    # Get all the files names in the current track folder
    allSetupsFileNamesInFolder = tsm.getAllSetupsFromFolder(currentCarName, currentTrackBaseName)
    ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: allSetupsFileNamesInFolder = ' + str(allSetupsFileNamesInFolder))

    # Set the current upload filename
    if len(allSetupsFileNamesInFolder) > 0:
        currentUploadFileName = allSetupsFileNamesInFolder[0]
    else:
        currentUploadFileName = 'No file in track folder'

    ac.setText(uploadSectionElements['fileSelectorButton'], currentUploadFileName)

    # Check if we have errors that would break the upload function. If so, disable uploading.
    if not current_ac_version or not current_carId or not current_trackId or len(allSetupsFileNamesInFolder) == 0 or not userSteamId or not userTSMId:
        ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: disabling uploading...')
        uploadAvailability = False

    else:
        ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: enabling uploading...')
        uploadAvailability = True

    refreshUploadSection()


@async
def onRefreshUpdateSectionButtonClick(*args):
    global allSetupsFileNamesInFolder, uploadAvailability, userTSMSetups
    ac.log('TheSetupMarket logs | onRefreshUpdateSectionButtonClick')

    hideUpdateSection()
    hideUploadNewSection()
    ac.setText(updateSectionElements['updateMessageLabel'], 'Loading...')
    ac.setVisible(updateSectionElements['updateMessageLabel'], 1)

    unselectAllUserUpdateSetups()

    userTSMSetups = tsm.getUserSetups(userTSMId, current_carId, current_trackId)

    # Get all the files names in the current track folder
    allSetupsFileNamesInFolder = tsm.getAllSetupsFromFolder(currentCarName, currentTrackBaseName)
    ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: allSetupsFileNamesInFolder = ' + str(
        allSetupsFileNamesInFolder))

    # Check if we have errors that would break the update function. If so, disable updating.
    if not current_ac_version or not current_carId or not current_trackId or len(
            allSetupsFileNamesInFolder) == 0 or not userSteamId or not userTSMId:
        ac.log('TheSetupMarket logs | onRefreshUpdateSectionButtonClick: disabling updating...')
        uploadAvailability = False

    else:
        ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: enabling updating...')
        uploadAvailability = True

    refreshUpdateSection()


def onUpdateBaselineSelectorButtonClick(*args):
    global currentUpdateBaseline
    ac.log('TheSetupMarket logs | onUpdateBaselineSelectorButtonClick')

    if not currentUpdateBaseline:
        ac.setText(updateSectionElements['baselineSelectorButton'], 'Any tracks')
        GUIhelpers.changeElementBgColor(updateSectionElements['baselineSelectorButton'], 0, 0, 0)
        currentUpdateBaseline = True
    else:
        ac.setText(updateSectionElements['baselineSelectorButton'], 'Track Specific')
        GUIhelpers.changeElementBgColor(updateSectionElements['baselineSelectorButton'], 1, 1, 1)
        currentUpdateBaseline = False


def onUpdateFileSelectorButtonClick(*args):
    global currentUpdateFileName
    ac.log('onUpdateFileSelectorButtonClick')

    if len(allSetupsFileNamesInFolder) > 0:

        currentIndex = allSetupsFileNamesInFolder.index(currentUpdateFileName)

        if currentIndex + 1 < len(allSetupsFileNamesInFolder):
            currentUpdateFileName = allSetupsFileNamesInFolder[currentIndex + 1]
        else:
            currentUpdateFileName = allSetupsFileNamesInFolder[0]

        ac.setText(updateSectionElements['fileSelectorButton'], currentUpdateFileName)


def onUpdateUploadButtonClick(*args):
    ac.log('TheSetupMarket logs | onUpdateUploadButtonClick')
    hideUpdateSection()
    ac.setText(updateSectionElements['updateMessageLabel'], 'Uploading...')
    ac.setVisible(updateSectionElements['updateMessageLabel'], 1)

    tsm.updateSetup(currentCarName, currentTrackBaseName, currentUpdateFileName, currentUpdateSetupId, current_carId, current_trackId, current_ac_version, currentUpdateTrim, currentUpdateBaseline, currentUpdateBestlap, currentUpdateComments, refreshUpdateUserSetupsAfterUpdate)


def onUploadTypeSwitcherButtonClick(*args):
    ac.log('onUploadTypeSwitcherButtonClick')
    unselectAllUserUpdateSetups()
    hideUpdateSection()
    showUploadNewSection()
    onRefreshUploadSectionButtonClick()
    GUIhelpers.changeElementBgColor(uploadSectionGeneralElements['updateTypeSwitcherButton'], 0, 0, 0)
    GUIhelpers.changeElementBgColor(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 1, 1, 1)


def onUpdateTypeSwitcherButtonClick(*args):
    ac.log('onUpdateTypeSwitcherButtonClick')
    hideUploadNewSection()
    refreshUpdateSection()

    GUIhelpers.changeElementBgColor(uploadSectionGeneralElements['uploadTypeSwitcherButton'], 0, 0, 0)
    GUIhelpers.changeElementBgColor(uploadSectionGeneralElements['updateTypeSwitcherButton'], 1, 1, 1)

    refreshUserSetupsListingTable()


def onSelectUserSetupUpdateButton1Clicked(*args):
    global currentUpdateSetupId

    hideUpdateUserSetupDetails()

    ac.setText(updateSectionElements['updateOptionsMessageLabel'], 'Loading...')
    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)

    currentUpdateSetupId = updateEventInfos['setupIds'][0]

    unselectAllUserUpdateSetups()

    for key, label in updateListingTable[1].items():
        if key != 'select_cell':
            GUIhelpers.changeElementBgColor(label, 1, 1, 1)
            ac.setFontColor(label, 0.25098, 0.66274, 0.66274, 1)

    # Get the setup details and load the setup detail section
    tsm.getSetupDetails(currentUpdateSetupId, showUpdateUserSetupDetails)


def onSelectUserSetupUpdateButton2Clicked(*args):
    global currentUpdateSetupId

    hideUpdateUserSetupDetails()

    ac.setText(updateSectionElements['updateOptionsMessageLabel'], 'Loading...')
    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)

    currentUpdateSetupId = updateEventInfos['setupIds'][1]

    unselectAllUserUpdateSetups()

    for key, label in updateListingTable[2].items():
        if key != 'select_cell':
            GUIhelpers.changeElementBgColor(label, 1, 1, 1)
            ac.setFontColor(label, 0.25098, 0.66274, 0.66274, 1)

    # Get the setup details and load the setup detail section
    tsm.getSetupDetails(currentUpdateSetupId, showUpdateUserSetupDetails)


def onSelectUserSetupUpdateButton3Clicked(*args):
    global currentUpdateSetupId

    hideUpdateUserSetupDetails()

    ac.setText(updateSectionElements['updateOptionsMessageLabel'], 'Loading...')
    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)

    currentUpdateSetupId = updateEventInfos['setupIds'][2]

    unselectAllUserUpdateSetups()

    for key, label in updateListingTable[3].items():
        if key != 'select_cell':
            GUIhelpers.changeElementBgColor(label, 1, 1, 1)
            ac.setFontColor(label, 0.25098, 0.66274, 0.66274, 1)

    # Get the setup details and load the setup detail section
    tsm.getSetupDetails(currentUpdateSetupId, showUpdateUserSetupDetails)


def onSelectUserSetupUpdateButton4Clicked(*args):
    global currentUpdateSetupId

    hideUpdateUserSetupDetails()

    ac.setText(updateSectionElements['updateOptionsMessageLabel'], 'Loading...')
    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)

    currentUpdateSetupId = updateEventInfos['setupIds'][3]

    unselectAllUserUpdateSetups()

    for key, label in updateListingTable[4].items():
        if key != 'select_cell':
            GUIhelpers.changeElementBgColor(label, 1, 1, 1)
            ac.setFontColor(label, 0.25098, 0.66274, 0.66274, 1)

    # Get the setup details and load the setup detail section
    tsm.getSetupDetails(currentUpdateSetupId, showUpdateUserSetupDetails)


def onSelectUserSetupUpdateButton5Clicked(*args):
    global currentUpdateSetupId

    hideUpdateUserSetupDetails()

    ac.setText(updateSectionElements['updateOptionsMessageLabel'], 'Loading...')
    ac.setVisible(updateSectionElements['updateOptionsMessageLabel'], 1)

    currentUpdateSetupId = updateEventInfos['setupIds'][4]

    unselectAllUserUpdateSetups()

    for key, label in updateListingTable[5].items():
        if key != 'select_cell':
            GUIhelpers.changeElementBgColor(label, 1, 1, 1)
            ac.setFontColor(label, 0.25098, 0.66274, 0.66274, 1)

    # Get the setup details and load the setup detail section
    tsm.getSetupDetails(currentUpdateSetupId, showUpdateUserSetupDetails)


def onUpdateTrimSelectorRaceButtonClick(*args):
    global currentUpdateTrim
    ac.log('TheSetupMarket logs | onUpdateTrimSelectorRaceButtonClick')

    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorRaceButton'], 1, 1, 1)
    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorQualyButton'], 0, 0, 0)
    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorBaseButton'], 0, 0, 0)

    currentUpdateTrim = 'race'


def onUpdateTrimSelectorQualyButtonClick(*args):
    global currentUpdateTrim
    ac.log('TheSetupMarket logs | onUpdateTrimSelectorQualyButtonClick')

    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorQualyButton'], 1, 1, 1)
    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorRaceButton'], 0, 0, 0)
    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorBaseButton'], 0, 0, 0)

    currentUpdateTrim = 'qualy'


def onUpdateTrimSelectorBaseButtonClick(*args):
    global currentUpdateTrim
    ac.log('TheSetupMarket logs | onUpdateTrimSelectorBaseButtonClick')

    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorBaseButton'], 1, 1, 1)
    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorQualyButton'], 0, 0, 0)
    GUIhelpers.changeElementBgColor(updateSectionElements['trimSelectorRaceButton'], 0, 0, 0)

    currentUpdateTrim = 'base'


##################################
## Utilitary functions
##################################
def addTableCell(text, sizeX, r, g, b, posX, posY, textAlign, element):
    if not element:
        cell = ac.addLabel(appWindow, text)
    else:
        cell = element
        ac.setText(cell, text)

    ac.setSize(cell, sizeX, GUIConfig.GUIConstants['tableLayout']['cellHeight'])

    ac.setBackgroundColor(cell, r, g, b)
    ac.setBackgroundOpacity(cell, 1)
    ac.drawBackground(cell, 1)
    ac.drawBorder(cell, 0)
    ac.setVisible(cell, 1)

    ac.setPosition(cell, posX, posY)

    ac.setFontAlignment(cell, textAlign)


def unselectAllUserUpdateSetups():
    for rowNumber, row in updateListingTable.items():
        for key, label in row.items():
            if key != 'select_cell':
                ac.setFontColor(label, 1, 1, 1, 1)
                GUIhelpers.changeElementBgColor(label, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'R'],
                                      GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'G'],
                                      GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'B'])