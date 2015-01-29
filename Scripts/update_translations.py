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
EXTRACTION_DIR = "extracted_languages"
RENAME_RULES = {'zh-CN':'zh-Hant', 'zh-TW' : 'zh-Hans', 'ur-PK' : 'ur', 'es-ES' : 'es', 'sv-SE' : 'sv', 'pt-PT' : 'pt'}

def usage():
	print(__doc__)


def fetchLanguages(projectKey):
	try:
		languagesURL = ENDPOINT.format(projectID=PROJECT_ID, package="all", projectKey=projectKey)
		(filename, headers) = urllib.urlretrieve(languagesURL, FILENAME)
	except BaseException as e:
		return (None, e)
	else:
		return (filename, None)
	
	
def unzipFile(filename):
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
				pass
				shutil.rmtree(os.path.join(extractedDir, dir))
	except OSError as error:
		print(error.strerror)


def fetchLanguageStatus(projectKey):
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
		else:
			print(exception.strerror)
	