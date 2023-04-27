# Maybe Crypto

## Description

```
{
    "title": "Maybe Crypto",
    "category": "rev",
    "description": "The flag is somewhere in the binary. Can you find it?",
    "link": "",
    "points": "50",
    "max_tries": "99",
    "active": "0",
    "files": [
        "challenge"
    ],
    "author": "Sean Maher"
}
```

## Solution

<details><summary>Click me</summary>This problem is a simple XOR pad. We have our key (0x10), and we're iterating over our ciphertext.
The ciphertext is the second string in the binary, I didn't want to make it too obvious, I have fake 
strings and buffers (initialized to 0).

To find the flag, you can do one of two things. One, by identifying that this is an XOR pad, you can simply 
grab the ciphertext, key, and xor it yourself in a script, or online. 
If you're like me and you're lazy, you'll just set a breakpoint before the memset (which clears the memory 
where the flag was), run the program, and dump the stack. It'll be in memory, clear as day.

flag{r3v_0r_crypt0}

</details>