import sys
import ac
# import acsys
import traceback
import functools
import math
from collections import OrderedDict

try:
	from tsm import tsm
except Exception as e:
    ac.log('TheSetupMarket logs | error loading utils: ' + traceback.format_exc())

from config import GUIConfig

tester=0
class testEvent:
    def __init__(self, appWindow, labelCtrl, setupId, setupFilename):
        # When page change occurs, event on top of events cause problems...

        # ac.log('setupId: '+str(setupId)+', setupFilename: '+str(setupFilename))
        self.event = functools.partial(self.downloadSetup, setupId=setupId, setupFilename=setupFilename)
        ac.addOnClickedListener(labelCtrl,self.event)


    def downloadSetup(self, x, y, setupId, setupFilename):
        global currentCarName, currentTrackName

        ac.log('Download --> setupId: '+str(setupId)+' | filename: '+setupFilename)
        tsm.downloadSetup(setupId, setupFilename, currentCarName, currentTrackName)


def acMain(ac_version):
    global appWindow, currentCarName, currentTrackName, setupId, setupFilename, tester, setups, listingTables, listingSpinners, listingTableMisc

    appWindow = ac.newApp("The Setup Market")
    ac.setSize(appWindow, 600, 655)

    listingTableMisc = {
        'trackSpecific': {
            'emptyRowLabel': {
                'label': ac.addLabel(appWindow, ''),
                'text': 'No setups for current car and track'
            },
            'loadingLabel': {
                'label': ac.addLabel(appWindow, ''),
                'text': 'Loading...'
            },
        },
        'anyTracks': {
            'emptyRowLabel': {
                'label': ac.addLabel(appWindow, ''),
                'text': 'No setups for current car and no specfic track'
            },
            'loadingLabel': {
                'label': ac.addLabel(appWindow, ''),
                'text': 'Loading...'
            },
        },
        'otherTracks': {
            'emptyRowLabel': {
                'label': ac.addLabel(appWindow, ''),
                'text': 'No setups for current car and other tracks'
            },
            'loadingLabel': {
                'label': ac.addLabel(appWindow, ''),
                'text': 'Loading...'
            },
        }
    }

    listingTables = {
        'trackSpecific': OrderedDict([
            (1, {
                'dl_cell': ac.addLabel(appWindow, ''),
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
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            })
        ]),
        'anyTracks': OrderedDict([
            (1, {
                'dl_cell': ac.addLabel(appWindow, ''),
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
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            })
        ]),
        'otherTracks': OrderedDict([
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
    }

    #spinners
    listingSpinners = {
        'trackSpecific': ac.addSpinner(appWindow, ''),
        'anyTracks': ac.addSpinner(appWindow, ''),
        'otherTracks': ac.addSpinner(appWindow, '')
    }

    # Set the base GUI
    initGUI(appWindow)

    # ac.log('carname: '+str(ac.getCarName(0)))
    # ac.log('trackname: '+str(ac.getTrackName(0)))
    # ac.log('trackconfig: '+str(ac.getTrackConfiguration(0)))

    currentCarName = ac.getCarName(0)
    if ac.getTrackConfiguration(0) != '':
        currentTrackName = ac.getTrackName(0) + '-' + ac.getTrackConfiguration(0)
    else:
        currentTrackName = ac.getTrackName(0)

    setups = tsm.getSetups(currentCarName, currentTrackName)

    for setupType, setupList in setups.items():

        if len(setupList) > 0:
            if len(setupList) > GUIConfig.GUIConstants['setupsPerPage']:
                # ac.log(str(setupType)+' setups pages: '+str(len(setupList) / GUIConfig.GUIConstants['setupsPerPage']))
                updateSetupsListingTable(setupType, setupList[:5])
                updatePageSpinner(setupType, math.ceil(len(setupList) / GUIConfig.GUIConstants['setupsPerPage']), 1)
            else:
                # ac.log('One page only')
                updateSetupsListingTable(setupType, setupList)
        else:
            # ac.log('No '+str(setupType)+' setups')
            ac.setVisible(listingTableMisc[setupType]['emptyRowLabel']['label'], 1)

    return "The Setup Market"


def initGUI(appWindow):
    global section1Title, section2Title, listingTables, listingTableMisc

    ###################################
    ### Download section            ###
    ###################################

    ### Current track section ###
    section1Title = ac.addLabel(appWindow, "/Setups for current track")
    ac.setPosition(section1Title, 10, 31)

    # Add header row for track specific setups table
    addTableCell(appWindow, '', 35, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 53, 'center')
    addTableCell(appWindow, 'Author', 225, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 35, 53, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 260, 53, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 310, 53, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 390, 53, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 460, 53, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 53, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 53, 'center')

    ### Any track section ###
    section2Title = ac.addLabel(appWindow, "/Setups for no specific track")
    ac.setPosition(section2Title, 10, 199)

    # Add header row for Any track setups table
    addTableCell(appWindow, '', 35, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 222, 'center')
    addTableCell(appWindow, 'Author', 225, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 35, 222, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 260, 222, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 310, 222, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 390, 222, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 460, 222, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 222, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 222, 'center')

    section3Title=ac.addLabel(appWindow, "/Setups for other tracks")
    ac.setPosition(section3Title, 10, 367)
    
    # Add header row for other tracks setups table
    addTableCell(appWindow, '', 35, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 389, 'center')
    addTableCell(appWindow, 'Track', 125, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 35, 389, 'center')
    addTableCell(appWindow, 'Author', 100, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 160, 389, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 260, 389, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 310, 389, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 390, 389, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 460, 389, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 389, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 389, 'center')

    # SEPARATOR
    separator = ac.addLabel(appWindow, '')

    ac.setSize(separator, 600, 2)

    ac.setBackgroundColor(separator, 1, 1, 1)
    ac.setBackgroundOpacity(separator, 1)
    ac.drawBackground(separator, 1)
    ac.drawBorder(separator, 0)
    ac.setVisible(separator, 1)

    ac.setPosition(separator, 0, 559)

    # Add upload section title
    section4Title = ac.addLabel(appWindow, "/Upload setup")
    ac.setPosition(section4Title, 10, 564)

    # Add upload section message
    uploadText1 = ac.addLabel(appWindow, "Still in development, coming soon (tm)")
    ac.setPosition(uploadText1, 180, 592)
    uploadText2 = ac.addLabel(appWindow, "In the meantime, go to thesetupmarket.com to create an account and upload your setup.")
    ac.setPosition(uploadText2, 6, 613)

    # Init the setups listing table with empty labels
    for tableKey, listingTable in listingTables.items():
        yPos = GUIConfig.GUIConstants['tableLayout'][tableKey]['startingYPosition']
        rowNumber = 1
        # ac.log(str(listingTable))

        for key, cells in listingTable.items():
            # ac.log('tableKey: '+tableKey+' | rowId: '+str(key))
            
            for cellId, label in cells.items():
                #ac.log(tableKey+' :: '+rowId+' :: cellId: '+str(cellId)+', label: '+str(label)+'\n')
                ac.setPosition(label, GUIConfig.GUIConstants['tableLayout'][tableKey]['xPos'][cellId], yPos)
                ac.setText(label, '')
                ac.setSize(label, GUIConfig.GUIConstants['tableLayout'][tableKey]['cellXSize'][cellId], GUIConfig.GUIConstants['tableLayout']['cellHeight'])
                ac.setBackgroundColor(label, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'B'])
                ac.setBackgroundOpacity(label, 1)
                ac.drawBackground(label, 1)
                ac.drawBorder(label, 0)
                ac.setVisible(label, 0)
                ac.setFontAlignment(label, 'center')

            yPos += GUIConfig.GUIConstants['tableLayout']['cellHeight'] + 1
            rowNumber += 1

    for tableKey, labels in listingTableMisc.items():

        for labelName, labelConfig in labels.items():
            labelCtrl = labelConfig['label']
            labelText = labelConfig['text']

            ac.setText(labelCtrl, labelText)
            ac.setPosition(labelCtrl, 10, GUIConfig.GUIConstants['tableLayout'][tableKey]['startingYPosition'] + GUIConfig.GUIConstants['tableLayout']['cellHeight'] * 2)
            ac.setSize(labelCtrl, 580, GUIConfig.GUIConstants['tableLayout']['cellHeight'])
            ac.drawBorder(labelCtrl, 0)
            ac.setVisible(labelCtrl, 0)
            ac.setFontAlignment(labelCtrl, 'center')

    for tableKey, spinner in listingSpinners.items():
        ac.setPosition(spinner, 530, GUIConfig.GUIConstants['tableLayout'][tableKey]['startingYPosition'] + 111)
        ac.setSize(spinner, 60, 20)
        ac.setVisible(spinner, 0)


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


def updateSetupsListingTable(setupCategory, setups):
    rowNumber = 1

    for setup in setups:
        setupId = setup['_id']
        setupFilename = setup['file_name']

        # ac.log('Row '+str(rowNumber)+'----------------------')
        for cellName, labelCtrl in listingTables[setupCategory][rowNumber].items():
            ac.setVisible(labelCtrl, 1)

            if cellName == 'dl_cell':
                # ac.log('Download cell')
                ac.setBackgroundTexture(labelCtrl, 'apps/python/thesetupmarket/img/dl_bg_alt.png')
                tester = testEvent(appWindow, labelCtrl, setupId, setupFilename)
            elif cellName == 'track_cell':
                ac.log(setup['track']['name'])
                ac.setText(labelCtrl, setup['track']['name'])
            elif cellName == 'author_cell':
                # ac.log(setup['author']['display_name'])
                ac.setText(labelCtrl, setup['author']['display_name'])
            elif cellName == 'trim_cell' :
                # ac.log(setup['type'])
                ac.setText(labelCtrl, setup['type'])
            elif cellName == 'bestlap_cell':
                bestlap = 'n/a'
                if setup['best_time'] != '':
                    bestlap = setup['best_time']

                # ac.log(bestlap)
                ac.setText(labelCtrl, bestlap)
            elif cellName == 'rating_cell':
                totalRating = 0

                for rating in setup['ratings']:
                    totalRating += rating['rating']

                if totalRating == 0:
                    rating = 'n/a'
                else:
                    rating = str(totalRating)

                # ac.log('Rating: '+str(rating))
                ac.setText(labelCtrl, str(rating))

            elif cellName == 'downloads_cell':
                # ac.log('Downloads: '+str(setup['downloads']))
                ac.setText(labelCtrl, str(setup['downloads']))
            elif cellName == 'acversion_cell':
                # ac.log('Ac version: '+str(setup['sim_version']))
                ac.setText(labelCtrl, str(setup['sim_version']))
            elif cellName == 'version_cell':
                # ac.log('Version: v'+str(setup['version']))
                ac.setText(labelCtrl, 'v'+str(setup['version']))

        rowNumber += 1


def updatePageSpinner(setupType, pageCount, currentValue):
    global listingSpinners

    spinner = listingSpinners[setupType]

    ac.setVisible(spinner, 1)
    ac.setRange(spinner, 1, pageCount)
    ac.setValue(spinner, currentValue)

    if setupType == 'trackSpecific':
        ac.addOnValueChangeListener(spinner, onTrackSpecificPageChangeSpinnerClick)
    elif setupType == 'anyTracks':
        ac.addOnValueChangeListener(spinner, onAnyTrackPageChangeSpinnerClick)
    elif setupType == 'otherTracks':
        ac.addOnValueChangeListener(spinner, onOtherTracksPageChangeSpinnerClick)


def onTrackSpecificPageChangeSpinnerClick(x):
    global setups

    fromIndex = x * GUIConfig.GUIConstants['setupsPerPage'] - GUIConfig.GUIConstants['setupsPerPage']
    toIndex = x * GUIConfig.GUIConstants['setupsPerPage']

    updateSetupsListingTable('trackSpecific', setups['trackSpecific'][fromIndex:toIndex])


def onAnyTrackPageChangeSpinnerClick(x):
    ac.console('onAnyTrackPageChangeSpinnerClick :: page: '+str(x))
    global setups

    fromIndex = x * GUIConfig.GUIConstants['setupsPerPage'] - GUIConfig.GUIConstants['setupsPerPage']
    toIndex = x * GUIConfig.GUIConstants['setupsPerPage']

    updateSetupsListingTable('anyTracks', setups['anyTracks'][fromIndex:toIndex])


def onOtherTracksPageChangeSpinnerClick(x):
    ac.console('onOtherTracksPageChangeSpinnerClick :: page: '+str(x))
    global setups

    fromIndex = x * GUIConfig.GUIConstants['setupsPerPage'] - GUIConfig.GUIConstants['setupsPerPage']
    toIndex = x * GUIConfig.GUIConstants['setupsPerPage']

    updateSetupsListingTable('otherTracks', setups['otherTracks'][fromIndex:toIndex])