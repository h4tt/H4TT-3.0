# EC 2: An Interesting Memo

## Description

```
{
    "title": "EC 2: An Interesting Memo",
    "category": "evilcorp",
    "description": "Looks like the Evil Corp mole has given us an encrypted file, see if you can't decrypt it.",
    "hint": "Ever built a dictionary?",
    "link": "https://evilcorp.h4tt.ca",
    "points": "40",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "required": "EC 1: Welcome to Evil Corp",
    "author": "Francisco Trindade"
}
```

## Solution

<details><summary>Click me</summary>Downloading the file linked in the solution of the previous challenge "Welcome to Evil Corp". The file is an encrypted zip file.

The solution is to either use `crunch` or another script to generate every possibly permutation of 5 lower case alphanumeric characters and pre-pending them all with the 5 characters shown in the note. Then run a dictionary attack either using John or pcrackzip against the zip file.
The password reveals itself to be: b2vk1di2ie

Flag: flag{c4p741n_crunch}
</details>