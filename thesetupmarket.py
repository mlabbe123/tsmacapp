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

# 10 + 40 + 210 + 50 + 90 + 60 + 40 + 30 + 60 + 10 = 600 (600)
GUIConstants = {
    'cellHeight': 25,
    'tableHeaderColorR': 0.25,
    'tableHeaderColorG': 0.66,
    'tableHeaderColorB': 0.66,
    'tableRowColor1R': 0.9098,
    'tableRowColor1G': 0.6,
    'tableRowColor1B': 0.2706,
    'tableRowColor2R': 0.9922,
    'tableRowColor2G': 0.6706,
    'tableRowColor2B': 0.1882,
    'tableRowColor3R': 1,
    'tableRowColor3G': 0.6039,
    'tableRowColor3B': 0.1804,
    'tableRowColor4R': 0.9922,
    'tableRowColor4G': 0.6314,
    'tableRowColor4B': 0.1882,
    'tableRowColor5R': 0.9294,
    'tableRowColor5G': 0.6,
    'tableRowColor5B': 0.251,
    'setupsPerPage': 5,
    'trackSpecificSetupsFirstRowYPosition': 100
}

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
    global appWindow, currentCarName, currentTrackName, setupId, setupFilename, tester, setups

    appWindow = ac.newApp("The Setup Market")
    ac.setSize(appWindow, 600, 600)

    # Set the base GUI
    initGUI(appWindow)

    # Add header row for track specific setups table
    addTableCell(appWindow, 'dl', 40, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 10, 75, 'center')
    addTableCell(appWindow, 'Author', 210, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 50, 75, 'center')
    addTableCell(appWindow, 'Trim', 50, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'],GUIConstants['tableHeaderColorB'] , 260, 75, 'center')
    addTableCell(appWindow, 'Best Time', 90, GUIConstants['tableHeaderColorR'],GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 310, 75, 'center')
    addTableCell(appWindow, 'Rating', 70, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 390, 75, 'center')
    addTableCell(appWindow, 'Dl', 40, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 460, 75, 'center')
    addTableCell(appWindow, 'AC', 30, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 500, 75, 'center')
    addTableCell(appWindow, 'Version', 60, GUIConstants['tableHeaderColorR'], GUIConstants['tableHeaderColorG'], GUIConstants['tableHeaderColorB'], 530, 75, 'center')

    currentCarName = ac.getCarName(0)
    currentTrackName = ac.getTrackName(0)

    setups = tsm.getSetups(currentCarName, currentTrackName)
    YPosition = 100

    if len(setups['trackSpecific']) > 0:
        if len(setups['trackSpecific']) <= 5:
            updateSetupsListingTable(setups['trackSpecific'], YPosition)
        else:
            firstPageSetups = []
            for setup in setups['trackSpecific'][:5]:
                firstPageSetups.append(setup)

            updateSetupsListingTable(firstPageSetups, YPosition)

        # Spinner for page change
        if len(setups['trackSpecific']) > GUIConstants['setupsPerPage']:
            section1PageChangeSpinner = ac.addSpinner(appWindow, "Page:")
            ac.setPosition(section1PageChangeSpinner, 530, 260)
            ac.setSize(section1PageChangeSpinner, 60, 20)

            #Set number of page
            totalPages = math.ceil(len(setups['trackSpecific']) / GUIConstants['setupsPerPage'])

            ac.setRange(section1PageChangeSpinner, 1, totalPages)
            ac.setValue(section1PageChangeSpinner, 1)
            ac.addOnValueChangeListener(section1PageChangeSpinner, onSection1PageChangeSpinnerClick)

    else:
        noSetupsLabel = ac.addLabel(appWindow, 'No setup for this car and track')
        ac.setSize(noSetupsLabel, 580, GUIConstants['cellHeight'])

        ac.drawBorder(noSetupsLabel, 0)
        ac.setVisible(noSetupsLabel, 1)

        ac.setPosition(noSetupsLabel, 10, YPosition)

        ac.setFontAlignment(noSetupsLabel, 'center')

    YPosition2 = 340
    if len(setups['anyTracks']) > 0:
        rowNumber = 1

        for setup in setups['anyTracks']:
            setupId = setup['_id']
            setupFilename = setup['file_name']

            tester = testEvent(appWindow, setupId, YPosition2, setupFilename)

            #download button cell
            #addDownloadButton(appWindow, GUIConstants['tableRowColor'+str(rowNumber)+'R'], GUIConstants['tableRowColor'+str(rowNumber)+'G'], GUIConstants['tableRowColor'+str(rowNumber)+'B'], YPosition2)

            #author display_name cell
            addTableCell(appWindow, setup['author']['display_name'], 210, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition2, 'center')

            #setup trim cell
            addTableCell(appWindow, setup['type'], 50, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition2, 'center')

            #setup best laptime cell
            addTableCell(appWindow, setup['best_time'], 90, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition2, 'center')

            totalRating = 0
            for rating in setup['ratings']:
                totalRating += rating['rating']

            if totalRating == 0:
                rating = 'n/a'
            else:
                rating = str(totalRating)

            #setup rating cell
            addTableCell(appWindow, rating, 70, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition2, 'center')

            #setup downloads cell
            addTableCell(appWindow, str(setup['downloads']), 40, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition2, 'center')

            #setup AC version cell
            addTableCell(appWindow, str(setup['sim_version']), 30, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition2, 'center')

            #setup version cell
            addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition2, 'center')

            YPosition2 += GUIConstants['cellHeight']
            rowNumber += 1

    elif len(setups['otherTracks']) > 0:
        rowNumber = 1

        for setup in setups['otherTracks']:
            setupId = setup['_id']
            setupFilename = setup['file_name']

            tester = testEvent(appWindow, setupId, YPosition2, setupFilename)

            #download button cell
            #addDownloadButton(appWindow, GUIConstants['tableRowColor'+str(rowNumber)+'R'], GUIConstants['tableRowColor'+str(rowNumber)+'G'], GUIConstants['tableRowColor'+str(rowNumber)+'B'], YPosition2)

            #author display_name cell
            addTableCell(appWindow, setup['author']['display_name'], 210, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition2, 'center')

            #setup trim cell
            addTableCell(appWindow, setup['type'], 50, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition2, 'center')

            #setup best laptime cell
            addTableCell(appWindow, setup['best_time'], 90, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition2, 'center')

            totalRating = 0
            for rating in setup['ratings']:
                totalRating += rating['rating']

            if totalRating == 0:
                rating = 'n/a'
            else:
                rating = str(totalRating)

            #setup rating cell
            addTableCell(appWindow, rating, 70, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition2, 'center')

            #setup downloads cell
            addTableCell(appWindow, str(setup['downloads']), 40, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition2, 'center')

            #setup AC version cell
            addTableCell(appWindow, str(setup['sim_version']), 30, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition2, 'center')

            #setup version cell
            addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition2, 'center')

            YPosition2 += GUIConstants['cellHeight']
            rowNumber += 1
    else:
        noSetupsLabel = ac.addLabel(appWindow, 'No setup for this car and other tracks')
        ac.setSize(noSetupsLabel, 580, GUIConstants['cellHeight'])

        #ac.setBackgroundColor(noSetupsLabel, r, g, b)
        #ac.setBackgroundOpacity(noSetupsLabel, 1)
        #ac.drawBackground(noSetupsLabel, 1)
        ac.drawBorder(noSetupsLabel, 0)
        ac.setVisible(noSetupsLabel, 1)

        ac.setPosition(noSetupsLabel, 10, YPosition2)

        ac.setFontAlignment(noSetupsLabel, 'center')

    return "The Setup Market"

