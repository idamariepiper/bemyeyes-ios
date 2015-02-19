#!/usr/bin/python

import requests, argparse, json

EXPORT_URL = "https://api.crowdin.com/api/project/{projectID}/export?key={APIkey}&json"
PROJECT_ID = "bemyeyes"

def exportTranslations(APIKey):
	url = exportURL(APIKey)
	response = requests.get(url)
	if response.status_code != 200:
		print("Exporting translations failed. Status code: {0}. Response: {1}".format(response.status_code, response.text))
	else:
		parsed = json.loads(response.text)
		status = parsed["success"]["status"]
		if status == "skipped":
			print("Status: {0}. You can only export every 30 minutes.".format(status))
		else:
			print("Status: {0}. Export was successful.".format(status))
	
def exportURL(key):
	return EXPORT_URL.format(projectID=PROJECT_ID, APIkey=key)

#### Main ####

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("api_key", help="Key for accessing the CrowdIn API")
	args = parser.parse_args()
	
	exportTranslations(args.api_key)