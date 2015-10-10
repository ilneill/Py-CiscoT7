#!/usr/bin/python
#Filename: Py-CiscoT7.py

#A Python implementation to encrypt and decrypt Cisco Type 7 passwords.

#Ian Neill (c)2014
# - Works with Python v2.7

#ToDo
#1. Add an intuitive GUI.

import random

#GLOBAL CONSTANTS
VERSION = "v1.0.0"
BUILDDATE = "15/06/2014"

#CISCO XOR KEY
#The encryption/decryption key used by Cisco was sourced from the Internet.
#Key text: 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'
KEY_HEX = (0x64,0x73,0x66,0x64,0x3B,0x6B,0x66,0x6F,0x41,0x2C,
            0x2E,0x69,0x79,0x65,0x77,0x72,0x6B,0x6C,0x64,0x4A,
            0x4B,0x44,0x48,0x53,0x55,0x42,0x73,0x67,0x76,0x63,
            0x61,0x36,0x39,0x38,0x33,0x34,0x6E,0x63,0x78,0x76,
            0x39,0x38,0x37,0x33,0x32,0x35,0x34,0x6B,0x3B,0x66,
            0x67,0x38,0x37)

#MAIN PROGRAM
def main():
    global wheel, pointer_l, pointer_n, code_start_l, code_start_n, increment, blocksize
    welcome("Py-CiscoT7 - A Cisco Type 7 Password Encryptor/Decryptor")
    menu_min = 1
    menu_max = 2
    menu_quit = 0
    prg_quit = False
    while not prg_quit:
        #Show the Menu.
        show_menu(menu_min, menu_max, menu_quit)
        #Get the User Choice.
        user_choice = get_choice(menu_min, menu_max, menu_quit)
        #Take action as per selected menu-option.
        if user_choice == menu_quit:
            prg_quit = True
        elif user_choice == 1:
            prg_choice1()
        elif user_choice == 2:
            prg_choice2()
        elif user_choice == 3:
            prg_choice3()
        elif user_choice == 4:
            prg_choice4()
        elif user_choice == 5:
            prg_choice5()
        elif user_choice == 6:
            prg_choice6()
        elif user_choice == 7:
            prg_choice7()
        elif user_choice == 8:
            prg_choice8()
        elif user_choice == 9:
            prg_choice9()
    print "\nGoodbye.\n"
    return
    #End

#FUNCTIONS

#Welcome Function
def welcome(message):
    print message
    print "   Version,", str(VERSION), "-", str(BUILDDATE)
    print
    return

#Show Menu
def show_menu(min, max, quit):
    print (30 * '-')
    print "      P y - C I S C O T 7"
    print "       M A I N - M E N U"
    print (30 * '-')
    print
    if (min <= 1 <= max):
        print " 1. Encrypt a Password"
    if (min <= 2 <= max):
        print " 2. Decrypt a Password"
    if (min <= 3 <= max):
        print " 3. Nothing Yet"
    if (min <= 4 <= max):
        print " 4. Nothing Yet"
    if (min <= 5 <= max):
        print " 5. Nothing Yet"
    if (min <= 6 <= max):
        print " 6. Nothing Yet"
    if (min <= 7 <= max):
        print " 7. Nothing Yet"
    if (min <= 8 <= max):
        print " 8. Nothing Yet"
    if (min <= 9 <= max):
        print " 9. Nothing Yet"
    print
    print " " + str(quit) + ". Exit program"
    print
    print (30 * '-')
    return

#Get User Choice
def get_choice(min, max, quit):
    #Wait for valid choice in while...not.
    choice_is_valid=False
    while not choice_is_valid:
        try:
            choice = int(raw_input("Enter choice [" + str(min) + "-" + str(max) + " or " + str(quit) + "]: "))
            if (min <= choice <= max or choice == quit):
                #A valid choice will terminate the while...not loop.
                choice_is_valid = True
            else:
                print"Error! Only numbers " + str(min) + "-" + str(max) + " or " + str(quit) + " are valid."
        except ValueError as e:
            print ("Error! %s is not a valid choice." % e.args[0].split(": ")[1])
    return(choice)

