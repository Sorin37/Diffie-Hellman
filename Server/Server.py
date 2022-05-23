import random
import socket
import sympy

def isPrimitiveRoot(p, a):
    list = []

    for power in range(1, p):
        list.append(a**power % p)

    for nr in range(1, p):
        if nr not in list:
            return False

    return True

def decrypt(word, key):
    denc = ""
    for letter in word:
        ascii = (ord(letter) - key)
        if ord(letter) <= ord('Z') and ord(letter) >= ord('A'):
            if ascii < ord('A'):
                ascii = ord('Z') - ord('A') + ascii + 1
        elif ord(letter) <= ord('z') and ord(letter) >= ord('a'):
            if ascii < ord('a'):
                ascii = ord('z') - ord('a') + ascii + 1
        denc += chr(ascii)
    return denc


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 3344
    p = 7
    a = 3
    close_connection = False

    if not sympy.isprime(p):
        print("p is not a prime number")

    if not isPrimitiveRoot(p, a):
        print("a is not a primitive root of p")

    #se genereaza Xa
    x_a = random.randint(1, p - 1)
    y_a = a**x_a % p

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    print("Server online!")
    client, address = server.accept()

    #se primeste y_b
    aux = client.recv(1024)
    aux = aux.decode("utf-8")

    #se trimite y_a
    client.send(bytes(str(y_a), "utf-8"))

    y_a = int(aux)

    #se calculeaza cheia
    key = y_a**x_a % p

    while not close_connection:
        string = client.recv(1024)
        string = string.decode("utf-8")

        print(string)
        print(decrypt(string, key))
        print()

        if 'Close connection' in decrypt(string, key)[0:len('Close connection')]:
            client.close()
            close_connection = True
