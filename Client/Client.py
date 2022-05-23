import random
import socket
import sympy

def encrypt(word, key):
    enc = ""
    for letter in word:
        ascii = (ord(letter) + key)
        if ord(letter) <= ord('Z') and ord(letter) >= ord('A'):
            if ascii > ord('Z'):
                ascii = ord('A') - ord('Z') + ascii - 1
        elif ord(letter) <= ord('z') and ord(letter) >= ord('a'):
            if ascii > ord('z'):
                ascii = ord('a') - ord('z') + ascii - 1
        enc += chr(ascii)
    return enc

def isPrimitiveRoot(p, a):
    list = []

    for power in range(1, p):
        list.append(a**power % p)

    for nr in range(1, p):
        if nr not in list:
            return False

    return True

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 3344
    close_connection = False
    p = 7
    a = 3

    if not sympy.isprime(p):
        print("p is not a prime number")

    if not isPrimitiveRoot(p, a):
        print("a is not a primitive root of p")

    #se genereaza Xb
    x_b = random.randint(1, p - 1)
    y_b = a**x_b % p

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    #se trimite Yb
    server.send(bytes(str(y_b), "utf-8"))

    #se primeste Ya
    aux = server.recv(1024)
    aux = aux.decode("utf-8")

    y_b = int(aux)

    #se calculeaza cheia
    key = y_b ** x_b % p


    while not close_connection:

        string = input("Enter string: ")
        if string == 'Close connection':
            close_connection = True
        server.send(bytes(encrypt(string, key), "utf-8"))
