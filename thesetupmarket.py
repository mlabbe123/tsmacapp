import sys
import ac
import traceback
import math
from collections import OrderedDict

try:
	from tsm import tsm
except Exception as e:
    ac.log('TheSetupMarket logs | error loading utils: ' + traceback.format_exc())

from config import GUIConfig

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


def acMain(ac_version):
    global appWindow, currentCarName, currentTrackBaseName, currentTrackLayout, setupFilename, setups, listingTable, listingTableMisc, activeSetupType, uploadSectionElements, currentUploadTrim, currentUploadBaseline

    appWindow = ac.newApp("The Setup Market")
    ac.setSize(appWindow, 800, 320)

    # downloadButton = 0

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

    # Set the GUI elements for the upload section
    # TODO: Set these elements on load, hidden. Create a function refreshUploadSection that shows/hides elements and change text for the errorMessageLabel and the fileSelectorButton. Create a helper function to show/hide an element.
    uploadSectionElements = {
        'fileSelectorButtonLabel': ac.addLabel(appWindow, ''),
        'fileSelectorButton': ac.addButton(appWindow, ''),
        'trimSelectorButtonLabel': ac.addLabel(appWindow, ''),
        'trimSelectorButton': ac.addButton(appWindow, ''),
        'baselineSelectorButtonLabel': ac.addLabel(appWindow, ''),
        'baselineSelectorButton': ac.addButton(appWindow, ''),
        'uploadButton': ac.addButton(appWindow, ''),
        'uploadMessageLabel': ac.addLabel(appWindow, ''),
        'refreshUploadGUIButton': ac.addButton(appWindow, '')
    }

    # Get current car/track/layout.
    currentCarName = ac.getCarName(0)
    currentTrackBaseName = ac.getTrackName(0)
    currentTrackLayout = ac.getTrackConfiguration(0)
    # Set the default active setup type
    activeSetupType = 'trackSpecific'

    # Set the base GUI
    initGUI(appWindow)

    # Init upload section variables
    initUploadSection()

    # Get setups for current car and track.
    setups = tsm.getSetups(currentCarName, currentTrackBaseName, currentTrackLayout)

    # If there is setups for the default type, update the table.
    if len(setups[activeSetupType]) > 0:

        # If there is more setups than setupsPerPage, update the table with 5 first items and a spinner
        if len(setups[activeSetupType]) > GUIConfig.GUIConstants['setupsPerPage']:
            # ac.log(str(setupType)+' setups pages: '+str(len(setupList) / GUIConfig.GUIConstants['setupsPerPage']))
            updateSetupsListingTable(setups[activeSetupType][:5])
            updatePageSpinner(math.ceil(len(setups[activeSetupType]) / GUIConfig.GUIConstants['setupsPerPage']), 1)
        else:
            # ac.log('One page only')
            updateSetupsListingTable(setups[activeSetupType])

    # if there is no setups for this type, show empty table label.
    else:
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)

    return "The Setup Market"


def initUploadSection():
    global userSteamCommunityID, userExists, allSetupsFileNamesInFolder, currentUploadFileName, currentUploadTrim, currentUploadBaseline, uploadAvailability, current_ac_version, current_carId, current_trackId

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

    # Get the user steam community ID
    userSteamCommunityID = tsm.getUserSteamCommunityIDFromLog()

    # Check TSM database to see if user exists
    userExists = tsm.checkIfUserExistsOnTSM(userSteamCommunityID)

    # Get the active AC version
    current_ac_version = tsm.get_ac_version_from_api()

    # Get the user steamID

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
    else:
        currentUploadFileName = 'No file in track folder'

    # Check if we have errors that would break the upload function. If so, disable uploading.
    if not current_ac_version or not current_carId or not current_trackId or len(allSetupsFileNamesInFolder) == 0 or not userSteamCommunityID or not userExists:
        ac.log('TheSetupMarket logs | disabling uploading...')
        uploadAvailability = False

    # Prepare the upload section GUI.
    initUploadSectionGUI()

    # Put the right GUI config and values.
    refreshUploadSection()


