# Token for your Thoughts

## Description

```
{
    "title": "Token for your Thoughts",
    "category": "crypto",
    "description": "We got word that Evilcorp is trying out a new authentication mechanism. It's pretty new and untested so I doubt it's secure. See if you can break it.",
    "link": "https://evilcorp.h4tt.ca/evilcorp-login",
    "points": "40",
    "max_tries": "99",
    "active": "0",
    "files": [],
    "author": "Matt Penny",
    "instructions": "The nodejs challenge server needs to be hosted somewhere"
}
```

## Solution

<details><summary>Click me</summary>1) Try to log in. You will get an error about not being an admin
2) Guess that the username is "admin" and enter any number in the token field,
   then try to log in again. You will be shown the previous token and need to
   enter the next one.
3) In the response headers are "Server: JBoss-EAP/7" and "X-Powered-By: JSP/2.3".
   Both of these indicate a Java-based environment (this is not actually the case,
   but the token was generated using standard Java classes -- this is a hint).
4) Notice that the previous token is 64 bits long and assume that
   java.util.Random.nextLong() was used to generate it. The implementation of
   nextLong() is defined as:
   ```
      return (nextInt() << 32) + nextInt();
   ``` 
   and nextInt() is defined as:
    ```
      seed = (seed * 0x5DEECE66DL + 0xBL) % (1L << 48);
      return seed >> 16;
   ```
   This is a simple linear congruental generator with 0x5DEECE66DL as the multiplier,
   0xBL as the increment, and 2^48 as the modulus. We have
   prevTok = (nextInt() << 32) + nextInt and can calculate num2 = prevTok & 0xFFFFFFFFL and
   num1 = (prevTok - num2) >> 32 -- the outputs of nextLong()'s 2 calls to nextInt().

   Now that we have two consecutive outputs of the LCG we can calculate its internal state
   (seed). There is a bit of bruteforcing to do since the seed is shifted 16 bits before being
   returned from nextInt(). Calculate seed = (((num1 << 16) | x) * 0x5DEECE66DL + 0xBL) % (1L << 48).
   When seed >> 16 is equal to num2 (for some 16-bit integer x), then you can apply the LCG two more
   times to generate two new 32-bit integers to form a 64-bit long.
5) Use the new long from (4) as the next token and you will receive the flag


flag{sh0u1d_h4ve_us3d_5ecur3r4nd0m}
</details>