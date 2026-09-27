---
title: Bypass Flutter SSL Pinning in Several Way
source_url: https://nikkoenggaliano.my.id/read.php?id=43
fetched_at: 2026-09-20T01:59:55Z
license: unspecified
category: mobile/flutter
---

Asssalamualaikum warahmatullahi wabarakatuh, halo teman-teman pada artikel kali ini saya akan membagikan hal yang telah saya dapatkan dalam proses Red Teaming yang saya lakukan beberapa hari ini, alasan terkuat saya menulis artikel ini adalah sebagai pengingat agar jika menemukan kasus serupa artikel ini akan menjadi dokumentasi terbaik bagi saya, di artikel ini saya tidak akan menuliskan apa itu “SSL Pinning”, saya akan langsung lurus ke bagaimana cara melakukan bypass-nya.

Ciri-ciri paling umum adanya SSL Pinning pada aplikasi adalah jika kita melakukan “*Intercepting*” maka Proxy aplikasi yang digunakan / *Burp Suite* akan mengeluarkan “*Alerting”* berupa “Failed Handshake” atau “Failed Negotiatie a TLS”. Hal ini adalah indikasi paling umum adanya SSL Pinning, hal lain yang bisa dideteksi adalah adanya error pada level aplikasi biasanya hal ini akan “pasti” ada di setiap aplikasi karena adanya `try catch` konsep yang ada pada aplikasi.

Untuk dapat melakukan “Bypass” pada aplikasi yang dibangung menggunakan Flutter ini, saya mendapatkan 2 cara yang cukup “Efektif” untuk melakukan ini terbagi secara spesifik dengan “Device” apa yang digunakan atau *Architecture* yang sedang digunakan (AMD64|86/ARM64|86).

Untuk mengetahui *arch* apa yang sedang digunakan, kita dapat menggunakan *command* `adb` seperti berikut ini `adb shell getprop ro.product.cpu.abi`

AMD

ARM

Untuk memulai cara bypass SSL pinning yang ada, pastikan aplikasi-nya ada, dalam kegiatan Pentesting / Red Teaming biasanya ada 2 cara mendapatkan aplikasi target pertama memang diberi oleh *Developer* atau mengunduh langsung dari *Playstore*, dalam kasus yang saya temui kali ini saya mendapatkan aplikasi-nya dari *Playstore*.

Jika *architecture* yang kita gunakan adalah “Intel” maka langkah-langkahnya akan sedikit “rumit” karena banyak bagian-bagian manual yang perlu dieksplorasi cukup dalam secara mandiri, tapi berikut ini langkah-langkah yang dapat ditempuh.

Extract APK dari *Devices*

Pertama cari ID dari aplikasi yang akan di-extract, jika sudah terpasang `frida client` dan `frida server` maka kita dapat menggunakan `frida-ps -Uai` setelahnya kita akan dapat mencari *real path* dari *base.apk* atau inti dari aplikasi tersebut

 `adb shell pm path [ID APLIKASI]`
Dari tangkapan layar di atas, terlihat bahwa aplikasi Flutter yang telah diinstall terbagi menjadi 5 bagian, 1 base.apk dan sisanya adalah *splitted config* atau yang sering disebut juga sebagai *App Bundle.* Hal yang perlu diperhatikan pada proses ini kita hanya butuh `split_config.x86_64.apk` dikarenakan di sanalah tempat `libflutter.so` sebagai semua “core” yang ada di aplikasi *Flutter* itu sendiri.

Pull and Decompile APK

Setelah mendapatkan target aplikasi yang ada, kita perlu mengambil bagian aplikasi itu dengan menggunakan `adb` lagi dengan cara `adb pull` berikut ini langkah-langkahnya `adb pull /data/app/~~5hQAMgTj6NWj5qyiP5stkA==/xxxx.dmp-Gh4MHOgbYVs2v9etBVybKw==/split_config.x86_64.apk`

Dari sini kita sudah mendapatkan buah `split_config` dari aplikasi taget kita, kita hanya perlu melakukan dekompilasi pada `split_config` saya biasanya menggunakan `apktool.jar` untuk melakukannya.

Dari hasil dekompilasi menggunakan `apktool.jar d split_config.x86_64.apk` akan menghasilkan sebuah folder dengan nama yang sama tanpa `.apk` isi dari folder tersebut akan hanya berfokus pada *library* dari Flutter serta beberapa konfigurasi yang diperlukan oleh aplikasi tersebut.

Pada folder `split_config.x86_64\lib\x86_64` akan terdapat 2 files inti dari Flutter, biasanya akan ada `libapp.so` dan `libflutter.so`

Terlihat pada tangkapan layar di atas, terlihat `libapp.so` dan `libflutter.so` dan beberapa *library* yang lainnya termasuk `libtoolChecker.so` yang di dalamnya berisi untuk *checker* berupa `Anti Root` dan beberapa Anti yang lainnya.

Reverse Engineering the `libflutter.so`

Pada bagian ini adalah bagian yang *Menyenangkan* bagi saya sendiri, karena bagian ini kita perlu mencari *Inject Point* dari *Binary* yang ada, lalu *Inject Point* yang bagaimana yang akan kita cari? Saya menggunakan Ghidra untuk melakukan *Reverse* binary yang ada.

