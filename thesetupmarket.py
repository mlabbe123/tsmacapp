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
    global appWindow, currentCarName, currentTrackBaseName, currentTrackFullName, currentTrackLayout, setupFilename, setups, listingTable, listingTableMisc, activeSetupType

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

    # Get current car/track/layout.
    currentCarName = ac.getCarName(0)
    currentTrackBaseName = ac.getTrackName(0)
    currentTrackLayout = ac.getTrackConfiguration(0)
    # Set the default active setup type
    activeSetupType = 'trackSpecific'

     # Set the base GUI
    initGUI(appWindow)

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
    ac.setVisible(listingTableSetupTypeButton, 1)
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

    # Add upload section message
    uploadText1 = ac.addLabel(appWindow, "Still in development, coming soon (tm)")
    ac.setPosition(uploadText1, 280, 256)

    # MINI SEPARATOR
    miniseparator = ac.addLabel(appWindow, '')
    ac.setSize(miniseparator, 100, 1)
    ac.setBackgroundColor(miniseparator, 1, 1, 1)
    ac.setBackgroundOpacity(miniseparator, 1)
    ac.drawBackground(miniseparator, 1)
    ac.drawBorder(miniseparator, 0)
    ac.setVisible(miniseparator, 1)
    ac.setPosition(miniseparator, 352, 282)

    uploadText2 = ac.addLabel(appWindow, "In the meantime, please create an account at thesetupmarket.com to upload setups.")
    ac.setPosition(uploadText2, 123, 286)


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

    if len(setups) < GUIConfig.GUIConstants['setupsPerPage']:
        ac.log('TheSetupMarket logs | setups length less than 5. Length = ' + str(len(setups)))
        # Set all remaining rows to not visible
        for index in range(GUIConfig.GUIConstants['setupsPerPage'] - len(setups)):
           for cellName, labelCtrl in listingTable[GUIConfig.GUIConstants['setupsPerPage'] - index].items():
               ac.setVisible(labelCtrl, 0)


def hideSetupsListingTable():
    for key, row in listingTable.items():
        for cellName, labelCtrl in row.items():
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

    # Hide setups listing table
    hideSetupsListingTable()
    ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
    ac.setText(listingTableMisc['emptyRowLabel']['label'], 'Loading...')

    # Get setups from api.
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
        # ac.log('No '+str(setupType)+' setups')
        ac.setVisible(listingTableMisc['emptyRowLabel']['label'], 1)
        updateSetupsListingTable(setups[activeSetupType][:5])
