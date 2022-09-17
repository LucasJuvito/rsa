import random
import time
import hashlib
import base64
import math

"""PARTE 1"""
# Função que gera chave pública e chave privada
def generate_keys(show_steps=False):
    """Retorna uma tupla com uma chave pública (n,e) e uma chave privada (n,d)"""
    # Gerar p primo com 1024 bits
    if show_steps:
        print("Gerando p ideal com 1024 bits...")
    i = 0
    st = time.time()
    while True:
        i += 1
        p = random.randrange(2**1023, 2**1024)
        if is_prime(p, 20):
            break
    et = time.time()
    if show_steps:
        print(f"Tentativas = {i}")
        print(f"Tempo gasto: {et-st} segundos\n")

    # Gerar q primo com 1024 bits
    if show_steps:
        print("Gerando q ideal com 1024 bits...")
    i = 0
    st = time.time()
    while True:
        i += 1
        q = random.randrange(2**1023, 2**1024)
        if is_prime(q, 20):
            break
    et = time.time()
    if show_steps:
        print(f"Tentativas = {i}")
        print(f"Tempo gasto: {et-st} segundos\n")

    st = time.time()
    n = p * q
    et = time.time()
    if show_steps:
        print("Calculado n")
        print(f"Tempo gasto: {et-st} segundos\n")
    # phi_n é a Função totiente/phi de Euler aplicada em n, que é a quantidade
    # de números menores que n em que o máximo divisor comum com n é igual a 1,
    # a quatidade de números menores que n que são co-primos a ele
    st = time.time()
    phi_n = (p - 1) * (q - 1)
    et = time.time()
    if show_steps:
        print("Calculado phi de Euler de n")
        print(f"Tempo gasto: {et-st} segundos\n")

    # Gerar e tal que phi_n, e sejam primos entre si, co-primos
    if show_steps:
        print("Gerando e ideal...")
    i = 0
    st = time.time()
    while True:
        i += 1
        e = random.randrange(2, phi_n)
        if gcd(e, phi_n) == 1:
            break
    et = time.time()
    if show_steps:
        print(f"Tentativas = {i}")
        print(f"Tempo gasto: {et-st} segundos\n")

    # Calcular d tal que d*e = 1 mod phi_n
    st = time.time()
    d = pow(e, -1, phi_n)
    et = time.time()
    if show_steps:
        print("Calculado d")
        print(f"Tempo gasto: {et-st} segundos\n")

    # print(f"n = {n}")
    # print()
    # print(f"phi_n = {phi_n}")
    # print()
    # print(f"e = {e}")
    # print()
    # print(f"d = {d}")
    # print()
    pk, sk = (n, e), (n, d)
    return pk, sk


"""PARTE 2"""

"""PARTE 3"""


def calculate_hash(data):
    data = str(data)
    data = str.encode(data)
    return hashlib.sha3_256(data).hexdigest()


def to_base64(data):
    data = str(data)
    data = str.encode(data)
    return base64.b64encode(data)


def from_base64(encoded):
    data = base64.b64decode(encoded)
    return data.decode()


def encrypt_rsa(m, pk):
    n, e = pk

    c = power(m, e, n)

    return c


def encrypt(m, pk):
    plain_text_hash = calculate_hash(m)
    m = string_to_decimal(m)
    encrypted = encrypt_rsa(m, pk)
    encrypted_base64 = to_base64(encrypted)
    return plain_text_hash, encrypted_base64


"""PARTE 4"""


def decrypt_rsa(c, sk):
    n, d = sk

    m = power(c, d, n)

    return m


def decrypt(encrypted_base64, sk, plain_text_hash):
    encrypted_base64 = str.encode(encrypted_base64[2 : len(encrypted_base64) - 1])
    encrypted = int(from_base64(encrypted_base64))
    decrypted = decrypt_rsa(encrypted, sk)
    decrypted = decimal_to_string(decrypted)
    compared_hash = plain_text_hash == calculate_hash(decrypted)

    return compared_hash, decrypted


""" Funções auxiliares """
# Função que calcula o máximo divisor comum entre dois números
def gcd(x, y):
    while y:
        x, y = y, x % y
    return abs(x)


# função que calcula exponenciação modular (x^y) % p
def power(x, y, p):
    """Retorna o resultado de (x^y) % p"""
    res = 1

    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p

        y = y >> 1
        x = (x * x) % p

    return res


# Teste de Miller-Rabin
def miller_rabin_test(d, n):
    """Retorna False se n é composto ou retorna True se n é provavelmente primo. n é o número a ser testado e d é um número ímpar tal que d*2r = n-1 para algum r>=1"""

    a = 2 + random.randint(1, n - 4)

    x = power(a, d, n)

    if x == 1 or x == n - 1:
        return True

    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False
        if x == n - 1:
            return True

    return False


# Função que define se um número é primo ou não
def is_prime(n, k):
    """Retorna False se n é composto ou True se n é provavelmente primo. n é o número a ser testado e k a quatidade de testes em cima de n, quanto maior o k, maior a precisão"""

    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        if miller_rabin_test(d, n) == False:
            return False

    return True


def string_to_decimal(text: str):
    text_bytes = text.encode()
    text_hex = text_bytes.hex()
    text_int = int(text_hex, 16)
    return text_int


def decimal_to_string(number: int):
    number_hex = hex(number)[2:]
    number_bytes = bytes.fromhex(number_hex)
    number_str = number_bytes.decode()
    return number_str


if __name__ == "__main__":
    pk, sk = generate_keys(True)

    m = 123
    print(f"m = {m}")
    hash_antes = calculate_hash(m)

    c = encrypt_rsa(m, pk)
    print(f"c = {c}")
    c = to_base64(c)
    print(f"c base64 = {c}")
    c = int(from_base64(c))
    print(f"c = {c}")

    m_d = decrypt_rsa(c, sk)
    print(f"m_decrypt = {m_d}")

    hash_depois = calculate_hash(m_d)

    print(f"hash é o mesmo? {hash_antes == hash_depois}")
