import os
import json
import hashlib
import shutil

H4TT_VERSION = "3.0"

jsons = []
output = f"![sreencast](poster.jpg)\n\n# Hack All The Things Round {H4TT_VERSION}\n"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def CleanFolders():
    filenames = os.listdir (".")
    blacklistFolders = [
        ".git",
        "[template]"
        "CTFd-import"
    ]

    folders = []
    for filename in filenames:
        if os.path.isdir(os.path.join(os.path.abspath("."), filename)):
            folders.append(filename)

    for folder in folders:
        if folder in blacklistFolders:
            continue

        subFilenames = os.listdir(folder)
        subFolders = []
        for filename in subFilenames:
            if os.path.isdir(os.path.join(os.path.abspath(folder), filename)):
                subFolders.append(filename)

        for subFolder in subFolders:
            newName = subFolder

            newName = newName.lower()
            newName = newName.replace(" ", "_")
            newName = newName.replace("-", "_")

            os.rename(os.path.join(folder, subFolder), os.path.join(folder, newName))

def ScrapeJSON(output):
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".json"):
                if root.split(os.sep)[1] != "[template]":
                    jsons.append(os.path.join(root, file))

    categories = {}

    for file in jsons:
        # Skip non-challenge JSON files
        if not file.lower().endswith("challenge.json"):
            continue

        with open(file) as thisJsonFile:
            data = json.load(thisJsonFile)
            thisCat = data['category'].lower()

            if thisCat not in categories:
                categories[thisCat] = {}

            data['INTERNAL_PATH'] = file
            categories[thisCat][data['title']] = data

    return categories

def BuildReadme(categories, output):
    listCat = []
    totalPoints = 0

    for item in categories:
        listCat.append(item)

    listCat.sort()
    for thisCat in listCat:
        output += "## " + thisCat + "\n"

        listChallPoints = []
        for item in categories[thisCat]:
            thisChall = categories[thisCat][item]
            listChallPoints.append([int(thisChall['points']), thisChall['title']])

            totalPoints += int(thisChall['points'])
        
        listChallPoints.sort()
        
        for challenge in listChallPoints:
            thisChall = categories[thisCat][challenge[1]]
            output += "[%s | %s](https://github.com/h4tt/H4TT-%s/tree/master/%s/%s)\n\n" % (
                thisChall['title'],
                thisChall['points'],
                H4TT_VERSION,
                thisCat,
                thisChall['INTERNAL_PATH'].split(os.sep)[2]
            )

    print(totalPoints)
    return output

# Build all of the JSON files for CTFd to import
def BuildCTFd(categories):
    if os.path.exists("CTFd-import/"):
        shutil.rmtree("CTFd-import/")

    challengeDict = {}
    challengeDict['results'] = []

    flagDict = {}
    flagDict['results'] = []
    flagCount = 1

    fileDict = {}
    fileDict['results'] = []
    fileCount = 1

    idCount = 1
    idList = {}
    for category in categories:
        for challengeName in categories[category]:
            challenge = categories[category][challengeName]
            idList[challenge['title']] = [idCount, challenge]
            idCount += 1

    for idElement in idList.values():
        id = idElement[0]
        challenge = idElement[1]

        thisChallenge = {}
        challengeDict['results'].append(thisChallenge)

        thisChallenge['id'] = id
        thisChallenge['name'] = challenge['title']
        thisChallenge['description'] = challenge['description'].replace('\n', '<br>') + "<br><br>Author: " + challenge['author']
        thisChallenge['max_attempts'] = int(challenge['max_tries'])
        thisChallenge['value'] = int(challenge['points'])
        thisChallenge['category'] = challenge['category']
        thisChallenge['type'] = "standard"
        thisChallenge['state'] = "visible"

        if 'required' in challenge and challenge['required'] != '':
            thisChallenge['requirements'] = {}
            thisChallenge['requirements']['prerequisites'] = [idList[challenge['required']][0]]
        else:
            thisChallenge['requirements'] = None

        thisFlag = {}
        flagDict['results'].append(thisFlag)

        thisFlag['id'] = flagCount
        flagCount += 1

        thisFlag['challenge_id'] = id
        thisFlag['type'] = "static"
        thisFlag['content'] = challenge['flag']
        thisFlag['data'] = "case_insensitive"

        for fileName in challenge['files']:
            if fileName == '':
                continue

            internalPath = challenge['INTERNAL_PATH'].rsplit("/", 1)[0] + "/" + fileName

            fileMD5 = md5(internalPath)

            if os.path.exists("CTFd-import/uploads/" + fileMD5):
                shutil.rmtree("CTFd-import/uploads/" + fileMD5)

            os.makedirs("CTFd-import/uploads/" + fileMD5)

            shutil.copyfile(internalPath, "CTFd-import/uploads/" + fileMD5 + "/" + fileName)

            thisFile = {}
            fileDict['results'].append(thisFile)

            thisFile['id'] = fileCount
            fileCount += 1

            thisFile['type'] = "challenge"
            thisFile['location'] = fileMD5 + "/" + fileName.split('/')[-1]
            thisFile['challenge_id'] = id
            thisFile['page_id'] = None


    challengeDict['count'] = len(challengeDict['results'])
    challengeDict['meta'] = {}

    flagDict['count'] = len(flagDict['results'])
    flagDict['meta'] = {}

    fileDict['count'] = len(fileDict['results'])
    fileDict['meta'] = {}

    if not os.path.exists("CTFd-import"):
        os.makedirs("CTFd-import")

    with open('CTFd-import/challenges.json', 'w') as outfile:
        json.dump(challengeDict, outfile)

    with open('CTFd-import/flags.json', 'w') as outfile:
        json.dump(flagDict, outfile)

    with open('CTFd-import/files.json', 'w') as outfile:
        json.dump(fileDict, outfile)


if __name__ == "__main__":
    CleanFolders()
    categories = ScrapeJSON(output)
    output = BuildReadme(categories, output)
    BuildCTFd(categories)

    text_file = open("README.md", "w")
    text_file.write(output)
    text_file.close()
