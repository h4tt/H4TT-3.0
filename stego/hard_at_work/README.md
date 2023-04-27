# Hard At Work

## Description

```
{
    "title": "Hard At Work",
    "category": "stego",
    "description": "We've recieved an image of two evilcorp members in a video call. Take a look for any hidden messages",
    "link": "",
    "points": "35",
    "max_tries": "99",
    "active": "0",
    "files": [
        "challenge.jpg"
    ],
    "author": "Matt Langois"
}
```

## Solution

<details><summary>Click me</summary>There is a second image appended to the first. You can see it with binwalk. If you run `binwalk --dd=".*" challenge.jpg` you can extract all of the files.

flag{well_hello_there}</details>