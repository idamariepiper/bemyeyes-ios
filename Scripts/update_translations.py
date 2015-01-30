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
APP_STORE_DESCRIPTIONS_DIR = "app_store_descriptions"
EXTRACTION_DIR = "extracted_languages"
RENAME_RULES = {'zh-CN':'zh-Hant', 'zh-TW' : 'zh-Hans', 'ur-PK' : 'ur', 'es-ES' : 'es', 'sv-SE' : 'sv', 'pt-PT' : 'pt'}

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
				print("{0} -> {1}".format(dir, dirName))
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
		descriptionsDir = os.path.join(os.getcwd(), APP_STORE_DESCRIPTIONS_DIR)
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
			progressString = status["translated_progress"]
			progress = int(progressString)
			if isAcceptable(progress):
				fullyTranslated.append(status["code"])
	return fullyTranslated


def isAcceptable(progress):
	"""
	Function evaluating whether a translation is acceptable based
	on its progress.
	"""
	if progress == 100:
		return True
	else:
		return False


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
		else:
			print(exception.strerror)
	