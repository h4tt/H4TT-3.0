# The Agent In Estonia

## Description

```
{
    "title": "The Agent In Estonia",
    "category": "crypto",
    "description": "One of our FSociety agents was undercover in Estonia in 2017. We haven't heard from him since, and we thought he was KIA. However, we've recently recieved a file with their identity card. Clearly the agent is trying to give us some information, but what is it?",
    "link": "",
    "points": "180",
    "max_tries": "99",
    "active": "0",
    "files": [
        "jaak-joeorg.zip"
    ],
    "author": "Clayton Smith and Forest Anderson"
}
```

## Solution

<details><summary>Click me</summary>The public key is vulnerable to the ROCA attack. This was hinted to by the Estonian identity cards, which had the same problem in 2017. You need to find something that makes use of the attack, such as: https://github.com/argilo/ROCA_SAS or https://gitlab.com/jix/neca

Once you have cracked the public key and have p and q, you can generate the private key with a tool like https://github.com/ius/rsatool

p = 126964385406516869019574570507880488608489232876197956365247703493295519051033
q = 131206414487224030504707496238767554301002010236858260973825608596162602205471

Finally, you can create the private key and decrypt the file

flag{c0pp3rsmith_4nd_j030rg_b0th_b4ck_fr0m_d34d}</details>