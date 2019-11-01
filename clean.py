import os
import json

H4TT_VERSION = "3.0"

jsons = []
output = "![sreencast](poster.jpg)\n\n# Hack All The Things Round %s\n" % H4TT_VERSION

def CleanFolders():
    filenames = os.listdir (".")
    blacklistFolders = [
        ".git",
        "[template]"
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
    for item in categories:
        listCat.append(item)

    listCat.sort()
    for thisCat in listCat:
        output += "## " + thisCat + "\n"

        listChallPoints = []
        for item in categories[thisCat]:
            thisChall = categories[thisCat][item]
            listChallPoints.append([int(thisChall['points']), thisChall['title']])
        
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
    return output

if __name__ == "__main__":
    CleanFolders()
    categories = ScrapeJSON(output)
    output = BuildReadme(categories, output)

    text_file = open("README.md", "w")
    text_file.write(output)
    text_file.close()
