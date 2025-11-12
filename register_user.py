# Gera salt e verificador e salva em users.json
import json, os, secrets
from constants import N, g, H
from utils import i2b

DB = "users.json"

def Hx(user: str, password: str, salt: bytes) -> int:
    up = f"{user}:{password}".encode()
    xH = H(H(up), salt)
    return int.from_bytes(xH, "big")

def main():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    salt = secrets.token_bytes(16)
    x = Hx(username, password, salt)
    v = pow(g, x, N)

    data = {}
    if os.path.exists(DB):
        with open(DB, "r", encoding="utf-8") as f:
            data = json.load(f)

    data[username] = {
        "salt": salt.hex(),
        "v": v
    }

    with open(DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Usuário registrado com sucesso.")

if __name__ == "__main__":
    main()
