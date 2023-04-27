# EC 3: A Weak Login

## Description

```
{
    "title": "EC 3: A Weak Login",
    "category": "evilcorp",
    "description": "Looks like the leaked memo might reveal some security vulnerabilities on the login form. See if you can't gain access.",
    "hint": "You can GET an HTTP page but also XXXX an HTTP page.",
    "link": "https://evilcorp.h4tt.ca",
    "points": "50",
    "max_tries": "99",
    "active": "0",
    "files": [
        ""
    ],
    "required": "EC 2: An Interesting Memo",
    "author": "Francisco Trindade"
}
```

## Solution

<details><summary>Click me</summary>In the top secret markdown document contained in the ZIP file the hint to "knock on the post-mans door before logging in" is to point towards making a POST request to `/evilcorp-login`. You'll receive back:

Here's your cookie: {"admin":"e2lzY29ycGFkbWluOiBmYWxzZX0K="}

Then base64 decode the value of the json file will return "{iscorpadmin: false}". The next step is to then base64 encode "{iscorpadmin: true}". Which encode to e2lzY29ycGFkbWluOiB0cnVlfQo=. Then injecting the cookie: {"admin": "e2lzY29ycGFkbWluOiB0cnVlfQo="} and putt ing in any username/password combo will result in getting accepted and redirecting to "/evilcorp-home?file=listing". Click on the file "flag.txt" will reveal the flag.

Flag: flag{wh0_n33d5_l061n_cr3d5}
</details>