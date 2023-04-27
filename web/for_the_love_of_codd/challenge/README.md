# For the Love of Codd

## Description

```
{
    "title": "For the Love of Codd",
    "category": "web",
    "description": "It looks like EvilCorp runs personalized web portals for employees to access the contents of their corporate phones. We've got access to one of them - I wonder if there are any secrets in there.",
    "link": "https://evilcorp.h4tt.ca/phone-access",
    "points": "70",
    "max_tries": "99",
    "active": "0",
    "files": [],
    "author": "Matt Penny",
    "instructions": "The nodejs challenge server needs to be hosted somewhere"
}
```

## Solution

<details><summary>Click me</summary>1) The endpoint http://SERVER/ui/sms-convo/info/id is vulnerable to SQL injection. Enter `1+1` as the
   id, for example, and observe that the input is evaluated (i.e., conversation 2 is rendered).
   Additionally, malformed queries will return SQL errors.

2) Determine the number of columns expected in the query result. Union the results of an arbitrary
   query to the results. Keep adding columns to the query until no error is returned:

   http://SERVER/ui/sms-convo/info/1 UNION SELECT 10,9,8,7,6,5,4,3,2 FROM sqlite_master

   We can deduce that the server expects the query result to have 9 columns. Look at the rendered
   SMS conversation and notice that another message has been added to the bottom. Observe that
   the '3' column corresponds to the message sender and the '5' column corresponds to message body.
   This can be used to extract data.

3) Enumerate all tables the in database using the sqlite_master table and add their information to
   the chat. For this example, message sender will be table name and message body will be the query
   that created it.

   http://SERVER/ui/sms-convo/info/1 UNION SELECT 10,9,8,7,6,sql,4,tbl_name,2 FROM sqlite_master WHERE type='table'

   We now have the schema of every table in the database

4) Notice there is a table called 'secrets'. Access it and retrieve the flag:

   http://SERVER/ui/sms-convo/info/1 UNION SELECT 10,9,8,7,6,secretContent,4,secretType,2 FROM secrets

flag{th3_nam3s_t4bles_r0bert_tab1e5}</details>