def initGUI(appWindow):
    global section1Title, section2Title

    ###################################
    ### Download section            ###
    ###################################

    ### Current track section ###
    section1Title=ac.addLabel(appWindow,"/Setups for current track")
    ac.setPosition(section1Title,10,50)

    ### Any/Other tracks section ###
    section2Title=ac.addLabel(appWindow,"/Setups for no specific track")
    # TEXT WILL CHANGE BASED ON IF THERE IS SETUPS FOR ANY TRACKS. IF NOT, THEN SHOW SETUPS FOR OTHER TRACKS
    #section2Title=ac.addLabel(appWindow,"/Setups for other tracks")
    ac.setPosition(section2Title,10,300)

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

    ac.setSize(cell, sizeX, GUIConstants['cellHeight'])

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
    updateSetupsListingTable2(setupsToShow, GUIConstants['trackSpecificSetupsFirstRowYPosition'])


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
        addTableCell(appWindow, setup['author']['display_name'], 210, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition, 'center')

        #setup trim cell
        addTableCell(appWindow, setup['type'], 50, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition, 'center')

        #setup best laptime cell
        addTableCell(appWindow, setup['best_time'], 90, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition, 'center')

        totalRating = 0
        for rating in setup['ratings']:
            totalRating += rating['rating']

        if totalRating == 0:
            rating = 'n/a'
        else:
            rating = str(totalRating)

        #setup rating cell
        addTableCell(appWindow, rating, 70, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition, 'center')

        #setup downloads cell
        addTableCell(appWindow, str(setup['downloads']), 40, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition, 'center')

        #setup AC version cell
        addTableCell(appWindow, str(setup['sim_version']), 30, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition, 'center')

        #setup version cell
        addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition, 'center')

        YPosition += GUIConstants['cellHeight']


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
        addTableCell(appWindow, setup['author']['display_name'], 210, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 50, YPosition, 'center')

        #setup trim cell # avec juste cette ligne de pas commenté, ça pante au 6e clic
        addTableCell(appWindow, setup['type'], 50, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 260, YPosition, 'center')

        #setup best laptime cell
        addTableCell(appWindow, setup['best_time'], 90, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 310, YPosition, 'center')

        totalRating = 0
        for rating in setup['ratings']:
            totalRating += rating['rating']

        if totalRating == 0:
            rating = 'n/a'
        else:
            rating = str(totalRating)

        #setup rating cell
        addTableCell(appWindow, rating, 70, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 390, YPosition, 'center')

        #setup downloads cell
        addTableCell(appWindow, str(setup['downloads']), 40, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 460, YPosition, 'center')

        #setup AC version cell
        addTableCell(appWindow, str(setup['sim_version']), 30, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 500, YPosition, 'center')

        #setup version cell
        addTableCell(appWindow, 'v'+str(setup['version']), 60, GUIConstants['tableRowColor' + str(rowNumber) +'R'], GUIConstants['tableRowColor' + str(rowNumber) +'G'], GUIConstants['tableRowColor' + str(rowNumber) +'B'], 530, YPosition, 'center')

        YPosition += GUIConstants['cellHeight']


def buildSetupList(setupType, pageNumber):
    returnSetupsList = []

    numberOfItemsToGet = int(pageNumber) * GUIConstants['setupsPerPage']

    for setup in setups[setupType][numberOfItemsToGet-GUIConstants['setupsPerPage']:numberOfItemsToGet]:
        returnSetupsList.append(setup)

    return returnSetupsList