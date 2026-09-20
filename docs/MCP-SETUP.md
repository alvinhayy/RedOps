# Mobile runtime MCP setup

RedOps keeps mobile runtime automation optional and external to the default
installation. The recommended adapter is
[uiautomator2-mcp](https://github.com/fdciabdul/uiautomator2-mcp), backed by
[openatx/uiautomator2](https://github.com/openatx/uiautomator2). It provides
screen capture, UI hierarchy inspection, input, app lifecycle, and read-only
device information for an authorized Android emulator/device.

## Authorization and device scope

Use this MCP only with a device/emulator you own or have written authorization to
test, and only with an in-scope application. Prefer a disposable emulator and a
dedicated test account. Do not connect a personal device, production account, or
third-party device. The server's `shell_command` capability can change device
state, so use it only when that action is explicitly in scope.

Static analysis remains static: do not install or launch the target while using
`reverse-engineer`. Runtime MCP is only for the later, authorized confirmation
phase. Native fuzzing remains offline/local and should not use this MCP to send
fuzz cases to a remote service.

## Install upstream server (optional)

```bash
git clone https://github.com/fdciabdul/uiautomator2-mcp.git ~/tools/uiautomator2-mcp
cd ~/tools/uiautomator2-mcp
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
adb devices
```

The clone and virtual environment are intentionally outside this repository. No
MCP package is required by the default RedOps install.

## Generic MCP client configuration

Use absolute paths and never put tokens in this JSON:

```json
{
  "mcpServers": {
    "redops-exegol": {
      "command": "redops",
      "args": ["exegol-mcp"]
    },
    "uiautomator2": {
      "command": "/Users/me/tools/uiautomator2-mcp/.venv/bin/python",
      "args": ["/Users/me/tools/uiautomator2-mcp/server.py"]
    }
  }
}
```

The Exegol adapter is local and argv-safe. Use it for isolated tools such as
Frida, `jadx`, or `apktool` when they are available in the selected container.

## RedOps configuration and health check

RedOps does not start the third-party server automatically. Set these optional
values when a client or launcher needs a canonical command:

```bash
export REDOPS_MOBILE_MCP_PYTHON="$HOME/tools/uiautomator2-mcp/.venv/bin/python"
export REDOPS_MOBILE_MCP_SERVER="$HOME/tools/uiautomator2-mcp/server.py"
export REDOPS_MOBILE_DEVICE_SERIAL=emulator-5554
```

The configuration validator only checks local paths and does not contact the
device. Before runtime work, perform a read-only check:

```bash
adb devices -l
redops exegol status
```

Then initialize the MCP session with `connect_device`, followed by
`device_info`, `app_current`, and `dump_hierarchy_summary`. Stop if the serial is
not the intended isolated device. The mobile agent profile is documented in
[`mobile-agent.md`](mobile-agent.md).

## Other optional connectors

See [`mcp-tools.md`](mcp-tools.md) and the non-secret
[`.mcp.json.example`](../.mcp.json.example) for Burp, optional Camoufox, Ghidra,
radare2, and bounded terminal MCP routing. BloodHound is an AD/identity-only
connector and is not part of the mobile workflow. Exegol remains first choice:
Burp is limited to authorized mobile-app proxy traffic, Ghidra/r2 to local static
analysis, and terminal MCP to approved allowlisted argv inside the workspace.
