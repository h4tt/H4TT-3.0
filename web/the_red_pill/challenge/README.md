# The Red Pill

## Description

```
{
    "title": "The Red Pill",
    "category": "web",
    "description": "Morpheus has an interesting decision for you Neo.",
    "hint": "alg is an interesting jwt payload header.",
    "link": "https://evilcorp.h4tt.ca/the-red-pill",
    "points": "85",
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

<details><summary>Click me</summary>Going to jwt.io you'll notice an article advertised https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/

Mainly that an attacker can make use of the "alg" key in the header to exploit the jwt verification when the server uses assymetric JWT verification. In this challenge since we provide a public key it can be assumed that assymetric verification is used.

Assymetric has the interesting property that it signs using the Private Key but validates using the public key. So then the serverside verification would look like so:

`jwt.verify(token, publicKey)`. This has been patched in current implementations of the JWT libraries. However this server code cares about the algorithm in the header and will use whichever algorithms to verify that was specified in the header of the JWT.

So then if the user crafts a jwt token with the crafted body asking for the "red" pill rather than the given "blue" pill in the body. And signs it with a symmetric algorithm like "HS256" with the key being the public key. Then the JWT verification will accept it and pass back the flag.

The following token should return the flag: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXF1ZXN0ZWRQaWxsIjoicmVkIiwiaWF0IjoxNTcyOTIwOTcwfQ.NFbZX5bAUH0bPJGS79WQfxiAW6sewJ25q3qYYgOQyLM`

Flag: flag{d0n7_7ru57_7h3_4lg}
</details>