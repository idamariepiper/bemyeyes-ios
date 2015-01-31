#!/usr/bin/python

"""
Usage:
	update_translations.py -p <project-key>
"""

import urllib, sys, getopt, os, json, shutil
from zipfile import ZipFile

PROJECT_ID = "bemyeyes"
ENDPOINT = "https://api.crowdin.com/api/project/{projectID}/download/{package}.zip?key={projectKey}"
LANG_STATUS_ENDPOINT = "https://api.crowdin.com/api/project/{projectID}/status?key={projectKey}&jsonp"
FILENAME = "languages.zip"
APP_STORE_DESCRIPTION = "AppStore.txt"
APP_STORE_DESCRIPTIONS_DIR = "AppStoreDescriptions"
EXTRACTION_DIR = "Localization"
RENAME_RULES = {'zh-CN':'zh-Hant', 'zh-TW' : 'zh-Hans', 'ur-PK' : 'ur', 'es-ES' : 'es', 'sv-SE' : 'sv', 'pt-PT' : 'pt'}
APP_LANGUAGES = ['af','ar','ca','cs','da','de','el','es-ES','fi','fr','he','hi','hr','hu', 'lt','ja','ko','it','nb','nl','no', 'nb','pl','pt-BR','pt-PT','ro','ru','sk','sr','sv-SE','tr','uk','ur-PK','vi','zh-TW','zh-CN']


def usage():
	print(__doc__)


def fetchLanguages(projectKey):
	"""
	This function fetches all translations in a zipped file
	and returns the name of the downloaded file or an error.
	"""
	try:
		languagesURL = ENDPOINT.format(projectID=PROJECT_ID, package="all", projectKey=projectKey)
		(filename, headers) = urllib.urlretrieve(languagesURL, FILENAME)
	except BaseException as e:
		return (None, e)
	else:
		return (filename, None)
	
	
def unzipFile(filename):
	"""
	Unzips the file containing translations.
	Returns name of the directory where files were extracted.
	"""
	try:
		file = ZipFile(filename)
		file.extractall(EXTRACTION_DIR)
	except zipfile.BadZipFile as e:
		print("Error while unzipping: {0}".format(e.strerror))
		sys.exist(2)
	except zipfile.LargeZipFile as e:
		print("Error while unzipping: {0}".format(e.strerror))
		sys.exist(2)
	return EXTRACTION_DIR
	
	
def renameAndRemoveDirectories(parentDir, renameRules, fullyTranslated):
	"""
	Renames folders by following the RENAME_RULES and adds the .lproj suffix.
	Removes folders for languages that have not been fully translated.
	"""
	extractedDir = os.path.join(os.getcwd(), parentDir)
	dirsList = [name for name in os.listdir(extractedDir)
	            if os.path.isdir(os.path.join(extractedDir, name))]
	try:
		for dir in dirsList:
			if dir in fullyTranslated:
				dirName = dir + ".lproj"
				if dir in renameRules:
					dirName = renameRules[dir] + ".lproj"
				os.rename(os.path.join(extractedDir, dir), os.path.join(extractedDir, dirName))
			else:
				shutil.rmtree(os.path.join(extractedDir, dir))
	except OSError as error:
		print(error.strerror)


def moveAppStoreDescriptions(dirName):
	"""
	Moves all AppStore.txt files into a separate directory.
	"""
	descriptionsDir = ''
	try:
		descriptionsDir = appStoreDescriptionsExtractPath()
		os.mkdir(descriptionsDir)
		
		extractedDir = os.path.join(os.getcwd(), dirName)
		dirsList = [name for name in os.listdir(extractedDir)
				            if os.path.isdir(os.path.join(extractedDir, name))]
		for dir in dirsList:
			fromPath = os.path.join(extractedDir, dir, APP_STORE_DESCRIPTION)
			toPath = os.path.join(descriptionsDir, dir, APP_STORE_DESCRIPTION)
			newDir = os.path.join(descriptionsDir, dir)
			os.mkdir(newDir)
			shutil.move(fromPath, toPath)

	except OSError as e:
		print(e.strerror)
		sys.exit(2)
			