Lalu apa yang harus kita lalukan saat sudah membuka Ghidra ini? mari sedikit membahas apa *library* yang digunakan oleh Flutter untuk melakukan SSL Pinning Checker, mari berkenalan dengan *boringssl*. Repository tempat asal *boringssl*, kita dapat mencari fungsi yang bernama `ssl_crypto_x509_session_verify_cert_chain`

Inilah fungsi yang mengurusi SSL Pinning di dalam aplikasi Flutter, dari sini kita harus mencari di mana letak *address* dari aplikasi ini, tapi masalah yang ada bagaimana mencari *address* aplikasi ini, sedangkan *binary* yang ada akan melakukan obfuscated terhadap fungsi-fungsi yang ada, tapi tenang dengan menggunakan Ghidra, kita masih mencari string-string yang masih terkait dengan fungsi-fungsi tersebut.

String Search Ghidra

b. Search rules

c. Search for String

d. Copy the Address

e. Go To the Address

f. Paste the Address

g. Inspect the Address

Setelah sampai pada proses **g** kita akan sampai pada sebuah ASM code yang mana akan banyak fungsi-fungsi (**FUN_005***) yang mana kita harus mencari di manakah fungsi yang paling mirip dengan isi dari `ssl_crypto_x509_session_verify_cert_chain`

Kita perlu mengecek satu persatu address yang ada untuk melihat fungsi-fungsi tersebut, kita dapat melakukan *double click* untuk mencari hasil dari dekompilasi yang ada.

Inilah fungsi dari hasil dekompilasi yang paling mirip dengan `ssl_crypto_x509_session_verify_cert_chain` kenapa? karena secara fungsi yang kita dapat lihat di *boringssl*, fungsi target memiliki 3 argument, dan hasil dekompilasi memiliki 3 argument juga

Lalu variable pertama dari fungsi target adalah menginisiasi sebuah konstanta, ke dalam sebuah pointer yang mana isi dari `SSL_AD_INTERNAL_ERROR` adalah memiliki nilai decimal 80.

```
//boring ssl
 *out_alert = SSL_AD_INTERNAL_ERROR;
//decompile
    *param_3 = 0x50;
```
Nilai decimal dari 0x50 adalah 80 dalam decimal, dari sini kita sudah dapat meyakini penuh bahwa `ulong FUN_00531a56` adalah `ssl_crypto_x509_session_verify_cert_chain` selanjutnya, kita hanya perlu merubah hasil *return* dari *boolean* fungsi ini, cara terbaiknya adalah tetap menggunakan Frida, berikut base script yang dapat digunakan.

```
var address1 = ptr('0x531a56');
var address2 = ptr('0x100000');
var fixedAddr = address1.sub(address2); //just put the address here if you has fixed
var do_dlopen = null;
var call_constructor = null;
Process.findModuleByName("linker64").enumerateSymbols().forEach(function(symbol){
    if(symbol.name.indexOf("do_dlopen") >= 0){
        do_dlopen = symbol.address;
    }
    if(symbol.name.indexOf("call_constructor") >= 0){
        call_constructor = symbol.address;
    }
});
var lib_loaded = 0;
Interceptor.attach(do_dlopen,function(){
    var library_path = this.context.rdi.readCString();
    if(library_path.indexOf("libflutter.so") >= 0){
        Interceptor.attach(call_constructor, function(){
            if(lib_loaded == 0){
                lib_loaded = 1;
                var module = Process.findModuleByName("libflutter.so");
                console.log(`[+] libflutter is loaded at ${module.base}`);
                BypassSSL(module.base.add(fixedAddr));
            }
        })
    }
});
function BypassSSL(address){
    Interceptor.attach(address, {
        onLeave: function(retval){
            retval.replace(0x1);
        }
    });
}
```
Mengingat Ghidra memulai *base image address* dari `00100000` maka kita mengurangi *address* yang didapatkan dari Ghidra dengan `0x100000` dari *script* di atas kita tidak perlu mengurangi secara manual, hanya perlu menempatkan pada variable `address1` saja. Kalau menggunakan *decompiler* yang memulai base address dari `00000000` maka kita perlu mengganti `fixedAddr` saja.

Kita dapat menjalankan frida hook untuk melakukan Bypass SSL Pinning dengan cara seperti berikut ini

`frida -U -f [nama package] -l script.js`
Dan hasilnya sudah berhasil kita bypass SSL Pinning bawaan dari Flutter ini, cara ini cukup efektif dalam berbagai kasus yang telah saya hadapi dalam pentest hari ke hari.

Untuk proses bypass SSL Pinning dengan menggunakan *architecture* *ARM* akan sangat sederhana, karena tools yang ada akan memudahkan dan mengautomasi proses yang ada, berikut ini langkah-langkahnya.

Extract All Part APK dari *Devices*

Merged All Part to 1 APK

Reflutter for Bypass SSL Pinning

Sign the apks

Jika menggunakan *arch ARM* *tools* paling Ampuh untuk saat ini masilah menggunakan reFlutter, karena prosesnya “Instan” dan probabilitas untuk berhasil lebih tinggi daripada menggunakan Frida dan melakukan *Reverse Engineering*, semoga artikel singkat ini dapat bermanfaat bagi teman-teman pentester di luar sana!
