from sys import exit
from configparser import ConfigParser
import os.path
from plexapi.server import PlexServer
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
config_filepath = dir_path+"/config.ini"
exists = os.path.exists(config_filepath)
config = None
if exists:
    print("--------config.ini file found at ", config_filepath)
    config = ConfigParser()
    config.read(config_filepath)
else:
    print("---------config.ini file NOT FOUND at ", config_filepath)
    exit(0)


serverSettings = config["SERVER"]

plexHost = serverSettings['plexHost']
plexToken = serverSettings['plexToken']
plexLibraryName = serverSettings['plexLibraryName']

plexServer = PlexServer(plexHost, plexToken)
tvLibrary = plexServer.library.section(plexLibraryName)

configOptions = config["OPTIONS"]
debugging = configOptions.getboolean('debugging')
dryRun = configOptions.getboolean('dryRun')
tryAltTitleIfNoEpisodeIndicator = configOptions.getboolean('tryAltTitleIfNoEpisodeIndicator')
seriesTitle = configOptions['seriesTitle']
seriesYear = int(configOptions['seriesYear'])

def Main():
    if seriesYear > 0: showsFound = tvLibrary.searchShows(title=seriesTitle, year=seriesYear)
    else: showsFound = tvLibrary.searchShows(title=seriesTitle)
    
    if EvaluateFailureConditionAndLog( len(showsFound) == 0, seriesTitle + ', year: ' + str(seriesYear) + ' NOT FOUND in library ' + plexLibraryName): 
        exit(1)

    if len(showsFound) > 1:
        combinedTitles = ''
        for show in showsFound:
            combinedTitles = combinedTitles + '"' + show.title + '", '
        print('Multiple series found with title ' + seriesTitle + ', they include ' + combinedTitles + 'please be more specific')
        exit(0)

    show = showsFound[0]
    print(show.title + ' (' + str(show.year) + ') Found!')

    showEpisodes = show.episodes()
    if EvaluateFailureConditionAndLog(not showEpisodes, 'Episodes not found'): 
        exit(1)

    for episode in showEpisodes:
        print('\nStarting Title Cleanup for episode titled ' + episode.title)
        EvaluateFailureConditionAndLog(not episode.media or not episode.media[0] or not episode.media[0].parts or not episode.media[0].parts[0], 'Episode or episode parts not found')
        formattedTitle = GetFormattedTitle(episode)
        if not formattedTitle:
            print('Failed to find acceptable title, continuing')
            continue

        print('New Title: ' + formattedTitle)
        if dryRun: print('Dry Run is enabled, not committing change')
        else:
            print('Dry Run is false, COMMITTING TITLE CHANGE')
            episode.edit(**{"title.value": formattedTitle, 'title.locked': 1})
            episode.reload()

def GetFormattedTitle(episode):
    filePath = episode.media[0].parts[0].file
    filePathFromFoundStart = ''
    finalTitle = ''

    if debugging: print('filePath: ' + filePath)

    extIndex = filePath.rfind('.')
    filePathNoExt = filePath[0:extIndex]
    if debugging: print('File Path Without Extension: ' + filePathNoExt)

    (episodeIndicatorFound) = re.search('e.[0-9]', filePathNoExt, re.I)

    if (episodeIndicatorFound): 
        episodeIndicatorIndex = (episodeIndicatorFound).start()
        filePathFromEpIndicator = filePathNoExt[episodeIndicatorIndex:]
        firstSpaceNum = filePathFromEpIndicator.find(' ')
        filePathFromFoundStart = filePathFromEpIndicator[firstSpaceNum:]
    else:
        print( 'Episode Indicator (S0xE0x) not found for ' + filePathNoExt + ', this means the file does not contain the letter E next to a digit, indicating where the title should start')
        if tryAltTitleIfNoEpisodeIndicator: print('Trying to find alternative title start')
        else:
            print('TryAltTitleIfNoEpisodeIndicator is false, skipping title')
            return None
        alternativeTitleStartIndex = filePathNoExt.rfind("-")
        if alternativeTitleStartIndex == -1: alternativeTitleStartIndex = filePathNoExt.rfind("\\")
        if alternativeTitleStartIndex == -1: alternativeTitleStartIndex = 0 # - or | not found
        else: 
            print('Found "-" or "/" in file name, using as title start basis')
            alternativeTitleStartIndex += 1 # next index after the found \ or -
        filePathFromFoundStart = filePathNoExt[alternativeTitleStartIndex:]

            
    if not filePathFromFoundStart[0].isalnum(): 
        firstLetterFound = re.search(r'[a-z]', filePathFromFoundStart, re.I)
        firstLetterIndex = firstLetterFound.start() if firstLetterFound != None else -1
        firstDigitFound = re.search(r'[0-9]', filePathFromFoundStart, re.I)
        firstDigitIndex = firstDigitFound.start() if firstDigitFound != None else -1

        firstAlphaNum = 999
        if firstLetterIndex > -1: firstAlphaNum = firstLetterIndex
        if firstDigitIndex > -1 and firstDigitIndex < firstAlphaNum: firstAlphaNum = firstDigitIndex
        if firstAlphaNum == 999: firstAlphaNum = 0 

        finalTitle = filePathFromFoundStart[firstAlphaNum:]
    else:  finalTitle = filePathFromFoundStart
        
    return finalTitle
        
    
def EvaluateFailureConditionAndLog(condition, log):
    if condition: print(log)
    
    return condition

Main()