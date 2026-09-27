---
title: "Bruteforce hash (few chars)"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/python/bruteforce-hash-few-chars.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: tools
---

# Bruteforce Hash Few Chars

```
import hashlib
target = '2f2e2e' #/..
candidate = 0
while True:
    plaintext = str(candidate)
    hash = hashlib.md5(plaintext.encode('ascii')).hexdigest()
    if hash[-1*(len(target)):] == target: #End in target
        print('plaintext:"' + plaintext + '", md5:' + hash)
        break
    candidate = candidate + 1
```
```
#From isHaacK
import hashlib
from multiprocessing import Process, Queue, cpu_count
def loose_comparison(queue, num):
	target = '0e'
	plaintext = f"a_prefix{str(num)}a_suffix"
	hash = hashlib.md5(plaintext.encode('ascii')).hexdigest()
	if hash[:len(target)] == target and not any(x in "abcdef" for x in hash[2:]):
		print('plaintext: ' + plaintext + ', md5: ' + hash)
		queue.put("done") # triggers program exit
def worker(queue, thread_i, threads):
	for num in range(thread_i, 100**50, threads):
		loose_comparison(queue, num)
def main():
	procs = []
	queue = Queue()
	threads = cpu_count() # 2
	for thread_i in range(threads):
		proc = Process(target=worker, args=(queue, thread_i, threads ))
		proc.daemon = True # kill all subprocess when main process exits.
		procs.append(proc)
		proc.start()
	while queue.empty(): # exits when a subprocess is done
		pass
	return 0
main()
```
## References
