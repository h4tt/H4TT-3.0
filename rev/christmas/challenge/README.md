# Christmas

## Description

```
{
    "title": "Christmas",
    "category": "rev",
    "description": "Can you hear the elves sending out packages?",
    "link": "",
    "points": "40",
    "max_tries": "99",
    "active": "0",
    "files": [
        "challenge.exe"
    ],
    "author": "Sean Maher"
}
```

## Solution

<details><summary>Click me</summary>This challenge doesn't have much to it. I've packed the executable using UPX packing,
and a surprising small amount of people don't know much about process packing, much less
how to circumvent it. 

You can unpack this executable manually by running it in a debugger, finding the original 
entry point, then dumping it, or simply using the UPX application provided at upx.github.io.
Afterwards, you'll see a simple stack string which you can see by observing the code in a debugger
(or setting a breakpoint after the stack string is set)

flag{p4ck1ng_1s_n0t_crypt0}

</details>