# EC 5: What Bash?

## Description

```
{
    "title": "EC 5: What Bash?",
    "category": "evilcorp",
    "description": "We need to see what's in /tmp. Try and gain access to those files.",
    "hint": "PATH is a cool variable",
    "link": "https://evilcorp.h4tt.ca",
    "points": "70",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "required": "EC 4: Up and Down We Go",
    "author": "Francisco Trindade"
}
```

## Solution

<details><summary>Click me</summary>When entering the bash shell users have entered a restricted bash shell, with only access to vi, echo. The hint given in the motd is to attempt to point at using the program vi as a way out.

Enter vi. Then press: ESC and type ":!/bin/bash" will return a bash shell. Then change the path variable to gain access to other programs.

`export PATH=/bin:/usr/bin`

Navigate to /tmp and cat out the only file found there and the flag will be in it.

Flag: flag{rb45h_c4n7_570p_m3}
</details>