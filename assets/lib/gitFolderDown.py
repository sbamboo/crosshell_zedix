# [Imports]
import os
import requests

# Function to download a directory from a github repository
def gitFolderDown(url=str(),resultDir=str()):
    # Replace GITHUB_USERNAME with the username of the GitHub account
    # Replace REPOSITORY_NAME with the name of the repository
    # Replace DIRECTORY_NAME with the name of the directory you want to download
    # url = f"https://api.github.com/repos/GITHUB_USERNAME/REPOSITORY_NAME/contents/DIRECTORY_NAME"

    # Make a GET request to the GitHub API to get the contents of the directory
    response = requests.get(url)

    # The response will be a JSON object containing a list of the files in the directory
    files = response.json()
    # Iterate over the list of files and download each one
    for file in files:
        file_url = file["download_url"]
        file_response = requests.get(file_url)

        # Write the contents of the file to a local file
        name = file["name"]
        path = f"{resultDir}{os.sep}{name}"
        with open(path, "wb") as f:
            f.write(file_response.content)