def fetchLanguageStatus(projectKey):
	"""
	Fetches info about languages to determine which ones
	have been fully translated.
	"""
	fullyTranslated = []
	try:
		statusURL = LANG_STATUS_ENDPOINT.format(projectID=PROJECT_ID, projectKey=projectKey)
		f = urllib.urlopen(statusURL)
		r = f.read()[1:-2]
		response = json.loads(r)
		f.close()
	except BaseException as e:
		print(e)
	else:
		for status in response:
			languageCode = status["code"]
			progress = int(status["translated_progress"])
			langName = status["name"]
			if isAcceptable(languageCode):
				fullyTranslated.append(languageCode)
			elif(isLanguageReady(progress)):
				print("""{0} (code: {1}) is ready. Please add its code"""
				""" to APP_LANGUAGES list at the top of this script.""".format(langName, languageCode))
	return fullyTranslated

def isLanguageReady(progress):
	return (progress == 100)

def isAcceptable(languageCode):
	"""
	Function evaluating whether a translation is acceptable based
	on its progress.
	"""
	if languageCode in APP_LANGUAGES:
		return True
	else:
		return False


def moveTranslations():
	"""
	Move translations to the right folder in the project.
	"""
	#move Base.lproj out
	try:
		shutil.move(baseLprojPathCurrent(), baseLprojPathNew())
	except IOError as e:
		print("Error while moving Base.lproj: {0}".format(e.strerror))
	
	#remove the whole Localization folder
	try:
		shutil.rmtree(localizationDirPath())
	except OSError as e:
		print("Error while removing existing localizations: {0}".format(e.strerror))
	
	#move extracted languages to the right folder
	try:
		shutil.move(extractedLocalizationDirPath(), localizationDirPath())
	except OSError as e:
		print("Error while moving localizations: {0}".format(e.strerror))
		
	#move Base.lproj back
	try:
		shutil.move(baseLprojPathNew(), baseLprojPathCurrent())
	except IOError as e:
		print("Error while moving Base.lproj: {0}".format(e.strerror))
		
	#move AppStoreDescriptions into the Localization folder
	try:
		shutil.move(appStoreDescriptionsExtractPath(), appStoreDescriotionsCopyPath())
	except IOError as e:
		print("Error while moving AppStoreDescriptions: {0}".format(e.strerror))
	

def cleanUp(downloadedTranslationsFile):
	"""
	Remove redundant files
	"""
	try:
		os.remove(os.path.join(os.getcwd(), downloadedTranslationsFile))
	except IOError as e:
		print("Error while deleting the downloaded translations: {0}".format(e.strerror))
	
##### Paths #####

def extractedLocalizationDirPath():
	return os.path.join(os.getcwd(), EXTRACTION_DIR)

def localizationDirPath():
	parent = os.path.join(os.getcwd(), os.pardir)
	return os.path.join(parent, "BeMyEyes", "Localization")
	
def baseLprojPathCurrent():
	return os.path.join(localizationDirPath(), "Base.lproj")
	
def baseLprojPathNew():
	parent = os.path.join(os.getcwd(), os.pardir)
	return os.path.join(parent, "Base.lproj")
	
def appStoreDescriptionsExtractPath():
	return os.path.join(os.getcwd(), APP_STORE_DESCRIPTIONS_DIR)
	
def appStoreDescriotionsCopyPath():
	return os.path.join(localizationDirPath(), APP_STORE_DESCRIPTIONS_DIR)

##### Main #####

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "p:")
		if len(opts) != 1:
			usage()
			sys.exit(2)
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	else:
		projectKey = ''
		for opt, arg in opts:
			if opt == "-p":
				projectKey = arg
			else:
				usage()
				sys.exit(2)
		
		fullyTranslated = fetchLanguageStatus(projectKey)
		(filename, exception) = fetchLanguages(projectKey)
		
		if filename:
			dirName = unzipFile(filename)
			renameAndRemoveDirectories(dirName, RENAME_RULES, fullyTranslated)
			moveAppStoreDescriptions(dirName)
			moveTranslations()
			cleanUp(filename)
			print("All done!")
		else:
			print(exception.strerror)
	