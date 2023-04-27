# An Old Way

## Description

```
{
    "title": "An Old Way",
    "category": "forensics",
    "description": "You find yourself in a room with a strip of paper being fed out of a wall and a flashing light. After a time, it stops. On the tape is a sequence of bits traced out. The start and end are smudged. What could they mean? \n...1111111111111111111111100000111111101101011111110010000001001110011011110010110000100000011101000110100001101001011100110010000001101001011100110010000001101110011011110111010000100000011000010111001101100011011010010110100100101110001000001110100000010111110110110010000111101011011011111111100110110110001111111010101101100001111110001101001110110001111111101100011111111011000111010100110110001111111100000001110110111111101100001100100100000010000000000000000000000000000...\nflag format: flag(UPPER_CASE)",
    "link": "",
    "points": "63",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "author": "Griffin"
}
```

## Solution

<details><summary>Click me</summary>#############################
#
# FLAG(I-R3AD-PUNCH-TAP3)
#
# Explination
#
#
# The intended way to solve this envolves reading 
# https://en.wikipedia.org/wiki/Baudot_code#ITA2
# 
# ITA2 is International telegraphy alphabet No. 2 (Baudot–Murray code)
# 

111   #Wake up pulses
11111
11111
11111
11111
00000 #synchronization pulse
11111 #back porch
11011 #figure shift (FS)
01011 #bell 
11111 #letter shift (LS)

# The fake ascii block, it is alligned to the 8 bit bounds

00100000 #[space]
01001110 #N
01101111 #o
00101100 #,
00100000 #[space]
01110100 #t
01101000 #h
01101001 #i
01110011 #s
00100000 #[space]
01101001 #i
01110011 #s
00100000 #[space]
01101110 #n
01101111 #o
01110100 #t
00100000 #[space]
01100001 #a
01110011 #s
01100011 #c
01101001 #i
01101001 #i
00101110 #.
00100000 #[space]

111      #filler to correct allignment

# This ascii block's length in bits must evenly devide in 5, fill with ones until it does
# when this block is read as ITA2, it should not contain [OIOOI] while in symbol shift, as this has special meaning, it is a request for a reply with identifying information


01000 #[CR]
00010 #[LF]
11111 #[LS]
01101 #F
10010 #L
00011 #A
11010 #G
11011 #[FS]
01111 #(
11111 #[LS]
00110 #I
11011 #[FS]
00011 #-
11111 #[LS]
01010 #R
11011 #[FS]
00001 #3
11111 #[LS]
00011 #A
01001 #D
11011 #[FS]
00011 #-
11111 #[LS]
10110 #P
00111 #U
11111 #[LS]
01100 #N
01110 #C
10100 #H
11011 #[FS]
00011 #-
11111 #[LS]
10000 #T
00011 #A
10110 #P
11111 #[LS]
11011 #[FS]
00001 #3
10010 #)
01000 #[CR]
00010 #[LF]

#free to add some garbage here, 5 bit alligned

00000 #[null]
00000 #[null]
00000 #[null]
00000 #[null]
00000 #[null]
00    #[trailing silence]
</details>