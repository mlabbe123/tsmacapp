import sys
import ac
import acsys
import traceback
import functools
import math

try:
	from tsm import tsm
except Exception as e:
    ac.log('TheSetupMarket logs | error loading utils: '+traceback.format_exc())

from config import GUIConfig

tester=0
class testEvent:
    def __init__(self, appWindow, setupId, YPosition, setupFilename):
        self.bt = ac.addButton(appWindow, 'dl')
        ac.setSize(self.bt, 40, 25)
        ac.setPosition(self.bt, 10, YPosition)
        ac.setText(self.bt, 'dl')
        ac.drawBorder(self.bt, 0)
        self.event = functools.partial(self.downloadSetup, setupId=setupId, setupFilename=setupFilename)
        ac.addOnClickedListener(self.bt,self.event)

    def testOnClick(self, x,y, setupId, setupFilename):
        ac.console("clicked setupId : " + setupId + '. Setup Filename: '+setupFilename)

    def downloadSetup(self, x, y, setupId, setupFilename):
        global currentCarName, currentTrackName
        tsm.downloadSetup(setupId, setupFilename, currentCarName, currentTrackName)

def acMain(ac_version):
    global appWindow, currentCarName, currentTrackName, setupId, setupFilename, tester, setups, listingTables

    appWindow = ac.newApp("The Setup Market")
    ac.setSize(appWindow, 600, 800)

    listingTables = {
        'trackSpecific': {
            'row1': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row2': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row3': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row4': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row5': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            }
        },
        'anyTracks': {
            'row1': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row2': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row3': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row4': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row5': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            }
        },
        'otherTracks': {
            'row1': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row2': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row3': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row4': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            },
            'row5': {
                'dl_cell': ac.addLabel(appWindow, ''),
                'author_cell': ac.addLabel(appWindow, ''),
                'trim_cell': ac.addLabel(appWindow, ''),
                'bestlap_cell': ac.addLabel(appWindow, ''),
                'rating_cell': ac.addLabel(appWindow, ''),
                'downloads_cell': ac.addLabel(appWindow, ''),
                'acversion_cell': ac.addLabel(appWindow, ''),
                'version_cell': ac.addLabel(appWindow, '')
            }
        }
    }

    # Set the base GUI
    initGUI(appWindow)

    currentCarName = ac.getCarName(0)
    currentTrackName = ac.getTrackName(0)

    setups = tsm.getSetups(currentCarName, currentTrackName)
    YPosition = 100

    # if len(setups['trackSpecific']) > 0:
    #     if len(setups['trackSpecific']) <= 5:
    #         updateSetupsListingTable(setups['trackSpecific'], YPosition)
    #     else:
    #         firstPageSetups = []
    #         for setup in setups['trackSpecific'][:5]:
    #             firstPageSetups.append(setup)
    #
    #         updateSetupsListingTable(firstPageSetups, YPosition)
    #
    #     # Spinner for page change
    #     if len(setups['trackSpecific']) > GUIConfig.GUIConstants['setupsPerPage']:
    #         section1PageChangeSpinner = ac.addSpinner(appWindow, "Page:")
    #         ac.setPosition(section1PageChangeSpinner, 530, 260)
    #         ac.setSize(section1PageChangeSpinner, 60, 20)
    #
    #         #Set number of page
    #         totalPages = math.ceil(len(setups['trackSpecific']) / GUIConfig.GUIConstants['setupsPerPage'])
    #
    #         ac.setRange(section1PageChangeSpinner, 1, totalPages)
    #         ac.setValue(section1PageChangeSpinner, 1)
    #         ac.addOnValueChangeListener(section1PageChangeSpinner, onSection1PageChangeSpinnerClick)
    #
    # else:
    #     noSetupsLabel = ac.addLabel(appWindow, 'No setup for this car and track')
    #     ac.setSize(noSetupsLabel, 580, GUIConfig.GUIConstants['cellHeight'])
    #
    #     ac.drawBorder(noSetupsLabel, 0)
    #     ac.setVisible(noSetupsLabel, 1)
    #
    #     ac.setPosition(noSetupsLabel, 10, YPosition)
    #
    #     ac.setFontAlignment(noSetupsLabel, 'center')
    #
    # YPosition2 = 340
    # if len(setups['anyTracks']) > 0:
    #     rowNumber = 1
    #
    #     for setup in setups['anyTracks']:
    #         setupId = setup['_id']
    #         setupFilename = setup['file_name']
    #
    #         tester = testEvent(appWindow, setupId, YPosition2, setupFilename)
    #
    #         #download button cell
    #         #addDownloadButton(appWindow, GUIConfig.GUIConstants['tableRowColor'+str(rowNumber)+'R'], GUIConfig.GUIConstants['tableRowColor'+str(rowNumber)+'G'], GUIConfig.GUIConstants['tableRowColor'+str(rowNumber)+'B'], YPosition2)
    #
    #         #author display_name cell
    #         addTableCell(appWindow, setup['author']['display_name'], 210, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition2, 'center')
    #
    #         #setup trim cell
    #         addTableCell(appWindow, setup['type'], 50, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition2, 'center')
    #
    #         #setup best laptime cell
    #         addTableCell(appWindow, setup['best_time'], 90, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition2, 'center')
    #
    #         totalRating = 0
    #         for rating in setup['ratings']:
    #             totalRating += rating['rating']
    #
    #         if totalRating == 0:
    #             rating = 'n/a'
    #         else:
    #             rating = str(totalRating)
    #
    #         #setup rating cell
    #         addTableCell(appWindow, rating, 70, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition2, 'center')
    #
    #         #setup downloads cell
    #         addTableCell(appWindow, str(setup['downloads']), 40, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition2, 'center')
    #
    #         #setup AC version cell
    #         addTableCell(appWindow, str(setup['sim_version']), 30, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition2, 'center')
    #
    #         #setup version cell
    #         addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition2, 'center')
    #
    #         YPosition2 += GUIConfig.GUIConstants['cellHeight']
    #         rowNumber += 1
    #
    # elif len(setups['otherTracks']) > 0:
    #     rowNumber = 1
    #
    #     for setup in setups['otherTracks']:
    #         setupId = setup['_id']
    #         setupFilename = setup['file_name']
    #
    #         tester = testEvent(appWindow, setupId, YPosition2, setupFilename)
    #
    #         #download button cell
    #         #addDownloadButton(appWindow, GUIConfig.GUIConstants['tableRowColor'+str(rowNumber)+'R'], GUIConfig.GUIConstants['tableRowColor'+str(rowNumber)+'G'], GUIConfig.GUIConstants['tableRowColor'+str(rowNumber)+'B'], YPosition2)
    #
    #         #author display_name cell
    #         addTableCell(appWindow, setup['author']['display_name'], 210, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition2, 'center')
    #
    #         #setup trim cell
    #         addTableCell(appWindow, setup['type'], 50, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition2, 'center')
    #
    #         #setup best laptime cell
    #         addTableCell(appWindow, setup['best_time'], 90, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition2, 'center')
    #
    #         totalRating = 0
    #         for rating in setup['ratings']:
    #             totalRating += rating['rating']
    #
    #         if totalRating == 0:
    #             rating = 'n/a'
    #         else:
    #             rating = str(totalRating)
    #
    #         #setup rating cell
    #         addTableCell(appWindow, rating, 70, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition2, 'center')
    #
    #         #setup downloads cell
    #         addTableCell(appWindow, str(setup['downloads']), 40, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition2, 'center')
    #
    #         #setup AC version cell
    #         addTableCell(appWindow, str(setup['sim_version']), 30, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition2, 'center')
    #
    #         #setup version cell
    #         addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition2, 'center')
    #
    #         YPosition2 += GUIConfig.GUIConstants['cellHeight']
    #         rowNumber += 1
    # else:
    #     noSetupsLabel = ac.addLabel(appWindow, 'No setup for this car and other tracks')
    #     ac.setSize(noSetupsLabel, 580, GUIConfig.GUIConstants['cellHeight'])
    #
    #     #ac.setBackgroundColor(noSetupsLabel, r, g, b)
    #     #ac.setBackgroundOpacity(noSetupsLabel, 1)
    #     #ac.drawBackground(noSetupsLabel, 1)
    #     ac.drawBorder(noSetupsLabel, 0)
    #     ac.setVisible(noSetupsLabel, 1)
    #
    #     ac.setPosition(noSetupsLabel, 10, YPosition2)
    #
    #     ac.setFontAlignment(noSetupsLabel, 'center')

    return "The Setup Market"

