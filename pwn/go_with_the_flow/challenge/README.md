# Go with the flow

## Description

```
{
    "title": "Go with the flow",
    "category": "pwn",
    "description": "We managed to get restricted access to a box! \r\n\r\n`nc evilcorp.h4tt.ca 9005`\r\n\r\nP.S. We managed to get the source to the binary, see the attached file.",
    "link": "",
    "points": "50",
    "max_tries": "99",
    "active": "0",
    "files": [
        "app.c"
    ],
    "author": "Matt Langois"
}
```

## Solution

<details><summary>Click me</summary>This program is vulnerable to a buffer overflow. The program allocates 12 bytes for the buffer but then reads 16, thus the 4 bytes overflow into the integer test. Next you need to make test look like 664c617, which converts to fLaG. Since integer values are little endian it must be reversed in the overflow. Thus the overflow must look like [12 bytes]GaLf or AAAAAAAAAAAAGaLf

This will cause the readfile function to execute printing...

flag{th3_cup_0v3rfl0with}
</details>