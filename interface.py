import json
import rsa
import time
import os
import sys


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    clear()
    print("Escolha uma das opções a seguir:")
    print()
    options = {
        "generate_keys": "Gerar chaves RSA",
        "encrypt_rsa": "Cifrar com rsa",
        "decrypt_rsa": "Decifrar com rsa",
        "end": "sair",
    }

    for i, option in enumerate(options.values()):
        print(f"{i+1} - {option}")
    print()

    while True:
        cmd = input("opção: ")
        try:
            cmd = int(cmd)
            if cmd in range(len(options) + 1):
                break
            else:
                print("Digite um número válido")
        except:
            print("Digite um número válido")

    eval(list(options.keys())[cmd - 1] + "()")


def end():
    print("Encerrando...")
    sys.exit()


def show_steps():
    print("Deseja visualizar os passos?")
    print("S - sim")
    print("N - não")
    print()
    show = False
    while True:
        cmd = input("opção: ")
        if cmd.upper() in ["S", "SIM"]:
            show = True
            break
        elif cmd.upper() in ["N", "NÃO", "NAO"]:
            break
        else:
            print("Digite uma opção válida")
    return show


def generate_keys():
    clear()
    show = show_steps()
    clear()

    if not show:
        print("aguarde...\n")

    pk, sk = rsa.generate_keys(show_steps=show)

    path = "keys"
    if os.path.isdir(path):
        i = 1
        while os.path.isdir(f"keys_{i}"):
            i += 1
        path = f"keys_{i}"

    os.mkdir(path)

    pk_file = open(f"{path}/public_key.txt", "w+")
    n, e = pk
    pk = {"n": n, "e": e}
    pk_file.write(json.dumps(pk))
    # pk_file.write(
    #     f"""
    # *** PUBLIC KEY ***
    # n: {n}
    # e: {e}
    # """
    # )
    pk_file.close()

    sk_file = open(f"{path}/secret_key.txt", "w+")
    n, d = sk
    sk = {"n": n, "d": d}
    sk_file.write(json.dumps(sk))

    # sk_file.write(
    #     f"""
    # *** SECRET KEY ***
    # n: {n}
    # d: {d}
    # """
    # )
    sk_file.close()

    print(f"As chaves foram salvas na pasta {path}")

    print()
    options = {"menu": "voltar", "end": "sair"}

    for i, option in enumerate(options.values()):
        print(f"{i+1} - {option}")
    print()

    while True:
        cmd = input("opção: ")
        try:
            cmd = int(cmd)
            if cmd in range(len(options) + 1):
                break
            else:
                print("Digite um número válido")
        except:
            print("Digite um número válido")

    eval(list(options.keys())[cmd - 1] + "()")


def encrypt_rsa():
    clear()

    path = "keys"
    try:
        with open(f"{path}/public_key.txt") as pk_file:
            pk = json.load(pk_file)
        print(f"Chave pública encontrada em {path}/public_key.txt")
    except:
        print(f"A chave pública não foi localizada em {path}/public_key.txt!")
        print()
        options = {"menu": "voltar", "end": "sair"}

        for i, option in enumerate(options.values()):
            print(f"{i+1} - {option}")
        print()

        while True:
            cmd = input("opção: ")
            try:
                cmd = int(cmd)
                if cmd in range(len(options) + 1):
                    break
                else:
                    print("Digite um número válido")
            except:
                print("Digite um número válido")

        eval(list(options.keys())[cmd - 1] + "()")

    pk = pk["n"], pk["e"]
    print()
    plain_text = input("Digite a mensagem que será cifrada: ")

    plain_text_hash, encrypted_base64 = rsa.encrypt(plain_text, pk)

    encrypted_file = open(f"encrypted_with_rsa.txt", "w+")
    encrypted_dict = {
        "hash": plain_text_hash,
        "encrypted_base64": str(encrypted_base64),
    }
    encrypted_file.write(json.dumps(encrypted_dict))
    encrypted_file.close()

    print()
    print("Arquivo com mensagem cifrada criado em encrypted_with_rsa.txt")

    print()
    options = {"menu": "voltar", "end": "sair"}

    for i, option in enumerate(options.values()):
        print(f"{i+1} - {option}")
    print()

    while True:
        cmd = input("opção: ")
        try:
            cmd = int(cmd)
            if cmd in range(len(options) + 1):
                break
            else:
                print("Digite um número válido")
        except:
            print("Digite um número válido")

    eval(list(options.keys())[cmd - 1] + "()")


def decrypt_rsa():
    clear()
    path = "keys"
    try:
        with open(f"{path}/secret_key.txt") as sk_file:
            sk = json.load(sk_file)
        print(f"Chave privada encontrada em {path}/secret_key.txt")
    except:
        print(f"A chave privada não foi localizada em {path}/secret_key.txt!")
        print()
        options = {"menu": "voltar", "end": "sair"}

        for i, option in enumerate(options.values()):
            print(f"{i+1} - {option}")
        print()

        while True:
            cmd = input("opção: ")
            try:
                cmd = int(cmd)
                if cmd in range(len(options) + 1):
                    break
                else:
                    print("Digite um número válido")
            except:
                print("Digite um número válido")

        eval(list(options.keys())[cmd - 1] + "()")

    sk = sk["n"], sk["d"]

    try:
        with open("encrypted_with_rsa.txt") as encrypted_file:
            encrypted_dict = json.load(encrypted_file)
        print(f"Arquivo com mensagem cifrada encontrado em encrypted_with_rsa.txt")
    except:
        print(
            f"Arquivo com mensagem cifrada não foi encontrado em encrypted_with_rsa.txt!"
        )
        print()
        options = {"menu": "voltar", "end": "sair"}

        for i, option in enumerate(options.values()):
            print(f"{i+1} - {option}")
        print()

        while True:
            cmd = input("opção: ")
            try:
                cmd = int(cmd)
                if cmd in range(len(options) + 1):
                    break
                else:
                    print("Digite um número válido")
            except:
                print("Digite um número válido")

        eval(list(options.keys())[cmd - 1] + "()")

    plain_text_hash, encrypted_base64 = (
        encrypted_dict["hash"],
        encrypted_dict["encrypted_base64"],
    )

    compared_hash, decrypted = rsa.decrypt(encrypted_base64, sk, plain_text_hash)

    print()
    if compared_hash:
        print("Mensagem não foi corrompida!")
    else:
        print("Mensagem foi corrompida!")

    print()
    print(f"Menssagem: {decrypted}")

    print()
    options = {"menu": "voltar", "end": "sair"}

    for i, option in enumerate(options.values()):
        print(f"{i+1} - {option}")
    print()

    while True:
        cmd = input("opção: ")
        try:
            cmd = int(cmd)
            if cmd in range(len(options) + 1):
                break
            else:
                print("Digite um número válido")
        except:
            print("Digite um número válido")

    eval(list(options.keys())[cmd - 1] + "()")


menu()
