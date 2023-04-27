# Eye of the Parser

## Description

```
{
    "title": "Eye of the Parser",
    "category": "stego",
    "description": "We found this strange file but have no idea what's inside it, or even what it is.",
    "link": "",
    "points": "120",
    "max_tries": "99",
    "active": "0",
    "files": [
        "Challenge.zip"
    ],
    "author": "Matt Penny"
}
```

## Solution

<details><summary>Click me</summary>1) Challenge.zip has a file in it called `secret.txt`. Write the value in this file down for later
   (16 byte hex value encoded in ASCII)
2) Challenge.zip has a GIF appended to it. Retrieve it using dd, a hex editor, or some other tool
3) The GIF from (2) has a text comment in it (16 byte hex value encoded in ASCII). Write this value
   down for later
4) The GIF from (2) is also valid HTML. Open it in a browser and save the JPEG that is displayed
5) Note the comment in the JPEG from (4). It is telling you to encrypt the file. Encrypt it using
   aes-128-cbc. The key is the value from (1) and the IV is the value from (4) (they are both exactly
   128 bits in length! -- one AES block). I.e.,
   `openssl aes-128-cbc -K 746869735f69736e745f615f666c6167 -iv 1ecd05afd2f241cf3ce9fe2d005f46d8 -in JPG -out PNG`
6) The result of the encryption in (5) is a PNG containing the key


flag{g3t_4head3r}

---

The comment in the JPEG instructing you to encrypt it coupled with the fact that "secret.txt" and the
GIF comment are both 128 bits/16 bytes long are intended as a hint to use 128-bit AES. The key actually
decodes to "this_isnt_a_flag" but I kept it in hex to help draw out the pacing of the puzzle and (hopefully)
allow the challenger to more easily recognize the IV in the GIF comment and that it is a significant value.
</details>