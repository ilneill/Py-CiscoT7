## Py-CiscoT7

A Python program to encrypt and decrypt Cisco Type 7 passwords.

### Why?
It was a bit of fun, and the algorithm descriptions I found seemed fairly straight forward...

### How Does The Cisco Type 7 Password Algorithm Work?
It is a type of XOR based substitution cipher. 

At a very basic level, each plaintext character is XOR’ed with a character from a key, thus producing the ciphertext character.

#### The algorithm, in more detail:

The key used in the Cisco Type 7 XOR based encryption and decryption:

dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87

##### Encryption
Each plaintext character is XOR'ed with a different character from the key. The first character used from the key is determined by a random number offset between 0 and 15. This offset is pre-pended to the encrypted password as 2 decimal digits. The ASCII code of each encrypted character is appended to the encrypted password as 2 hex digits and the offset is incremented as each character of the plaintext password is encrypted.
A plaintext password has a permissible length of 1 to 25 characters. Spaces are allowed, but not at the beginning.

##### Decryption
The first 2 digits of the encrypted password are the offset into the key and this is decimal number between 0 and 15. The remaining digits are processed in pairs, and are the hex value of the character's ASCII code. Each plaintext character is recovered as each encrypted digit-pair is XOR'ed with a character from the key. The first character used from the key is determined by the offset, and the offset is incremented as each pair of digits from the encrypted password is decrypted.
An encrypted password has a permissible length of 4 - 52 digits, and always has an even number of digits.

### Is it useful?
Only if you want to encrypt or decrypt a Type 7 password for a Cisco router or switch.

### Running
Py-CiscoT7 is a python script. Run from the command line or via IDLE.

### Missing and ToDo
For this CLI version, nothing is outstanding... unless something is spotted.

Perhaps an intuitive GUI would be good?

### Credits
Most of the Internet for help & inspiration.

### License
Public domain - do what you like.
