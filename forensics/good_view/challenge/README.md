# A Good View

## Description

```
{
    "title": "A Good View",
    "category": "forensics",
    "description": "What a sublime day!",
    "link": "",
    "points": "40",
    "max_tries": "99",
    "active": "0",
    "files": [
        "view.bmp"
    ],
    "author": "Matt Langois"
}
```

## Solution

<details><summary>Click me</summary>The bitmap header has been corrupted/modified (the size at byte 0x20 has been changed)

flag{you_fixed_the_header}
</details>