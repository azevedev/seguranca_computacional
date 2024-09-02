# simple menu, able to interact with the code 

import os
import sys
import time
import base64
import aes
import rsa


def main():
  choice = 0
  number = 0
  public_key = 0
  private_key = 0
  while choice != 5:
    print("1. Encrypt/Decrypt")
    print("2. Generate RSA Keys")
    print("3. Encrypt with RSA Keys")
    print("4. Decrypt with RSA Keys")
    print("5. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
      print("Choose a mode to encrypt: ")
      print("1. EBC mode")
      print("2. CTR mode")
      mode = int(input(""))
      print("How many rounds?")
      rounds = int(input(""))
      print("Choose a key:")
      print("Do you want to use a random key? (y/n)")
      random = input("")
      if random == "y":
        key = os.urandom(16)
      else:
        key = input("Enter your key of choice:")

      print("Do you want to encrypt a file? (y/n)")
      hasFile = input("")
      file = None
      if hasFile == "y":
        file = input("Enter filename: ")
        with open(file, "rb") as f:
          data = f.read()
      else:
        data = input("Enter message (string) to encrypt: ")
        data = bytes(data, 'utf-8')
      
      print("Counter initial value :")
      counter_initial = int(input(""))
      print("Counter increment value :")
      counter_increment = int(input(""))

      cypher, decrypted = aes.init(key, data, rounds, mode, counter_initial, counter_increment)

      pretty_aes_print(cypher, decrypted, file)

    elif choice == 2:
      number, public_key, private_key = rsa.generate_keys()

      print("Done!")
      print("Public key: ", public_key)
      print("Private key: ", private_key)
      print("Number n: ", number)

    elif choice == 3:
      print("Enter the message to encrypt: ")
      message = input("")
      result = rsa.encrypt(message, public_key, number)
      print("Encrypted message: ", result)

    elif choice == 4:
      print("Enter the cypher to decrypt: ")
      message = input("")
      result = rsa.decrypt(message, private_key, number)

      print("Decrypted message: ", result)

    elif choice == 5:
      sys.exit()

    else:
      print("Invalid choice")
      time.sleep(1)
      os.system("clear")
      main()

def pretty_aes_print(cypher, decryted, file):
  print("Encrypted data (Base64): ", base64.b64encode(cypher).decode('ASCII')) 
  if(file):
    print("Decrypted file: ", 'out_' + file)
    with open('out_' + file, "wb") as f:
      f.write(decryted)
  else:
    print("Decrypted data (UTF-8): ", decryted.decode("utf-8"))

if __name__ == "__main__":
  main()