# Hog

## Description

```
{
    "title": "Hog",
    "category": "crypto",
    "description": "EEMEMEMEMEEEEEEEEMMEEMEMMEMEMMEMEMMEMEMMEEEEMEEEEEEEEMEEMMEMEMMEE\n\nformat: FLAG{UPPERCASE-WITH-DASHES-FOR-SPACE}",
    "link": "",
    "points": "50",
    "max_tries": "99",
    "active": "0",
    "files": [],
    "author": "Dave Petrasovic"
}
```

## Solution

<details><summary>Click me</summary>The title "Hog" should provide a hint to the type of cipher used: Bacon Cipher
https://www.dcode.fr/bacon-cipher
Plugging the cipher in there will yield a couple of results. Only one will be coherent.
Some manual work will need to be done to get from MMMMBACON to the flag but it should
be obvious what changes to make as the description tells you the format.

FLAG{MMMM-BACON}
</details>