#!/usr/bin/python

"""
Usage:
	upload_translations.py <project-key> [-a|-u] 
	
	-a : Add files
	-u : Update files
	
	Either -a or -u should be specified. Defaults to -a.
"""

import requests, os, argparse, sys, json

PROJECT_ID = "bemyeyes"
MAX_FILE_LIST_LENGTH = 20
IGNORED_FILES = set(["InfoPlist.strings"])
UPDATE_FILE_URL = "https://api.crowdin.com/api/project/{projectID}/{addOrUpdate}-file?key={APIKey}"
PROJECT_INFO_URL = "https://api.crowdin.com/api/project/{projectID}/info?key={APIkey}&json"
PATH_TO_ENGLISH = "../BeMyEyes/Localization/en.lproj"

class Mode:
	add, update, addAndUpdate = range(0, 3)

def p(message):
	"""
	Used to print distinguishable messages.
	"""
	print("### {0} ###".format(message))


def uploadFiles(APIKey, mode, existingFiles):
	"""
	The heart of this script. This function looks for English translation files
	and uploads them to CrowdIn.
	
	APIKey - key giving access to the CrowdIn API
	mode - either 'a' (add files) or 'u' (update files)
	"""
	englishDir = pathToEnglishTranslation()
	fileSet = fileSetAt(englishDir, lambda x: x.endswith(".strings"))
	filesToUpdate, filesToAdd = classifyFiles(fileSet - IGNORED_FILES, existingFiles)
	
	print("Files to update: {0}".format(filesToUpdate))
	print("Files to add: {0}".format(filesToAdd))
	
	#Update files
	if mode != Mode.add:
		step1URL = uploadURL(PROJECT_ID, APIKey, Mode.update)
		step1Suc = upload(filesToUpdate, step1URL, englishDir)
	
	#Add files
	if mode != Mode.update:
		step2URL = uploadURL(PROJECT_ID, APIKey, Mode.add)
		step2Suc = upload(filesToAdd, step2URL, englishDir)
	
	return True

def classifyFiles(filesToUpload, existingFiles):
	filesToUpdate = []
	filesToAdd = []
	for file in filesToUpload:
		if file in existingFiles:
			filesToUpdate.append(file)
		else:
			filesToAdd.append(file)
	return filesToUpdate, filesToAdd


def upload(files, url, englishDir):
	filesToUpload = {}
	for file in files:
		location = os.path.join(englishDir, file)
		filesToUpload["files[{0}]".format(file)] = open(location, "r")
		if len(filesToUpload) == MAX_FILE_LIST_LENGTH:
			p("Uploading {0} files".format(len(filesToUpload)))
			if makeUploadRequest(filesToUpload, url):
				filesToUpload = {}
			else:
				return False
					
	if len(filesToUpload):
		p("Uploading {0} files".format(len(filesToUpload)))
		success = makeUploadRequest(filesToUpload, url)
		if success:
			p("Upload successful")
		else:
			return False

def makeUploadRequest(filesToUpload, url):
	"""
	Function opening a connection to the CrowdIn server and uploading files.
	"""
	response = requests.post(url, files=filesToUpload)
	if response.status_code != 200:
		print("Upload unsuccessful! Status code {0}. Response: {1}".format(response.status_code, response.text))
		return False
	else:
		return True
		
		
def pathToEnglishTranslation():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    return os.path.join(dname, PATH_TO_ENGLISH)
	
	
def fileSetAt(directory, condition):
	"""
	Return a list of all elements in a given directory that 
	fulfill the supplied condition.
	"""
	dirsList = [name for name in os.listdir(directory)
			            if condition(name)]
	return set(dirsList)


def uploadURL(projID, key, mode):
	"""
	We need a different URL depending on whether the user wants to add files or upload them.
	"""
	if mode == Mode.add:
		return UPDATE_FILE_URL.format(projectID=projID, APIKey=key, addOrUpdate="add")
	elif mode == Mode.update:
		return UPDATE_FILE_URL.format(projectID=projID, APIKey=key, addOrUpdate="update")
	else:
		return ''
	
def projectInfoURL(projID, key):
	return PROJECT_INFO_URL.format(projectID=projID, APIkey=key)	

def modeFromArguments(add, update):
	both = add and update
	neither = not add and not update
	if both or neither:
		return Mode.addAndUpdate
	elif add:
		return Mode.add
	else:
		return Mode.update
		
		
def fetchExistingFilenames(projID, APIKey):
	"""
	Method fetching info about the project and extracting
	names of uploaded files.
	"""
	url = projectInfoURL(projID, APIKey)
	response = requests.get(url)
	parsedJSON = json.loads(response.text)
	files = parsedJSON["files"]
	existingNames = []
	for langDict in files:
		existingNames.append(langDict["name"])
	return set(existingNames)

###### Main ######

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("api_key", help="Key for accessing the CrowdIn API")
	parser.add_argument("-a", "--add", help="New files will be added", action="store_true")
	parser.add_argument("-u", "--update", help="Existing files will be updated", action="store_true")
	args = parser.parse_args()
	
	mode = modeFromArguments(args.add, args.update)
	existingFilenames = fetchExistingFilenames(PROJECT_ID, args.api_key)
	uploadFiles(args.api_key, mode, existingFilenames)
	