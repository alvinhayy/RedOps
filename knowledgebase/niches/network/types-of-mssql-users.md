---
title: "Types of MSSQL Users"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-mssql-microsoft-sql-server/types-of-mssql-users.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Offensive reading of `sys.database_principals`

`sys.database_principals`
From an attacker perspective, this view is more useful than just a user list:[\[1\]](#references)[\[3\]](#references)

- `type` /`type_desc` quickly tells you if you are dealing with a regular SQL user (`S` ), Windows-backed principal (`U` /`G` ), a role (`R` ), or Microsoft Entra-backed principals (`E` /`X` ).
- `authentication_type_desc='DATABASE'` is a strong hint of a**contained** user. These accounts live inside the database, are easy to miss if you only enumerate server logins, and often survive restores/migrations.
- `authentication_type_desc='NONE'` usually means a principal that cannot authenticate directly (for example some`WITHOUT LOGIN` , certificate-mapped, asymmetric-key, or role-style principals), but it can still matter for ownership chains and`EXECUTE AS USER` .
- `owning_principal_id` matters when reviewing custom roles, application roles, or ownership chains.
- `is_fixed_role=1` only tells you that the principal is a built-in role. It does**not** show all effective permissions inherited through that role, so always enumerate role membership separately.

If your output looks incomplete, remember that metadata visibility is restricted. A low-privileged user can always see their own principal, system users, and fixed database roles, but not necessarily every other user or role member.

## Quick enumeration

```
SELECT dp.name,
       dp.type,
       dp.type_desc,
       dp.authentication_type_desc,
       SUSER_SNAME(dp.sid) AS mapped_login,
       USER_NAME(dp.owning_principal_id) AS owner_name,
       dp.default_schema_name,
       dp.create_date
FROM sys.database_principals AS dp
WHERE dp.name NOT IN ('sys', 'INFORMATION_SCHEMA')
ORDER BY dp.type_desc, dp.name;
```
```
SELECT r.name AS role_name,
       m.name AS member_name,
       m.type_desc,
       m.authentication_type_desc
FROM sys.database_role_members AS drm
JOIN sys.database_principals AS r ON r.principal_id = drm.role_principal_id
JOIN sys.database_principals AS m ON m.principal_id = drm.member_principal_id
ORDER BY r.name, m.name;
```
```
SELECT grantee.name AS grantee,
       target.name AS target_user,
       perm.state_desc
FROM sys.database_permissions AS perm
JOIN sys.database_principals AS grantee ON grantee.principal_id = perm.grantee_principal_id
JOIN sys.database_principals AS target ON target.principal_id = perm.major_id
WHERE perm.class_desc = 'DATABASE_PRINCIPAL'
  AND perm.permission_name = 'IMPERSONATE';
```
Useful quick triage for suspicious/high-value principals:

```
SELECT name, type_desc, authentication_type_desc
FROM sys.database_principals
WHERE name IN ('dbo', 'guest')
   OR is_fixed_role = 1
   OR type IN ('E', 'X')
   OR authentication_type_desc IN ('DATABASE', 'EXTERNAL')
ORDER BY name;
```
## Principals and roles worth special attention

- **`dbo`** : this is**not** the same as the`db_owner` role and**not** the same as the login recorded as database owner. If you can reach`EXECUTE AS USER = 'dbo'` or`EXECUTE AS OWNER` , explicit`DENY` on the original principal is not a reliable barrier anymore.
- **`guest`** : every database has it. If`CONNECT` is available, users without a mapped database principal can inherit any permission granted to`guest` . Enumerate both`guest` and`public` grants when access seems broader than expected.
- **Contained users and `WITHOUT LOGIN` users** : contained users are good pivot and persistence indicators because they do not depend on a server login.`WITHOUT LOGIN` users cannot authenticate directly, but Microsoft explicitly notes that they can connect to other databases as`guest` , so they are especially interesting when you already control execution context changes.
- **`db_securityadmin`** : this role can manage permissions and custom role membership, so it can often be turned into a stronger position even when it is not instant`sysadmin` . Fixed-role membership changes still require`db_owner` .
- **`EXTERNAL_USER` / `EXTERNAL_GROUPS`** : in Azure SQL / SQL Managed Instance these are usually Microsoft Entra-backed identities. Do not ignore them during enumeration because they can own schemas, be role members, and participate in impersonation paths. Database-principal impersonation is supported even where server-level Entra impersonation is limited.
- **Special roles in `msdb`** : enumerate them separately. Microsoft documents that`db_ssisadmin` and`dc_admin` can become privilege-escalation material because Integration Services packages may end up executing through SQL Server Agent in a high-privilege context.<sup>[\[1\]](#references)</sup>

If you find interesting `IMPERSONATE`, `db_owner`, or linked-server paths, continue from the main MSSQL page:

## Tooling

MSSQLPwner can enumerate **linked-server** and **impersonation chains** automatically:[\[2\]](#references)

```
mssqlpwner corp.com/user:pass@10.10.10.10 enumerate
mssqlpwner corp.com/user:pass@10.10.10.10 get-chain-list
mssqlpwner corp.com/user:pass@10.10.10.10 interactive
```
## References

- [1] [Microsoft Learn - Database-Level Roles](https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles?view=sql-server-ver17)
- [2] [ScorpionesLabs - MSSqlPwner](https://github.com/ScorpionesLabs/MSSqlPwner)
- [3] [Microsoft Learn - sys.database_principals (Transact-SQL)](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-database-principals-transact-sql?view=sql-server-ver17)
