# Mips Is Awesome!

## Description

```
{
    "title": "Mips Is Awesome!",
    "category": "rev",
    "description": "Who needs x86 when you have MIPS?",
    "link": "",
    "points": "20",
    "max_tries": "99",
    "active": "0",
    "files": [
        "mips_is_awesome"
    ],
    "author": "Matt Langois"
}
```

## Solution

<details><summary>Click me</summary>We know the binary is in another architecture. However we can do some analysis on the binary without needing to run it.

If we run `strings` here (or open it in something like IDA) we'll see the flag.

flag{unkn0wn_pl4tf0rm}</details>