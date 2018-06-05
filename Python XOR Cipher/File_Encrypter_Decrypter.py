def encrypt_file(file):
    
    f = open(file, 'rb')
    content = f.read()
    f.close()

    # Convert bytes into byte array so you can modify each byte in the file
    content = bytearray(content)

    # Key must a value from 0 to 255
    key = 232

    # enumerate(bytearray) returns iterator with indexes and their values of byte array
    # each value of iterator is a decimal number
    for index, value in enumerate(content):
        content[index] = value ^ key

    try:
        f = open(file, 'wb')
        f.write(content)
        f.close()
        print('Encrypted')
    except:
        print('Something went wrong')


def decrypt_file(file):

    f = open(file, 'rb')
    content = f.read()
    f.close()

    # Convert bytes into byte array so you can modify each byte in the file
    content = bytearray(content)

    # Key must a value from 0 to 255
    key = 232

    # enumerate(bytearray) returns iterator with indexes and their values of byte array
    # each value of iterator is a decimal number
    for index, value in enumerate(content):
        content[index] = value ^ key

    try:
        f = open(file, 'wb')
        f.write(content)
        f.close()
        print('Decrypted')
    except:
        print('Something went wrong')

e_or_d = input('Enter E to encrypt or anything else to decrypt file: ')
file_name = input('Enter file location: ')
if e_or_d == 'e' or e_or_d == 'E':
    encrypt_file(file_name)
else:
    decrypt_file(file_name)
