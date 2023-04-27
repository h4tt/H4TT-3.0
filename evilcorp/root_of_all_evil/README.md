# EC 6: Root of all Evil

## Description

```
{
    "title": "EC 6: Root of all Evil",
    "category": "evilcorp",
    "description": "The mole seems to have given us a way to get the last bit of info in /root. See if you can't get access to it.",
    "hint": "man sudo",
    "link": "https://evilcorp.h4tt.ca",
    "points": "100",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "required": "EC 5: What Bash?",
    "author": "Francisco Trindade"
}
```

## Solution

<details><summary>Click me</summary>Assuming you have a proper unrestricted bash shell. Typing `sudo -l` will reveal that the user can run `hexdump` as sudo without a password. Running `hexdump -C /root/flag.txt` (or a potential variation) will print out he final message and flag.

Flag: flag{5ud0_15_p0w3rful}
</details>