def initGUI(appWindow):
    global section1Title, section2Title, listingTable, listingTableMisc, listingTablePageSpinner, listingTableSetupTypeButton, activeSetupType

    ###################################
    ### Download section            ###
    ###################################

    ### Current track section ###
    section1Title = ac.addLabel(appWindow, "/Download setups")
    ac.setPosition(section1Title, 10, 31)

    # Setting up the refresh setups button
    refreshSetupsButton = ac.addButton(appWindow, '')
    ac.setPosition(refreshSetupsButton, 720, 30)
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
    addTableCell(appWindow, '', 25, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 53, 'center')
    addTableCell(appWindow, 'Track', 250, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 35, 53, 'center')
    addTableCell(appWindow, 'Author', 175, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'],285, 53, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 460, 53, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 510, 53, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 590, 53, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 660, 53, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 700, 53, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 730, 53, 'center')

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
        ac.setPosition(labelCtrl, 10, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + GUIConfig.GUIConstants['tableLayout']['cellHeight'] * 2)
        ac.setSize(labelCtrl, 780, GUIConfig.GUIConstants['tableLayout']['cellHeight'])
        ac.drawBorder(labelCtrl, 0)
        ac.setVisible(labelCtrl, 0)
        ac.setFontAlignment(labelCtrl, 'center')

    # SEPARATOR BEFORE SPINNERS
    separator1 = ac.addLabel(appWindow, '')
    ac.setSize(separator1, 780, 1)
    ac.setBackgroundColor(separator1, 1, 1, 1)
    ac.setBackgroundOpacity(separator1, 1)
    ac.drawBackground(separator1, 1)
    ac.drawBorder(separator1, 0)
    ac.setVisible(separator1, 1)
    ac.setPosition(separator1, 10, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + 114)

    # Setting up the setups listing setup type button
    listingTableSetupTypeButton = ac.addButton(appWindow, '')
    ac.setPosition(listingTableSetupTypeButton, 10, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + 120)
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
    ac.setPosition(listingTablePageSpinner, 730, GUIConfig.GUIConstants['tableLayout']['startingYPosition'] + 120)
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
    ac.setPosition(separator, 0, 228)

    # Add upload section title
    section4Title = ac.addLabel(appWindow, "/Upload setup")
    ac.setPosition(section4Title, 10, 235)

    # Add reset upload section button
    ac.setPosition(uploadSectionElements['refreshUploadGUIButton'], 720, 235)
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

    ac.log('TheSetupMarket logs | initUploadSectionGUI: Init the upload section GUI')

    # Configure the error message label
    ac.setPosition(uploadSectionElements['uploadMessageLabel'], 0, 275)
    ac.setSize(uploadSectionElements['uploadMessageLabel'], 800, 22)
    ac.setFontAlignment(uploadSectionElements['uploadMessageLabel'], 'center')
    ac.setVisible(uploadSectionElements['uploadMessageLabel'], 0)

    # Configure the file selector label
    ac.setPosition(uploadSectionElements['fileSelectorButtonLabel'], 10, 260)
    ac.setSize(uploadSectionElements['fileSelectorButtonLabel'], 300, 22)
    ac.setText(uploadSectionElements['fileSelectorButtonLabel'], 'Select a file to upload (click to cycle files)')
    ac.setVisible(uploadSectionElements['fileSelectorButtonLabel'], 0)

    # Configure the file selector button
    ac.setPosition(uploadSectionElements['fileSelectorButton'], 10, 282)
    ac.setSize(uploadSectionElements['fileSelectorButton'], 300, 22)
    ac.setText(uploadSectionElements['fileSelectorButton'], currentUploadFileName)
    ac.addOnClickedListener(uploadSectionElements['fileSelectorButton'], onFileSelectorButtonClick)
    ac.setVisible(uploadSectionElements['fileSelectorButton'], 0)

    # Configure the setup trim selector label
    ac.setPosition(uploadSectionElements['trimSelectorButtonLabel'], 350, 260)
    ac.setSize(uploadSectionElements['trimSelectorButtonLabel'], 75, 22)
    ac.setText(uploadSectionElements['trimSelectorButtonLabel'], 'Select a trim:')
    ac.setVisible(uploadSectionElements['trimSelectorButtonLabel'], 0)

    # Configure the upload setup trim selector
    ac.setPosition(uploadSectionElements['trimSelectorButton'], 350, 282)
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
    ac.setPosition(uploadSectionElements['baselineSelectorButtonLabel'], 450, 260)
    ac.setSize(uploadSectionElements['baselineSelectorButtonLabel'], 75, 22)
    ac.setText(uploadSectionElements['baselineSelectorButtonLabel'], 'Track Specific?')
    ac.setVisible(uploadSectionElements['baselineSelectorButtonLabel'], 0)

    # Configure the baseline selector button
    ac.setPosition(uploadSectionElements['baselineSelectorButton'], 450, 282)
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
    ac.setPosition(uploadSectionElements['uploadButton'], 715, 282)
    ac.setSize(uploadSectionElements['uploadButton'], 75, 22)
    ac.setText(uploadSectionElements['uploadButton'], 'Upload')
    ac.setBackgroundColor(uploadSectionElements['uploadButton'], 0.25098, 0.66274, 0.66274)
    ac.setFontColor(uploadSectionElements['uploadButton'], 1, 1, 1, 1)
    ac.setBackgroundOpacity(uploadSectionElements['uploadButton'], 1)
    ac.drawBackground(uploadSectionElements['uploadButton'], 1)
    ac.drawBorder(uploadSectionElements['uploadButton'], 0)
    ac.addOnClickedListener(uploadSectionElements['uploadButton'], onUploadButtonClick)
    ac.setVisible(uploadSectionElements['uploadButton'], 0)


def refreshUploadSection():
    if uploadAvailability:
        ac.log('TheSetupMarket logs | refreshUploadSection : if uploadAvailability:')
        ac.setVisible(uploadSectionElements['uploadMessageLabel'], 0)
        ac.setVisible(uploadSectionElements['refreshUploadGUIButton'], 1)
        showUploadGUI()
    else:
        ac.log('TheSetupMarket logs | refreshUploadSection : else uploadAvailability:')
        if not userExists:
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

        hideUploadGUI()
        ac.setVisible(uploadSectionElements['uploadMessageLabel'], 1)


def hideUploadGUI():
    ac.setVisible(uploadSectionElements['fileSelectorButtonLabel'], 0)
    ac.setVisible(uploadSectionElements['fileSelectorButton'], 0)
    ac.setVisible(uploadSectionElements['trimSelectorButtonLabel'], 0)
    ac.setVisible(uploadSectionElements['trimSelectorButton'], 0)
    ac.setVisible(uploadSectionElements['baselineSelectorButtonLabel'], 0)
    ac.setVisible(uploadSectionElements['baselineSelectorButton'], 0)
    ac.setVisible(uploadSectionElements['uploadButton'], 0)


def showUploadGUI():
    ac.setVisible(uploadSectionElements['fileSelectorButtonLabel'], 1)
    ac.setVisible(uploadSectionElements['fileSelectorButton'], 1)
    ac.setVisible(uploadSectionElements['trimSelectorButtonLabel'], 1)
    ac.setVisible(uploadSectionElements['trimSelectorButton'], 1)
    ac.setVisible(uploadSectionElements['baselineSelectorButtonLabel'], 1)
    ac.setVisible(uploadSectionElements['baselineSelectorButton'], 1)
    ac.setVisible(uploadSectionElements['uploadButton'], 1)


def addTableCell(appWindow, text, sizeX, r, g, b, posX, posY, textAlign):
    cell = ac.addLabel(appWindow, text)

    ac.setSize(cell, sizeX, GUIConfig.GUIConstants['tableLayout']['cellHeight'])

    ac.setBackgroundColor(cell, r, g, b)
    ac.setBackgroundOpacity(cell, 1)
    ac.drawBackground(cell, 1)
    ac.drawBorder(cell, 0)
    ac.setVisible(cell, 1)

    ac.setPosition(cell, posX, posY)

    ac.setFontAlignment(cell, textAlign)


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


    if currentTrackLayout != '':
        trackLayoutForFileName = '-' + currentTrackLayout
    else:
        trackLayoutForFileName = ''

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
                # ac.log(setup['type'])
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

    ac.log('TheSetupMarket logs | eventInfos: ' + str(eventInfos))

    if len(setups) < GUIConfig.GUIConstants['setupsPerPage']:
        ac.log('TheSetupMarket logs | setups length less than 5. Length = ' + str(len(setups)))
        # Set all remaining rows to not visible
        for index in range(GUIConfig.GUIConstants['setupsPerPage'] - len(setups)):
           for cellName, labelCtrl in listingTable[GUIConfig.GUIConstants['setupsPerPage'] - index].items():
               ac.setVisible(labelCtrl, 0)


def updatePageSpinner(pageCount, currentValue):
    global listingTablePageSpinner

    if pageCount > 1:
        ac.setVisible(listingTablePageSpinner, 1)
        ac.setRange(listingTablePageSpinner, 1, pageCount)
        ac.setValue(listingTablePageSpinner, currentValue)

        ac.addOnValueChangeListener(listingTablePageSpinner, onListingTablePageSpinnerClick)
    else:
         ac.setVisible(listingTablePageSpinner, 0)


def onListingTablePageSpinnerClick(x):
    global setups, activeSetupType

    fromIndex = x * GUIConfig.GUIConstants['setupsPerPage'] - GUIConfig.GUIConstants['setupsPerPage']
    toIndex = x * GUIConfig.GUIConstants['setupsPerPage']

    updateSetupsListingTable(setups[activeSetupType][fromIndex:toIndex])


def onListingTableSetupTypeButtonClick(*args):
    global activeSetupType

    if activeSetupType == 'trackSpecific':
        ac.log('TheSetupMarket logs | setups for anyTracks: ' + str(len(setups['anyTracks'])))
        activeSetupType = 'anyTracks'
        updateSetupsListingTable(setups['anyTracks'][:5])
        ac.setText(listingTableSetupTypeButton, 'Any Tracks')
        updatePageSpinner(math.ceil(len(setups['anyTracks']) / GUIConfig.GUIConstants['setupsPerPage']), 1)
    elif activeSetupType == 'anyTracks':
        ac.log('TheSetupMarket logs | setups for otherTracks: ' + str(len(setups['otherTracks'])))
        activeSetupType = 'otherTracks'
        updateSetupsListingTable(setups['otherTracks'][:5])
        ac.setText(listingTableSetupTypeButton, 'Other Tracks')
        updatePageSpinner(math.ceil(len(setups['otherTracks']) / GUIConfig.GUIConstants['setupsPerPage']), 1)
    else:
        ac.log('TheSetupMarket logs | setups for trackSpecific: ' + str(len(setups['trackSpecific'])))
        activeSetupType = 'trackSpecific'
        updateSetupsListingTable(setups['trackSpecific'][:5])
        ac.setText(listingTableSetupTypeButton, 'Current Track')
        updatePageSpinner(math.ceil(len(setups['trackSpecific']) / GUIConfig.GUIConstants['setupsPerPage']), 1)



def onDownloadButton1Clicked(*args):
    ac.log('TheSetupMarket logs | dl button1 clicked')
    if eventInfos['setupIds'][0] != '':
        tsm.downloadSetup(eventInfos['setupIds'][0], eventInfos['setupFilenames'][0], currentCarName, currentTrackBaseName, currentTrackLayout)

def onDownloadButton2Clicked(*args):
    ac.log('TheSetupMarket logs | dl button2 clicked')
    if eventInfos['setupIds'][1] != '':
        tsm.downloadSetup(eventInfos['setupIds'][1], eventInfos['setupFilenames'][1], currentCarName, currentTrackBaseName, currentTrackLayout)

def onDownloadButton3Clicked(*args):
    ac.log('TheSetupMarket logs | dl button3 clicked')
    if eventInfos['setupIds'][2] != '':
        tsm.downloadSetup(eventInfos['setupIds'][2], eventInfos['setupFilenames'][2], currentCarName, currentTrackBaseName, currentTrackLayout)

def onDownloadButton4Clicked(*args):
    ac.log('TheSetupMarket logs | dl button4 clicked')
    if eventInfos['setupIds'][3] != '':
        tsm.downloadSetup(eventInfos['setupIds'][3], eventInfos['setupFilenames'][3], currentCarName, currentTrackBaseName, currentTrackLayout)

def onDownloadButton5Clicked(*args):
    ac.log('TheSetupMarket logs | dl button5 clicked')
    if eventInfos['setupIds'][4] != '':
        tsm.downloadSetup(eventInfos['setupIds'][4], eventInfos['setupFilenames'][4], currentCarName, currentTrackBaseName, currentTrackLayout)

@async
def onRefreshSetupsButtonClick(*args):
    global setups
    setups = tsm.getSetups(currentCarName, currentTrackBaseName, currentTrackLayout)

    # If there is setups for the default type, update the table.
    if len(setups[activeSetupType]) > 0:

        # If there is more setups than setupsPerPage, update the table with 5 first items and a spinner
        if len(setups[activeSetupType]) > GUIConfig.GUIConstants['setupsPerPage']:
            # ac.log(str(setupType)+' setups pages: '+str(len(setupList) / GUIConfig.GUIConstants['setupsPerPage']))

            updatePageSpinner(math.ceil(len(setups[activeSetupType]) / GUIConfig.GUIConstants['setupsPerPage']), 1)
        else:
            # ac.log('One page only')
            updateSetupsListingTable(setups[activeSetupType])

    # if there is no setups for this type, show empty table label.
    else:
        # ac.log('No '+str(setupType)+' setups')
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        updateSetupsListingTable(setups[activeSetupType][:5])


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


def onUploadButtonClick(*args):
    ac.log('onUploadButtonClick')

    tsm.uploadSetup(currentUploadFileName, currentUploadTrim, currentUploadBaseline, currentCarName, currentTrackBaseName, currentTrackLayout)


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

    hideUploadGUI()
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
    if not current_ac_version or not current_carId or not current_trackId or len(allSetupsFileNamesInFolder) == 0 or not userSteamCommunityID or not userExists:
        ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: disabling uploading...')
        uploadAvailability = False

    else:
        ac.log('TheSetupMarket logs | onRefreshUploadSectionButtonClick: enabling uploading...')
        uploadAvailability = True

    refreshUploadSection()
