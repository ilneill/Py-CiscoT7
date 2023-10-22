#!/usr/bin/python


#  A Python v2.7 implementation to encrypt and decrypt Cisco Type 7 passwords.

#  Ian Neill (c)2014 - 2015
#  Revised by Matt Raio 2023

import random
intValue = 0
VERSION = "v1.0.2.1"
BUILDDATE = "10/19/2023"

#  Cisco XOR key.
#  The encryption/decryption key used by Cisco was sourced from the Internet.
#  Key text: 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'
KEY_HEX = (0x64, 0x73, 0x66, 0x64, 0x3B, 0x6B, 0x66, 0x6F, 0x41, 0x2C,
           0x2E, 0x69, 0x79, 0x65, 0x77, 0x72, 0x6B, 0x6C, 0x64, 0x4A,
           0x4B, 0x44, 0x48, 0x53, 0x55, 0x42, 0x73, 0x67, 0x76, 0x63,
           0x61, 0x36, 0x39, 0x38, 0x33, 0x34, 0x6E, 0x63, 0x78, 0x76,
           0x39, 0x38, 0x37, 0x33, 0x32, 0x35, 0x34, 0x6B, 0x3B, 0x66,
           0x67, 0x38, 0x37)


#  Important note from Cisco about passwords
#  =========================================
#  Understanding Enable and Enable Secret Passwords...
#  Each type of password is case sensitive, can contain from 1 to 25 uppercase and lowercase alphanumeric characters,
#  and can start with a numeral.
#  Spaces are also valid password characters; for example, "two words" is a valid password.
#  Leading spaces are ignored, but trailing spaces are recognized.
#
# Taken from: http://www.cisco.com/en/US/docs/ios/preface/usingios.html

# Main Function
def main():
    welcome("Py-CiscoT7 - A Cisco Type 7 Password Encryptor/Decryptor")
    menuMin = 1
    menuMax = 2
    menuQuit = 0
    while True:
        showMenu(menuMin, menuMax, menuQuit)  # Show the menu.
        userChoice = getInteger(0, 0, "Enter choice [%d--%d or %d]: " % (menuMin, menuMax, menuQuit), False)
        # Take action as per selected menu-option.
        if userChoice == menuQuit:
            break  # Leave the while loop.
        elif userChoice == 1:
            pwPlaintext = getValue("Enter Plaintext Password: ").lstrip()
            (ok, pwEncrypted) = encryptT7(pwPlaintext)
            if ok:
                print("Encrypted Password: %s => %s" % (pwPlaintext, pwEncrypted))
            else:
                print("Whoops... %s" % pwEncrypted)
        elif userChoice == 2:
            pwEncrypted = getValue("Enter Encrypted Password: ")
            (ok, pwPlaintext) = decryptT7(pwEncrypted)
            if ok:
                print("Plaintext Password: %s => %s" % (pwEncrypted, pwPlaintext))
            else:
                print("Whoops... %s" % pwPlaintext)
        else:
            print("Error: \"%d\" is not a valid choice!" % userChoice)
    print("\nGoodbye.\n")
    return


# Welcome message
def welcome(message):
    print(message)
    print("   Version, %s, %s" % (VERSION, BUILDDATE))
    return


#  Print the Available Menu Options
def showMenu(minimum, maximum, q):
    print("\n" + 30 * '-')
    print("      P y - C I S C O T 7")
    print("       M A I N - M E N U")
    print(30 * '-' + "\n")
    for i in range(minimum, maximum + 1):
        if i == 1:
            print(" 1. Encrypt a Password")
        elif i == 2:
            print(" 2. Decrypt a Password")
        elif i == 3:
            print(" 3. Nothing Yet")
        elif i == 4:
            print(" 4. Nothing Yet")
        elif i == 5:
            print(" 5. Nothing Yet")
        elif i == 6:
            print(" 6. Nothing Yet")
        elif i == 7:
            print(" 7. Nothing Yet")
        elif i == 8:
            print(" 8. Nothing Yet")
        elif i == 9:
            print(" 9. Nothing Yet")
        else:
            continue
    print("\n %d. Exit program\n" % q)
    print(30 * '-')
    return


