# Fast Cookie

## Description

```
{
    "title": "Fast Cookie",
    "category": "web",
    "description": "Can you catch it?",
    "hint": "____ shoulders, knees and toes!",
    "link": "https://evilcorp.h4tt.ca/fast-cookie",
    "points": "25",
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

<details><summary>Click me</summary>The server sends out a cookie with the flag when making a get request to /fast-cookies with a max age of 1 milisecond. However if you go into the dev-tools and look at the cookes they won't show. The only way to view it is to check the headers either via a `curl -i` request, going into the dev-tools and looking at the header under the network tab. Or to check it out with burpsuite.

The set cookie portion is urlencoded so you might have to use a url deocder to get the cookie value in more legible text.

Flag: flag{l00k_47_7h3_h34d3r}
</details>