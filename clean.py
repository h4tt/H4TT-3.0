import os
import json
import hashlib
import shutil
import base64
import zipfile

H4TT_VERSION = "3.0"

jsons = []
output = f"![sreencast](poster.jpg)\n\n# Hack All The Things Round {H4TT_VERSION}\n"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

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

            # Make a deep copy of data
            thisChallenge = {}
            for key in data:
                thisChallenge[key] = data[key]

            # Remove the flag and INTERNAL_PATH from the challenge
            thisChallenge.pop('flag', None)
            thisChallenge.pop('INTERNAL_PATH', None)

            # Write a README.md file for each challenge. It should be placed in
            # the directory above the file, and should put thisJsonFile in code
            # blocks
            readme = "# " + thisChallenge['title'] + "\n\n"
            readme += "## Description\n\n"
            readme += "```\n"
            readme += json.dumps(thisChallenge, indent=4)
            readme += "\n```"

            # Next, open the solution file and add it to the README.md. It's
            # located up one directory, and then in a directory called
            # "solution". Make sure that the solution is in a hidden block.
            solutionFile = os.path.join(os.path.dirname(file), "../", "solution", "solution.txt")
            if os.path.exists(solutionFile):
                with open(solutionFile) as solution:
                    readme += "\n\n## Solution\n\n"
                    readme += "<details><summary>Click me</summary>"
                    readme += solution.read()
                    readme += "</details>"

            with open(os.path.join(os.path.dirname(file), "../", "README.md"), "w") as readmeFile:
                readmeFile.write(readme)

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
            output += "### [%s | %s](https://github.com/h4tt/H4TT-%s/tree/master/%s/%s)\n" % (
                thisChall['title'],
                thisChall['points'],
                H4TT_VERSION,
                thisCat,
                thisChall['INTERNAL_PATH'].split(os.sep)[2]
            )
            output += "*Author: %s*\n" % (
                thisChall['author'],
            )
            output += "> %s\n\n" % (
                thisChall['description'].replace('\n', '\n> '),
            )

    print(str(totalPoints) + " points total")
    return output

