# Nickleback

## Description

```
{
    "title": "Nickleback",
    "category": "forensics",
    "description": "We found this Nickleback album on a disgruntled employee's computer. Are they hiding anything?",
    "link": "",
    "points": "35",
    "max_tries": "99",
    "active": "0",
    "files": [
        "challenge.zip"
    ],
    "author": "Dave Petrasovic"
}
```

## Solution

<details><summary>Click me</summary>Unzip the challenge.
Notice that 9/10 songs are 0 bytes
02 How you remind me.mp3 is the only file larger than 0 bytes
from cli, type: file 02\ How\ You\ Remind\ Me.mp3
it will tell you the file is a GIF
change the file extension to .gif

This actually happened where someone was hiding child exploitation videos
by renaming them to Nickleback mp3s on a work computer.

flag{l4m3_w4y_2_h1d3}
</details>