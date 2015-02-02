#!/usr/bin/python

"""
Usage:
	upload_translations.py -p <project-key>
"""

import requests, os, getopt, sys
from poster.encode import multipart_encode

# Testing
PROJECT_ID = "bemyeyes-test-project"

####### Production
#PROJECT_ID = "bemyeyes"

UPDATE_FILE_URL = "https://api.crowdin.com/api/project/{projectID}/add-file?key={APIKey}"
PATH_TO_ENGLISH = "../BeMyEyes/Localization/en.lproj"

def usage():
	print(__doc__)

def p(message):
	print("### {0} ###".format(message))

def uploadFiles(APIKey):
	englishDir = pathToEnglishTranslation()
	fileList = fileListAt(englishDir, lambda x: x.endswith(".strings"))
	
	maxFiles = 20
	filesToUpload = {}
	
	p("Preparing for upload")
	
	for file in fileList:
		location = os.path.join(englishDir, file)
		filesToUpload["files[{0}]".format(file)] = open(location, "r")
		if len(filesToUpload) == maxFiles:
			p("Uploading {0} files".format(len(filesToUpload)))
			if not makeUploadRequest(filesToUpload, APIKey):
				print("Upload unsuccessful! Status code {0}. Response: {1}".format(response.status_code, response.text))
				return False
			else:
				filesToUpload = {}
				
	if len(filesToUpload):
		p("Uploading {0} files".format(len(filesToUpload)))
		success = makeUploadRequest(filesToUpload, APIKey)
		if not success:
			print("Upload unsuccessful! Status code {0}. Response: {1}".format(response.status_code, response.text))
		else:
			p("Upload successful")
	
	return True

def makeUploadRequest(filesToUpload, APIKey):
	response = requests.post(uploadURL(PROJECT_ID, APIKey), files=filesToUpload)
	if response.status_code != 200:
		print("Upload unsuccessful! Status code {0}. Response: {1}".format(response.status_code, response.text))
		return False
	else:
		return True
		
def pathToEnglishTranslation():
	return os.path.join(os.getcwd(), PATH_TO_ENGLISH)
	
def fileListAt(directory, condition):
	dirsList = [name for name in os.listdir(directory)
			            if condition(name)]
	return dirsList

def uploadURL(projID, key):
	return UPDATE_FILE_URL.format(projectID=projID, APIKey=key)

###### Main ######

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
		
	uploadFiles(projectKey)
	