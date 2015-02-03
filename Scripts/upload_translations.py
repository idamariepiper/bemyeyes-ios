#!/usr/bin/python

"""
Usage:
	upload_translations.py -p <project-key> [-a|-u] 
	
	-a : Add files
	-u : Update files
	
	Either -a or -u should be specified. Defaults to -a.
"""

import requests, os, getopt, sys

# Testing
PROJECT_ID = "bemyeyes-test-project"

####### Production
#PROJECT_ID = "bemyeyes"
MAX_FILE_LIST_LENGTH = 20
IGNORED_FILES = ["InfoPlist.strings"]
UPDATE_FILE_URL = "https://api.crowdin.com/api/project/{projectID}/{addOrUpdate}-file?key={APIKey}"
PATH_TO_ENGLISH = "../BeMyEyes/Localization/en.lproj"

def usage():
	print(__doc__)


def p(message):
	"""
	Used to print distinguishable messages.
	"""
	print("### {0} ###".format(message))


def uploadFiles(APIKey, mode):
	"""
	The heart of this script. This function looks for English translation files
	and uploads them to CrowdIn.
	
	APIKey - key giving access to the CrowdIn API
	mode - either 'a' (add files) or 'u' (update files)
	"""
	englishDir = pathToEnglishTranslation()
	fileList = fileListAt(englishDir, lambda x: x.endswith(".strings"))
	
	filesToUpload = {}
	
	p("Preparing for upload")
	
	for file in fileList:
		location = os.path.join(englishDir, file)
		filesToUpload["files[{0}]".format(file)] = open(location, "r")
		if len(filesToUpload) == MAX_FILE_LIST_LENGTH:
			p("Uploading {0} files".format(len(filesToUpload)))
			if makeUploadRequest(filesToUpload, APIKey, mode):
				filesToUpload = {}
			else:
				return False
				
	if len(filesToUpload):
		p("Uploading {0} files".format(len(filesToUpload)))
		success = makeUploadRequest(filesToUpload, APIKey, mode)
		if success:
			p("Upload successful")
		else:
			return False
	
	return True


def makeUploadRequest(filesToUpload, APIKey, mode):
	"""
	Function opening a connection to the CrowdIn server and uploading files.
	"""
	url = uploadURL(PROJECT_ID, APIKey, mode)
	response = requests.post(url, files=filesToUpload)
	if response.status_code != 200:
		print("Upload unsuccessful! Status code {0}. Response: {1}".format(response.status_code, response.text))
		return False
	else:
		return True
		
		
def pathToEnglishTranslation():
	return os.path.join(os.getcwd(), PATH_TO_ENGLISH)
	
	
def fileListAt(directory, condition):
	"""
	Return a list of all elements in a given directory that 
	fulfill the supplied condition.
	"""
	dirsList = [name for name in os.listdir(directory)
			            if condition(name)]
	return dirsList


def uploadURL(projID, key, mode):
	"""
	We need a different URL depending on whether the user wants to add files or upload them.
	"""
	if mode == 'a':
		return UPDATE_FILE_URL.format(projectID=projID, APIKey=key, addOrUpdate="add")
	elif mode == 'u':
		return UPDATE_FILE_URL.format(projectID=projID, APIKey=key, addOrUpdate="update")
	else:
		return ''
	

###### Main ######

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "p:ua")
		if len(opts) != 2:
			usage()
			sys.exit(2)
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	else:
		projectKey = ''
		mode = 'a'
		for opt, arg in opts:
			if opt == "-p":
				projectKey = arg
			elif opt == "-u":
				mode = 'u'
			elif opt == "-a":
				pass
			else:
				usage()
				sys.exit(2)
		
	uploadFiles(projectKey, mode)
	