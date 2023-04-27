# 'Military Grade' Encryption

## Description

```
{
    "title": "'Military Grade' Encryption",
    "category": "rev",
    "description": "I lost my flag! Can you help me find it?",
    "link": "",
    "points": "100",
    "max_tries": "99",
    "active": "0",
    "files": [
        "readme.txt",
        "military_encryption"
    ],
    "author": "Sean Maher"
}
```

## Solution

<details><summary>Click me</summary>So in this challenge, I decided to write a scrambler in C (source code provided here, feel free to comment on it, 
if I made any mistakes in the writing of it, I'd love to know) which scrambles up the bits given, then encodes the 
scrambled input in base64, then outputs it on the command line. I'm providing the scrambler, and the end text. 
It's the job of the reverser to go back and remake the string from the scrambled text. I wrote a simple 
python script to do this, included in this solution folder as well. 

flag{0b5cur1ty_1s_n0t_3ncrypt10n}

</details>