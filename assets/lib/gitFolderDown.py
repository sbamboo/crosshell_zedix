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


def gitFolderDownRecurse(url=str(),resultDir=str(),debug=False,Authorization=None):
    if Authorization != None:
        headers = {'Authorization': Authorization}
    # Recursive search
    spliturl = url.split("/")
    spliturl.pop(-1)
    baseurl = ('/'.join(spliturl)).strip('/')
    # Send requests to baseurl
    if Authorization != None: responsejson = requests.get(url=baseurl,headers=headers).json()
    else: responsejson = requests.get(url=baseurl).json()
    if debug == "raw": print("[Raw.BaseURLreq]: ",responsejson,"\n\n","[Raw.BaseUrl]: ",baseurl,"\n\n")
    match = False
    for obj in responsejson:
        selflink = obj["_links"]["self"]
        if selflink.split("?")[0] == url:
            match = obj["git_url"]
    # Request recusive tree
    if match != False:
        if Authorization != None: responsejson = requests.get(url=f"{match}?recursive=1",headers=headers).json()
        else: responsejson = requests.get(url=f"{match}?recursive=1").json()
        if debug == "raw": print("[Raw.TreeURLreq]: ",responsejson,"\n\n","[Raw.TreeUrl]: ",f"{match}?recursive=1","\n\n")
        # Download files
        for obj in responsejson["tree"]:
            # Filter files
            if obj["type"] == "blob":
                blob_url = obj["url"]
                obj_path = obj["path"]
                # Send requests for content
                if Authorization != None: responsejson2 = requests.get(url=blob_url,headers=headers).json()
                else: responsejson2 = requests.get(url=blob_url).json()
                if debug == "raw": print("[Raw.BlobURLreq]: ",responsejson2,"\n\n","[Raw.BlobUrl]: ",blob_url,"\n\n")
                content = responsejson2["content"]
                encoding = responsejson2["encoding"]
                if encoding == "base64":
                    # Import format
                    import base64
                    # Decode content
                    decoded_content = base64.b64decode(content)
                    # Write the decoded content to the destination file
                    obj_path = obj_path.replace("/",os.sep)
                    # Create missing subfolders
                    if str(os.sep) in str(obj_path):
                        splitDir = obj_path.split(os.sep)
                        splitDir.pop(-1)
                        # Save old dir
                        olddir = os.getcwd()
                        # Go to destination dir
                        os.chdir(resultDir)
                        # Create folders
                        for folder in splitDir:
                            if not os.path.exists(folder): os.mkdir(folder)
                            os.chdir(folder)
                        # Go back to old dir
                        os.chdir(olddir)
                    # Write files
                    destinationpath = f"{resultDir}{os.sep}{obj_path}"
                    with open(destinationpath, "wb") as f:
                        f.write(decoded_content)
                if debug != False: print("[FileData]: ",encoding,content)