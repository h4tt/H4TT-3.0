# Racing the Beam

## Description

```
{
    "title": "Racing the Beam",
    "category": "misc",
    "description": "We intercepted a secret file, but how can anything fit in 24K?!",
    "link": "",
    "points": "40",
    "max_tries": "99",
    "active": "0",
    "files": [
        "hack"
    ],
    "author": "Matt Penny"
}
```

## Solution

<details><summary>Click me</summary>The file `hack` is an NES ROM. Run it in an emulator and after the intro some green garbage will
will appear on the screen. This is actually the flag but the ROM uses raster effects to obscure it
as the screen is being rendered. However, these effects are applied on top of the actual screen
layout (nametable) so it is possible to see what it says using an emulator's debugging features.

flag{n0_t1m3_f0r_g4m3s}
</details>