# Build all of the JSON files for CTFd to import
def BuildCTFd(categories):
    print("Building CTFd import file...")
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

        description = challenge['description'].replace('\n', '<br>') + "<br><br>Author: " + challenge['author']
        if challenge['link'] != "":
            description += '<br><br><a href="' + challenge['link'] + '">' + challenge['link'] + '</a>'

        thisChallenge['description'] = description
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

    print("Creating files...")
    if not os.path.exists("CTFd-import/db"):
        os.makedirs("CTFd-import/db")

    with open('CTFd-import/db/challenges.json', 'w') as outfile:
        json.dump(challengeDict, outfile)

    with open('CTFd-import/db/flags.json', 'w') as outfile:
        json.dump(flagDict, outfile)

    # File upload isn't working so it will have to be done manually
    # with open('CTFd-import/db/files.json', 'w') as outfile:
    #     json.dump(fileDict, outfile)
    open('CTFd-import/db/files.json', 'a').close()
    if os.path.exists("CTFd-import/uploads"):
        shutil.rmtree("CTFd-import/uploads")

    with open('CTFd-import/db/alembic_version.json', 'w') as outfile:
        outfile.write(str(base64.b64decode('''eyJjb3VudCI6IDEsICJyZXN1bHRzIjogW3sidmVyc2lvbl9udW0iOiAiYjI5NWIwMzMzNjRkIn1dLCAibWV0YSI6IHt9fQ==''').decode('utf-8')))

    open('CTFd-import/db/awards.json', 'a').close()

    with open('CTFd-import/db/config.json', 'w') as outfile:
        outfile.write(str(base64.b64decode('''ewogICAgImNvdW50IjogMzgsCiAgICAicmVzdWx0cyI6IFsKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDEsCiAgICAgICAgICAgICJrZXkiOiAiY3RmX3ZlcnNpb24iLAogICAgICAgICAgICAidmFsdWUiOiAiMi4xLjUiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDIsCiAgICAgICAgICAgICJrZXkiOiAiY3RmX3RoZW1lIiwKICAgICAgICAgICAgInZhbHVlIjogInN0b3JtY3RmIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAzLAogICAgICAgICAgICAia2V5IjogImN0Zl9uYW1lIiwKICAgICAgICAgICAgInZhbHVlIjogIkhhY2sgQWxsIFRoZSBUaGluZ3MgMy4wIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiA0LAogICAgICAgICAgICAia2V5IjogInN0YXJ0IiwKICAgICAgICAgICAgInZhbHVlIjogIjE1NzMzMTE2MDAiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDUsCiAgICAgICAgICAgICJrZXkiOiAidXNlcl9tb2RlIiwKICAgICAgICAgICAgInZhbHVlIjogInRlYW1zIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiA2LAogICAgICAgICAgICAia2V5IjogImNoYWxsZW5nZV92aXNpYmlsaXR5IiwKICAgICAgICAgICAgInZhbHVlIjogImFkbWlucyIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogNywKICAgICAgICAgICAgImtleSI6ICJyZWdpc3RyYXRpb25fdmlzaWJpbGl0eSIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICJwdWJsaWMiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDgsCiAgICAgICAgICAgICJrZXkiOiAic2NvcmVfdmlzaWJpbGl0eSIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICJwdWJsaWMiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDksCiAgICAgICAgICAgICJrZXkiOiAiYWNjb3VudF92aXNpYmlsaXR5IiwKICAgICAgICAgICAgInZhbHVlIjogInB1YmxpYyIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMTAsCiAgICAgICAgICAgICJrZXkiOiAiZW5kIiwKICAgICAgICAgICAgInZhbHVlIjogIjE1NzMzNDA0MDAiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDExLAogICAgICAgICAgICAia2V5IjogImZyZWV6ZSIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDEyLAogICAgICAgICAgICAia2V5IjogInZlcmlmeV9lbWFpbHMiLAogICAgICAgICAgICAidmFsdWUiOiBudWxsCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDEzLAogICAgICAgICAgICAia2V5IjogIm1haWxfc2VydmVyIiwKICAgICAgICAgICAgInZhbHVlIjogbnVsbAogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAxNCwKICAgICAgICAgICAgImtleSI6ICJtYWlsX3BvcnQiLAogICAgICAgICAgICAidmFsdWUiOiBudWxsCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDE1LAogICAgICAgICAgICAia2V5IjogIm1haWxfdGxzIiwKICAgICAgICAgICAgInZhbHVlIjogbnVsbAogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAxNiwKICAgICAgICAgICAgImtleSI6ICJtYWlsX3NzbCIsCiAgICAgICAgICAgICJ2YWx1ZSI6IG51bGwKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMTcsCiAgICAgICAgICAgICJrZXkiOiAibWFpbF91c2VybmFtZSIsCiAgICAgICAgICAgICJ2YWx1ZSI6IG51bGwKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMTgsCiAgICAgICAgICAgICJrZXkiOiAibWFpbF9wYXNzd29yZCIsCiAgICAgICAgICAgICJ2YWx1ZSI6IG51bGwKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMTksCiAgICAgICAgICAgICJrZXkiOiAibWFpbF91c2VhdXRoIiwKICAgICAgICAgICAgInZhbHVlIjogbnVsbAogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyMCwKICAgICAgICAgICAgImtleSI6ICJzZXR1cCIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIxIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyMSwKICAgICAgICAgICAgImtleSI6ICJjc3MiLAogICAgICAgICAgICAidmFsdWUiOiAiIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyMiwKICAgICAgICAgICAgImtleSI6ICJmcmVlemUtbW9udGgiLAogICAgICAgICAgICAidmFsdWUiOiAiIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyMywKICAgICAgICAgICAgImtleSI6ICJ2aWV3X2FmdGVyX2N0ZiIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIwIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyNCwKICAgICAgICAgICAgImtleSI6ICJzdGFydC1taW51dGUiLAogICAgICAgICAgICAidmFsdWUiOiAiMCIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMjUsCiAgICAgICAgICAgICJrZXkiOiAiZW5kLWRheSIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICI5IgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyNiwKICAgICAgICAgICAgImtleSI6ICJzdGFydC15ZWFyIiwKICAgICAgICAgICAgInZhbHVlIjogIjIwMTkiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDI3LAogICAgICAgICAgICAia2V5IjogImVuZC1taW51dGUiLAogICAgICAgICAgICAidmFsdWUiOiAiMCIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMjgsCiAgICAgICAgICAgICJrZXkiOiAiZnJlZXplLWhvdXIiLAogICAgICAgICAgICAidmFsdWUiOiAiIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAyOSwKICAgICAgICAgICAgImtleSI6ICJmcmVlemUteWVhciIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDMwLAogICAgICAgICAgICAia2V5IjogImZyZWV6ZS1taW51dGUiLAogICAgICAgICAgICAidmFsdWUiOiAiIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAzMSwKICAgICAgICAgICAgImtleSI6ICJlbmQtaG91ciIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIxOCIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMzIsCiAgICAgICAgICAgICJrZXkiOiAiZW5kLXllYXIiLAogICAgICAgICAgICAidmFsdWUiOiAiMjAxOSIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMzMsCiAgICAgICAgICAgICJrZXkiOiAic3RhcnQtaG91ciIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIxMCIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMzQsCiAgICAgICAgICAgICJrZXkiOiAic3RhcnQtbW9udGgiLAogICAgICAgICAgICAidmFsdWUiOiAiMTEiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDM1LAogICAgICAgICAgICAia2V5IjogImVuZC1tb250aCIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICIxMSIKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICAgImlkIjogMzYsCiAgICAgICAgICAgICJrZXkiOiAic3RhcnQtZGF5IiwKICAgICAgICAgICAgInZhbHVlIjogIjkiCiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IDM3LAogICAgICAgICAgICAia2V5IjogImZyZWV6ZS1kYXkiLAogICAgICAgICAgICAidmFsdWUiOiAiIgogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiAzOCwKICAgICAgICAgICAgImtleSI6ICJwYXVzZWQiLAogICAgICAgICAgICAidmFsdWUiOiAiMCIKICAgICAgICB9CiAgICBdLAogICAgIm1ldGEiOiB7fQp9''').decode('utf-8')))

    open('CTFd-import/db/hints.json', 'a').close()
    open('CTFd-import/db/notifications.json', 'a').close()

    with open('CTFd-import/db/pages.json', 'w') as outfile:
        outfile.write(str(base64.b64decode('''eyJjb3VudCI6IDEsICJyZXN1bHRzIjogW3siaWQiOiAxLCAidGl0bGUiOiBudWxsLCAicm91dGUiOiAiaW5kZXgiLCAiY29udGVudCI6ICI8ZGl2IGNsYXNzPVwicm93XCI+XG4gICAgPGRpdiBjbGFzcz1cImNvbC1tZC02IG9mZnNldC1tZC0zXCI+XG4gICAgICAgIDxpbWcgY2xhc3M9XCJ3LTEwMCBteC1hdXRvIGQtYmxvY2tcIiBzdHlsZT1cIm1heC13aWR0aDogNTAwcHg7cGFkZGluZzogNTBweDtwYWRkaW5nLXRvcDogMTR2aDtcIiBzcmM9XCJ0aGVtZXMvY29yZS9zdGF0aWMvaW1nL2xvZ28ucG5nXCIgLz5cbiAgICAgICAgPGgzIGNsYXNzPVwidGV4dC1jZW50ZXJcIj5cbiAgICAgICAgICAgIDxwPkEgY29vbCBDVEYgcGxhdGZvcm0gZnJvbSA8YSBocmVmPVwiaHR0cHM6Ly9jdGZkLmlvXCI+Y3RmZC5pbzwvYT48L3A+XG4gICAgICAgICAgICA8cD5Gb2xsb3cgdXMgb24gc29jaWFsIG1lZGlhOjwvcD5cbiAgICAgICAgICAgIDxhIGhyZWY9XCJodHRwczovL3R3aXR0ZXIuY29tL2N0ZmRpb1wiPjxpIGNsYXNzPVwiZmFiIGZhLXR3aXR0ZXIgZmEtMnhcIiBhcmlhLWhpZGRlbj1cInRydWVcIj48L2k+PC9hPiZuYnNwO1xuICAgICAgICAgICAgPGEgaHJlZj1cImh0dHBzOi8vZmFjZWJvb2suY29tL2N0ZmRpb1wiPjxpIGNsYXNzPVwiZmFiIGZhLWZhY2Vib29rIGZhLTJ4XCIgYXJpYS1oaWRkZW49XCJ0cnVlXCI+PC9pPjwvYT4mbmJzcDtcbiAgICAgICAgICAgIDxhIGhyZWY9XCJodHRwczovL2dpdGh1Yi5jb20vY3RmZFwiPjxpIGNsYXNzPVwiZmFiIGZhLWdpdGh1YiBmYS0yeFwiIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPjwvaT48L2E+XG4gICAgICAgIDwvaDM+XG4gICAgICAgIDxicj5cbiAgICAgICAgPGg0IGNsYXNzPVwidGV4dC1jZW50ZXJcIj5cbiAgICAgICAgICAgIDxhIGhyZWY9XCJhZG1pblwiPkNsaWNrIGhlcmU8L2E+IHRvIGxvZ2luIGFuZCBzZXR1cCB5b3VyIENURlxuICAgICAgICA8L2g0PlxuICAgIDwvZGl2PlxuPC9kaXY+IiwgImRyYWZ0IjogMCwgImhpZGRlbiI6IG51bGwsICJhdXRoX3JlcXVpcmVkIjogbnVsbH1dLCAibWV0YSI6IHt9fQ==''').decode('utf-8')))
    
    
    open('CTFd-import/db/solves.json', 'a').close()
    open('CTFd-import/db/submissions.json', 'a').close()
    open('CTFd-import/db/tags.json', 'a').close()
    open('CTFd-import/db/teams.json', 'a').close()
    open('CTFd-import/db/tracking.json', 'a').close()
    open('CTFd-import/db/unlocks.json', 'a').close()

    with open('CTFd-import/db/users.json', 'w') as outfile:
        outfile.write(str(base64.b64decode('''eyJjb3VudCI6IDEsICJyZXN1bHRzIjogW3siaWQiOiAxLCAib2F1dGhfaWQiOiBudWxsLCAibmFtZSI6ICJhZG1pbiIsICJwYXNzd29yZCI6ICIkYmNyeXB0LXNoYTI1NiQyYiwxMiRzNjVPb29RZVBjNExkeGViYlFzTEcuJDA3b3pFVzdTRkNVM3RjN21VY3VBWWhjZ0JjN3FFNHUiLCAiZW1haWwiOiAiYWRtaW5AYWRtaW4uY2EiLCAidHlwZSI6ICJhZG1pbiIsICJzZWNyZXQiOiBudWxsLCAid2Vic2l0ZSI6IG51bGwsICJhZmZpbGlhdGlvbiI6IG51bGwsICJjb3VudHJ5IjogbnVsbCwgImJyYWNrZXQiOiBudWxsLCAiaGlkZGVuIjogMSwgImJhbm5lZCI6IDAsICJ2ZXJpZmllZCI6IDAsICJ0ZWFtX2lkIjogbnVsbCwgImNyZWF0ZWQiOiAiMjAxOS0xMS0wOFQyMDoxNzozNiJ9XSwgIm1ldGEiOiB7fX0=''').decode('utf-8')))

    print("Zipping...")

    bashCommand = "zip -r ctfd-import.zip db" # uploads"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), cwd="CTFd-import/", stdout=subprocess.PIPE)
    output, error = process.communicate()



if __name__ == "__main__":
    CleanFolders()
    categories = ScrapeJSON(output)
    # print(categories)
    output = BuildReadme(categories, output)
    BuildCTFd(categories)

    text_file = open("README.md", "w")
    text_file.write(output)
    text_file.close()
