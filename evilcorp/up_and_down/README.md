# EC 4: Up and Down We Go

## Description

```
{
    "title": "EC 4: Up and Down We Go",
    "category": "evilcorp",
    "description": "Looks like some file is readable that shouldn't be. Go find it.",
    "hint": "What file is similar to /etc/passwd",
    "link": "https://evilcorp.h4tt.ca",
    "points": "60",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "required": "EC 3: A Weak Login",
    "author": "Francisco Trindade"
}
```

## Solution

<details><summary>Click me</summary>When obtaining proper access to `/evilcorp/home?file=listing`, the `file` parameter is vulnerable to LFI. Injecting `file=../../etc/shadow` will reveal the backed up readable `/etc/shadow` file. Copying the hash for `evilcorp-user` and throwing it at John the Ripper using a Dictionary attack with the dictionary rockyou.txt. It will eventually reveal to be an MD5 hash that decodes to `1nokungfu`.

Then sshing into evilcorp-user@evilcorp.h4tt.ca using the password the terminal will print out the motd with the flag in it.

Flag: flag{f0ll0w_7h3_r4bb17_n30}
</details>