def initGUI(appWindow):
    global section1Title, section2Title, listingTables

    ###################################
    ### Download section            ###
    ###################################

    ### Current track section ###
    section1Title = ac.addLabel(appWindow, "/Setups for current track")
    ac.setPosition(section1Title, 10, 35)

    # Add header row for track specific setups table
    addTableCell(appWindow, 'dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 60, 'center')
    addTableCell(appWindow, 'Author', 210, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 50, 60, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 260, 60, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 310, 60, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 390, 60, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 460, 60, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 60, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 60, 'center')

    ### Any track section ###
    section2Title = ac.addLabel(appWindow, "/Setups for no specific track")
    ac.setPosition(section2Title, 10, 235)

    # Add header row for Any track setups table
    addTableCell(appWindow, 'dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 260, 'center')
    addTableCell(appWindow, 'Author', 210, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 50, 260, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 260, 260, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 310, 260, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 390, 260, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 460, 260, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 260, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 260, 'center')

    section3Title=ac.addLabel(appWindow, "/Setups for other tracks")
    ac.setPosition(section3Title, 10, 435)
    
    # Add header row for other tracks setups table
    addTableCell(appWindow, 'dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 10, 460, 'center')
    addTableCell(appWindow, 'Author', 210, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 50, 460, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'],GUIConfig.GUIConstants['tableHeaderColorB'] , 260, 460, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConfig.GUIConstants['tableHeaderColorR'],GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 310, 460, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 390, 460, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 460, 460, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 500, 460, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConfig.GUIConstants['tableHeaderColorR'], GUIConfig.GUIConstants['tableHeaderColorG'], GUIConfig.GUIConstants['tableHeaderColorB'], 530, 460, 'center')

    # Init the setups listing table with empty labels

    for tableKey, listingTable in listingTables.items():
        yPos = GUIConfig.GUIConstants['tableLayout'][tableKey]['startingYPosition']
        rowNumber = 1

        for rowId, cells in listingTable.items():
            
            for cellId, label in cells.items():
                ac.log(tableKey+' :: '+rowId+' :: cellId: '+str(cellId)+', label: '+str(label)+'\n')
                ac.setPosition(label, GUIConfig.GUIConstants['tableLayout'][tableKey]['xPos'][cellId], yPos)
                ac.setText(label, '')
                ac.setSize(label, GUIConfig.GUIConstants['tableLayout'][tableKey]['cellXSize'][cellId], GUIConfig.GUIConstants['tableLayout']['cellHeight'])
                ac.setBackgroundColor(label, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) + 'B'])
                ac.setBackgroundOpacity(label, 1)
                ac.drawBackground(label, 1)
                ac.drawBorder(label, 0)
                ac.setVisible(label, 1)

            yPos += 25
            rowNumber += 1


        # for row in listingTable:
            # for cell in row:
                # ac.setPosition(cell, xPos, yPos)
                # xPos += 50
                # ac.setText(cell, 'caca')
                # ac.log('this is cell '+str(cell))
                # i += 1
                # ac.setSize(cell, 40, 25)
                # ac.setBackgroundColor(cell, 1, 0, 0)
                # ac.setBackgroundOpacity(cell, 1)
                # ac.drawBackground(cell, 1)
                # ac.drawBorder(cell, 0)
                # ac.setVisible(cell, 1)



    # Spinner for page change
    section2PageChangeSpinner = ac.addSpinner(appWindow, "Page2:")
    ac.setPosition(section2PageChangeSpinner, 530, 550)
    ac.setSize(section2PageChangeSpinner, 60, 10)
    ## Range will have to be passed as parameter to set the number of pages
    ac.setRange(section2PageChangeSpinner,1,2)
    ac.setValue(section2PageChangeSpinner,1)
    #ac.addOnValueChangeListener(section2PageChangeSpinner,onSection2PageChangeSpinnerClick)


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


def onSection1PageChangeSpinnerClick(x):
    ac.log(str(x))
    # Build the setup list to show in the listing table
    setupsToShow = buildSetupList('trackSpecific', str(x))
    updateSetupsListingTable2(setupsToShow, GUIConfig.GUIConstants['trackSpecificSetupsFirstRowYPosition'])


def onSection2PageChangeSpinnerClick(x):
    global section2Title
    ac.setText(section2Title, "Spinner: {0}".format(x))


def updateSetupsListingTable(setups, YPosition):
    rowNumber = 1

    for setup in setups:
        setupId = setup['_id']
        setupFilename = setup['file_name']

        tester = testEvent(appWindow, setupId, YPosition, setupFilename)

        #author display_name cell
        addTableCell(appWindow, setup['author']['display_name'], 210, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition, 'center')

        #setup trim cell
        addTableCell(appWindow, setup['type'], 50, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition, 'center')

        #setup best laptime cell
        addTableCell(appWindow, setup['best_time'], 90, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition, 'center')

        totalRating = 0
        for rating in setup['ratings']:
            totalRating += rating['rating']

        if totalRating == 0:
            rating = 'n/a'
        else:
            rating = str(totalRating)

        #setup rating cell
        addTableCell(appWindow, rating, 70, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition, 'center')

        #setup downloads cell
        addTableCell(appWindow, str(setup['downloads']), 40, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition, 'center')

        #setup AC version cell
        addTableCell(appWindow, str(setup['sim_version']), 30, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition, 'center')

        #setup version cell
        addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition, 'center')

        YPosition += GUIConfig.GUIConstants['cellHeight']


def updateSetupsListingTable2(setups, YPosition):
    rowNumber = 1

    # avec une ligne de pas commenté, ça pante au 6e clic (peu importe laquelle) :: 30 label de plus
    # avec 2 lignes de pas commenté, ça pante au 3e clic :: 30
    # avec 3 lignes de pas commenté, ça pante au 3e clic :: 45 (au 2e clic y'en a 30)
    # avec 4 lignes de pas commenté, ça pante au 2e clic :: 40
    # avec 5 lignes ou plus de pas commenté, ça pante au 1er clic :: 25
    # avec un seul setup, ça plante au 3e clic :: 24

    for setup in setups[:1]:
        setupId = setup['_id']
        setupFilename = setup['file_name']

        tester = testEvent(appWindow, setupId, YPosition, setupFilename) # avec juste cette ligne de pas commenté, ça pante au 6e clic

        #author display_name cell # avec juste cette ligne de pas commenté, ça pante au 6e clic
        addTableCell(appWindow, setup['author']['display_name'], 210, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition, 'center')

        #setup trim cell # avec juste cette ligne de pas commenté, ça pante au 6e clic
        addTableCell(appWindow, setup['type'], 50, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition, 'center')

        #setup best laptime cell
        addTableCell(appWindow, setup['best_time'], 90, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition, 'center')

        totalRating = 0
        for rating in setup['ratings']:
            totalRating += rating['rating']

        if totalRating == 0:
            rating = 'n/a'
        else:
            rating = str(totalRating)

        #setup rating cell
        addTableCell(appWindow, rating, 70, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition, 'center')

        #setup downloads cell
        addTableCell(appWindow, str(setup['downloads']), 40, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition, 'center')

        #setup AC version cell
        addTableCell(appWindow, str(setup['sim_version']), 30, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition, 'center')

        #setup version cell
        addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConfig.GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition, 'center')

        YPosition += GUIConfig.GUIConstants['cellHeight']


def buildSetupList(setupType, pageNumber):
    returnSetupsList = []

    numberOfItemsToGet = int(pageNumber) * GUIConfig.GUIConstants['setupsPerPage']

    for setup in setups[setupType][numberOfItemsToGet-GUIConfig.GUIConstants['setupsPerPage']:numberOfItemsToGet]:
        returnSetupsList.append(setup)

    return returnSetupsList