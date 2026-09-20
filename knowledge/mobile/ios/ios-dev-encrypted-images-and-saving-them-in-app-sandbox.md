---
title: "IOS Dev - Encrypting images and saving them in App Sandbox"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2013/09/26/ios-dev-encrypted-images-and-saving-them-in-app-sandbox.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

One of the requirements in my latest project was to encrypt an image and save it on the device in the application’s sandbox, then decrypt is during runtime and upload it to the server. I looked at the documentation for Apple’s CommonCrypto Framework, but it was taking me plenty of time to implement it so instead i decided to use some wrappers that would get the job done for me. I found the [RNCryptor](https://github.com/rnapier/RNCryptor) library on Github that uses AES encrypton. It was pretty simple to implement it. First, download the files from its github url and include all the files that are relevant to you present inside the **RNCryptor** folder on your project. In my case, i just imported all of them for now.  Then use the following code to encrypt the image.

```
//  Code for encrypting and saveing image
    UIImage *imageToEncrypt = [UIImage imageNamed:@"SomeImage"];
    NSString  *imagePath = [NSHomeDirectory() stringByAppendingPathComponent:@"Documents/encryptedImage.png"];
    NSData *data = UIImagePNGRepresentation(fetchedImage);
    NSError *error;
    NSData *encryptedData = [RNEncryptor encryptData:data
                                        withSettings:kRNCryptorAES256Settings
                                            password:@"ABC123"
                                               error:&error];
   [encryptedData writeToFile:imagePath atomically:YES];
```
Note that encryting and decrypting the image requires a passcode (ABC123). To decrypt the image, use the following code ..

```
 //  Code for loading image by decryption
    NSString  *imagePath = [NSHomeDirectory() stringByAppendingPathComponent:@"Documents/encryptedImage.png"];
    NSData *encryptedData = [NSData dataWithContentsOfFile:imagePath];
    NSData *decryptedData = [RNDecryptor decryptData:encryptedData
                                        withPassword:@"ABC123"
                                               error:&error];
    UIImage *image = [UIImage imageWithData:decryptedData];
```
See, its pretty simple. If you have any questions, let me know in the comments secton below and i will get back to you.