# Get a Number From the User
def getInteger(minimum, maximum, message, checkrange=True):
    global intValue
    while True:
        inputValue = getValue(message)
        try:
            intValue = int(inputValue)
        except ValueError:
            print("Error: \"%s\" is not an integer!" % inputValue)
            continue
        if (intValue < minimum or intValue > maximum) and checkrange:
            print("Error: \"%d\" is outside range [%d--%d]!" % (intValue, minimum, maximum))
            continue
        break  # Leave the while loop.
    return intValue


# Get Something From the User
def getValue(message="Enter choice: "):
    while True:
        inputValue = input(message)
        if len(inputValue) == 0:
            print("Error: No value given!")
            continue
        break  # Leave the while loop.
    return inputValue


# Encrypt a String
def encryptT7(string):
    # A routine to encrypt a string as a Cisco Type 7 password.
    # I read the description of the algorithm and invented this...
    #
    # Each plaintext character is XOR'ed with a different character from a key.
    # The first character used from the key is determined by a random number offset between 0 and 15.
    # This offset is pre-pended to the encrypted password as 2 decimal digits.
    # The offset is incremented as each character of the plaintext password is encrypted.
    # The ASCII code of each encrypted character is appended to the encrypted password as 2 hex digits.
    #
    # A plaintext password has a permissible length of 1 to 25 characters.
    ok = True
    if 1 <= len(string) <= 25:
        # The key offset (or salt) is any integer number between 0 and 15 (inclusive).
        salt = random.randint(0, 15)
        # For consistency with the decryption algorithm...
        decrypted = string[0:]
        # Start building the encrypted password - pre-pend the 2 decimal digit offset.
        encrypted = format(salt, "02d")
        # Step through the plaintext password 1 character at a time.
        for counter in range(0, len(decrypted), 1):
            # Get the next of the plaintext character.
            dec_char = ord(decrypted[counter])
            # Get the next character of the key.
            key_char = KEY_HEX[(counter + salt) % 53]
            # XOR the plaintext character with the key character.
            enc_char = dec_char ^ key_char
            # Build the encrypted password one character at a time.
            # The ASCII code of each encrypted character is added as 2 hex digits.
            encrypted += format(enc_char, "02X")
    else:
        ok = False
        encrypted = "Error! Bad password length."
    # Return the status and either the encrypted password, or an error message.
    return ok, encrypted


# Decrypt a String
def decryptT7(string):
    # A routine to decrypt a string as a Cisco Type 7 password.
    # I read the description of the algorithm and invented this...
    #
    # The first 2 digits of the encrypted password are the offset into a key, and is a decimal number between 0 and 15.
    # The remaining digits are processed in pairs, and are the hex value of the character's ASCII code.
    # Each plaintext character is recovered as each encrypted digit-pair is XOR'ed with a character from the key.
    # The first character used from the key is determined by the offset.
    # The offset is incremented as each pair of digits from the encrypted password is decrypted.
    #
    # An encrypted password has a permissible length of 4 - 52 digits, and always has an even number of digits.
    ok = True
    if (4 <= len(string) <= 52) and (len(string) % 2) == 0:
        try:
            # Any decimal number between 0 and 15 (inclusive) is valid.
            salt = int(string[:2])
            if salt < 16:
                # The rest of the string is the encrypted password.
                encrypted = string[2:]
                # Start building the decrypted password.
                decrypted = ''
                # Step through the encrypted password 2 digits at a time.
                for counter in range(0, len(encrypted), 2):
                    # Convert the 2 hex digits into the encrypted ASCII character.
                    enc_char = int(encrypted[counter:counter + 2], 16)
                    # Get the next character of the key.
                    key_char = KEY_HEX[int(counter / 2 + salt) % 53]
                    # XOR is reversible. Repeating will return the plaintext character.
                    dec_char = enc_char ^ key_char
                    # Build the plaintext password one character at a time.2
                    decrypted += chr(dec_char)
            else:
                ok = False
                decrypted = "Error! Bad key offset."
        except ValueError:
            ok = False
            decrypted = "Error! Invalid encryption."
    else:
        ok = False
        decrypted = "Error! Bad password length."
    # Return the the status and either the decrypted password, or an error message.
    return ok, decrypted


# Run the Program if it is the Primary Module
if __name__ == '__main__':
    main()

# EOF
