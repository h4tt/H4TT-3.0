# Report Generator

## Description

```
{
    "title": "Report Generator",
    "category": "web",
    "description": "Evil Corp threw up an interesting report generator",
    "hint": "The name field looks pretty interesting",
    "link": "https://evilcorp.h4tt.ca/generate-report",
    "points": "20",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "required": "",
    "author": "Francisco Trindade"
}
```

## Solution

<details><summary>Click me</summary>The name field is suseptible to XSS. You can get the flag if you submit anything in that field of the form "<script>{something}</script>"

Flag: flag{x55_m34n5_n0_v4l1d4710n}
</details>