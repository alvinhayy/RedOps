---
title: "Mass Assignment Cwe 915"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/mass-assignment-cwe-915.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# Mass Assignment (CWE-915) – Privilege Escalation via Unsafe Model Binding

## 1) Finding Mass Assignment

Look for self-service endpoints that create or update objects:[\[2\]](#references)

- `PUT/PATCH /api/users/{id}`
- `PATCH /me` ,`PUT /profile`
- `PUT /api/orders/{id}`
- `POST /api/checkout`
- GraphQL mutations such as `updateProfile` ,`editUser` ,`saveCart` ,`completeCheckout`

Heuristics indicating mass assignment:

- The response echoes server-managed fields (e.g., `roles` ,`status` ,`isAdmin` ,`permissions` ,`ownerId` ,`tenantId` ) even when you didn’t send them.
- Client bundles contain role names/IDs or other privileged attribute names used throughout the app (`admin` ,`staff` ,`moderator` ,`internal flags` ), hinting bindable schema.
- Backend serializers accept unknown fields without rejecting them.
- Validation errors reveal hidden property names or expected types after you submit additional JSON keys.
- The same object is returned by both a read route and an update route, but the update UI only edits a small subset of fields.

Quick test flow:

1. Perform a normal update with only safe fields and observe the full JSON response structure (this leaks the schema).
2. Repeat the update including a crafted privileged field in the body. If the response persists the change, you likely have mass assignment.
3. If the app rejects the key, try the same idea with nested objects, arrays, alternate casing, or partial-update verbs (`PATCH` , JSON Merge Patch, GraphQL mutations).

Example baseline update revealing schema:[\[1\]](#references)

```
PUT /api/users/12934 HTTP/1.1
Host: target.example
Content-Type: application/json
{
  "id": 12934,
  "email": "user@example.com",
  "firstName": "Sam",
  "lastName": "Curry"
}
```
Response hints at privileged fields:

```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "id": 12934,
  "email": "user@example.com",
  "firstName": "Sam",
  "lastName": "Curry",
  "roles": null,
  "status": "ACTIVATED",
  "filters": []
}
```
Useful high-impact property classes to test:

- **Privilege / trust flags** :`role` ,`roles` ,`isAdmin` ,`permissions` ,`verified` ,`emailVerified` ,`kycStatus`
- **Ownership / tenant pivots** :`ownerId` ,`organizationId` ,`tenantId` ,`accountId` ,`userId`
- **Business logic knobs** :`price` ,`discount` ,`credit` ,`balance` ,`limit` ,`refundAmount` ,`status`
- **Backend processing fields** :`templateId` ,`conversionParams` ,`exportFormat` ,`webhookUrl` ,`filePath`

Quick response-schema diffing from the CLI:

```
curl -s https://target.example/api/users/12934 -H "Authorization: Bearer $TOKEN" | jq -r 'paths(scalars) | map(tostring) | join(".")' | sort -u
```
## 2) Exploitation – Role Escalation via Mass Assignment

Once you know the bindable shape, include the privileged property in the same request.[\[1\]](#references)[\[3\]](#references)

Example: set `roles` to `ADMIN` on your own user resource:[\[1\]](#references)

```
PUT /api/users/12934 HTTP/1.1
Host: target.example
Content-Type: application/json
{
  "id": 12934,
  "email": "user@example.com",
  "firstName": "Sam",
  "lastName": "Curry",
  "roles": [
    { "id": 1, "description": "ADMIN role", "name": "ADMIN" }
  ]
}
```
If the response persists the role change, re-authenticate or refresh tokens/claims so the app issues an admin-context session and shows privileged UI/endpoints.

Notes

- Role identifiers and shapes are frequently enumerated from the client JS bundle or API docs. Search for strings like `roles` ,`ADMIN` ,`STAFF` , or numeric role IDs.
- If tokens contain claims (e.g., JWT roles), a logout/login or token refresh is usually required to realize the new privileges.
- Test create flows too (`POST /register` ,`POST /users` , invite flows, support-ticket creation). Some apps reject`role` changes on edit but still accept them on object creation.

## 3) Hidden-Field Recon Beyond the Obvious

- Inspect minified JS bundles for role strings and model names; source maps may reveal DTO shapes.
- Look for arrays/maps of roles, permissions, feature flags, workflow states, and checkout objects. Build payloads matching the exact property names and nesting.
- Compare **GET** responses with**POST/PUT/PATCH** request bodies. If the response object contains`discount` ,`credit` ,`role` ,`status` , or nested`internal` objects not present in the request, try replaying them in the write request.
- Fetch machine-readable API docs if present (`/swagger.json` ,`/v2/api-docs` ,`/openapi.json` , GraphQL introspection). Hidden fields often appear in schemas even when the frontend never sends them.
- Use error oracles: sending an unexpected key with the wrong type can reveal whether the server actually tried to bind it.

Handy greps against a downloaded bundle:

```
strings app.*.js | grep -iE "role|admin|isAdmin|permission|status|tenant|owner|discount|credit" | sort -u
```
GraphQL introspection is especially useful when a mutation input type exists but the frontend only populates a subset of it:

```
query IntrospectUserInput {
  __type(name: "UpdateUserInput") {
    inputFields {
      name
    }
  }
}
```
If changing `ownerId`, `organizationId`, or similar moves the object into another tenant/account, pivot into [IDOR / BOLA testing](idor.html) immediately because mass assignment often becomes the write-side primitive for a broader authorization break.

## 4) High-Value Abuse Patterns

**Nested relation / tenant hijack**

- Don’t stop at `role=admin` . In real APIs, reassigning`organizationId` ,`accountId` , or`ownerId` is often more valuable because it can move your session, cart, invoice, API key, or ticket into another tenant.
- Nested payloads are common: `{"profile":{"organizationId":7}}` ,`{"order":{"owner":{"id":7}}}` ,`{"user":{"team":{"id":1}}}` .

**Business-flow tampering**

- Checkout and billing APIs often return fields like `credit` ,`chosen_discount` ,`price` ,`coupon` ,`refundAmount` , or`approved` . If those properties can be echoed back inside the write request, you may get free purchases, over-refunds, or approval bypasses.
- Partial-update routes are worth hammering because developers sometimes protect the main UI form but forget alternate JSON/API handlers.

**Downstream exploit chaining**

- Some mass-assignment bugs don’t end at privilege escalation. If you can set a backend-only processing option such as transcoding flags, template selectors, or webhook destinations, the impact can become command injection, SSRF, or arbitrary workflow execution.
- A classic example is a video object exposing an internal conversion parameter field: modifying that property may later influence a shell command when the media is processed.

## 5) Framework Pitfalls and Secure Patterns

The vulnerability arises when frameworks bind `req.body` directly onto persistent entities. Below are common mistakes and minimal, secure patterns.

**Node.js (Express + Mongoose)**

Vulnerable:

```
// Any field in req.body (including roles/isAdmin) is persisted
app.put('/api/users/:id', async (req, res) => {
  const user = await User.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(user);
});
```
Fix:

```
// Strict allow-list and explicit authZ for role-changing
app.put('/api/users/:id', async (req, res) => {
  const allowed = (({ firstName, lastName, nickName }) => ({ firstName, lastName, nickName }))(req.body);
  const user = await User.findOneAndUpdate({ _id: req.params.id, owner: req.user.id }, allowed, { new: true });
  res.json(user);
});
// Implement a separate admin-only endpoint for role updates with server-side RBAC checks.
```
**Ruby on Rails**

Vulnerable (no strong parameters):

```
def update
  @user.update(params[:user]) # roles/is_admin can be set by client
end
```
Fix (strong params + no privileged fields):

```
def user_params
  params.require(:user).permit(:first_name, :last_name, :nick_name)
end
```
**Laravel (Eloquent)**

Vulnerable:

```
protected $guarded = []; // Everything mass-assignable (bad)
```
Fix:

```
protected $fillable = ['first_name','last_name','nick_name']; // No roles/is_admin
```
**Django / ModelForms**

Vulnerable pattern:

```
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"  # exposes server-managed fields if reused in self-service flows
```
Fix:

```
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "nick_name"]
```
**Spring Boot (Jackson)**

Vulnerable pattern:

```
// Directly binding to entity and persisting it
public User update(@PathVariable Long id, @RequestBody User u) { return repo.save(u); }
```
Fix: Map to a DTO with only allowed fields and enforce authorization:

```
record UserUpdateDTO(String firstName, String lastName, String nickName) {}
```
Then copy allowed fields from DTO to the entity server-side, and handle role changes only in admin-only handlers after RBAC checks. Use `@JsonIgnore` on privileged fields if necessary and reject unknown properties.

**ASP.NET Core**

Vulnerable pattern:

```
[HttpPost]
public async Task<IActionResult> Edit(int id, User user) {
    _db.Update(user);
    await _db.SaveChangesAsync();
    return Ok(user);
}
```
Fix: bind to a dedicated view model / DTO and map explicitly:

```
public record UserUpdateDto(string FirstName, string LastName, string NickName);
```
Microsoft explicitly treats this as **overposting** and recommends view models over binding entity classes directly, especially on edit paths.

**FastAPI / Pydantic**

Use separate input models for self-service routes and reject extras instead of reusing a broad DB model:

```
from pydantic import BaseModel
class UserUpdate(BaseModel):
    model_config = {"extra": "forbid"}
    first_name: str | None = None
    last_name: str | None = None
    nick_name: str | None = None
```
**Go (encoding/json)**

- Ensure privileged fields use `json:"-"` and validate with a DTO struct that includes only allowed fields.
- Consider `decoder.DisallowUnknownFields()` and post-bind validation of invariants (`roles` cannot change in self-service routes).

## References