#Option 1
def prg_choice1():
    #Assume all ok, unless the password encrypt fails.
    ok = True
    print
    pw_plaintext = raw_input("Enter Plaintext Password: ")
    (ok, pw_encrypted) = encrypt_t7(pw_plaintext)
    if ok:
        print "Encrypted Password:", pw_plaintext, "=>", pw_encrypted
    else:
        print "Whoops...", pw_encrypted
    print
    return

#Option 2
def prg_choice2():
    #Assume all ok, unless the password decrypt fails.
    ok = True
    print
    pw_encrypted = raw_input("Enter Encrypted Password: ")
    (ok, pw_plaintext) = decrypt_t7(pw_encrypted)
    if ok:
        print "Plaintext Password:", pw_encrypted, "=>", pw_plaintext
    else:
        print "Whoops...", pw_plaintext
    print
    return

#Option 3
def prg_choice3():
    return

#Option 4
def prg_choice4():
    return

#Option 5
def prg_choice5():
    return

#Option 6
def prg_choice6():
    return

#Option 7
def prg_choice7():
    return

#Option 8
def prg_choice8():
    return

#Option 9
def prg_choice9():
    return

#Encrypt a string
def encrypt_t7(string):
    #A routine to encrypt a string as a Cisco Type 7 password.
    #I read the description of the algorithm and invented this...
    #
    #Each plaintext character is XOR'ed with a different character from a key.
    #The first character used from the key is determined by a random number offset between 0 and 15.
    #This offset is pre-pended to the encrypted password as 2 decimal digits.
    #The offset is incremented as each character of the plaintext password is encrypted.
    #The ASCII code of each encrypted character is appended to the encrypted password as 2 hex digits.
    #
    #A plaintext password has a permissible length of 1 to 25 characters.
    ok = True
    if (1 <= len(string) <= 25):
        #The key offset (or salt) is any integer number between 0 and 15 (inclusive).
        salt = random.randint(0,15)
        #For consistency with the decryption algorithm...
        decrypted = string[0:]
        #Start building the encrypted password - pre-pend the 2 decimal digit offset.
        encrypted = format(salt, "02d")
        #Step through the plaintext password 1 character at a time.
        for counter in range(0, len(decrypted), 1):
            #Get the next of the plaintext character.
            dec_char = ord(decrypted[counter])
            #Get the next character of the key.
            key_char = KEY_HEX[(counter + salt) % 53]
            #XOR the plaintext character with the key character.
            enc_char = dec_char ^ key_char
            #Build the encrypted password one character at a time.
            #The ASCII code of each encrypted character is added as 2 hex digits.
            encrypted += format(enc_char, "02X")
    else:
        ok = False
        encrypted = "Error! Bad password length."
    #Return the status and either the encrypted password, or an error message.
    return(ok, encrypted)

#Decrypt a string
def decrypt_t7(string):
    #A routine to decrypt a string as a Cisco Type 7 password.
    #I read the description of the algorithm and invented this...
    #
    #The first 2 digits of the encrypted password are the offset into a key, and is a decimal number between 0 and 15.
    #The remaining digits are processed in pairs, and are the hex value of the character's ASCII code.
    #Each plaintext character is recovered as each encrypted digit-pair is XOR'ed with a character from the key.
    #The first character used from the key is determined by the offset.
    #The offset is incremented as each pair of digits from the encrypted password is decrypted.
    #
    #An encrypted password has a permissible length of 4 - 52 digits, and always has an even number of digits.
    ok = True
    if ((4 <= len(string) <= 52) and (len(string) % 2) == 0):
        try:
            #Any decimal number between 0 and 15 (inclusive) is valid.
            salt = int(string[:2])
            if salt < 16:
                #The rest of the string is the encrypted password.
                encrypted = string[2:]
                #Start building the decrypted password.
                decrypted = ''
                #Step through the encrypted password 2 digits at a time.
                for counter in range(0, len(encrypted), 2):
                    #Convert the 2 hex digits into the encrypted ASCII character.
                    enc_char = int(encrypted[counter:counter+2],16)
                    #Get the next character of the key.
                    key_char = KEY_HEX[(counter/2 + salt) % 53]
                    #XOR is reversible. Repeating will return the plaintext character.
                    dec_char = enc_char ^ key_char
                    #Build the plaintext password one character at a time.
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
    #Return the the status and either the decrypted password, or an error message.
    return(ok, decrypted)

#Run the program if it is the primary module
if __name__ == '__main__':
    main()

#EOF
