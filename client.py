# Cliente SRP
import json, socket, secrets
from constants import N, g, H
from utils import pad, k_param, u_value, KDF, m1, m2

HOST, PORT = "127.0.0.1", 5000

def Hx(user: str, password: str, salt: bytes) -> int:
    up = f"{user}:{password}".encode()
    xH = H(H(up), salt)
    return int.from_bytes(xH, "big")

def main():
    I = input("Username: ").strip()
    p = input("Password: ").strip()

    N_len = (N.bit_length() + 7) // 8
    a = secrets.randbelow(N - 1) or 1
    A = pow(g, a, N)

    with socket.create_connection((HOST, PORT)) as s:
        # Envia I e A
        s.sendall(json.dumps({"I": I, "A": str(A)}).encode())

        # Recebe s e B
        msg = json.loads(s.recv(8192).decode())
        if "err" in msg:
            print("Erro:", msg["err"])
            return
        salt = bytes.fromhex(msg["s"])
        B = int(msg["B"])
        if B % N == 0:
            print("Erro: B invalido")
            return

        # Calcula k, u, x, S, K
        k = k_param(N_len)
        u = u_value(A, B, N_len)
        x = Hx(I, p, salt)

        gx = pow(g, x, N)
        base = (B - (k * gx) % N) % N
        if base == 0:
            print("Erro: base inválida")
            return
        exp = (a + u * x) % (N - 1)
        S = pow(base, exp, N)
        K = KDF(S)

        # Provas M1 e M2
        M1_cli = m1(A, B, K, N_len)
        s.sendall(json.dumps({"M1": M1_cli.hex()}).encode())

        msg = json.loads(s.recv(8192).decode())
        if "err" in msg:
            print("Erro:", msg["err"])
            return
        M2_srv = bytes.fromhex(msg["M2"])
        if M2_srv != m2(A, M1_cli, K, N_len):
            print("Erro: M2 inválido")
            return

        print("Autenticação SRP concluída com sucesso.")
        print("K (hex):", K.hex())

if __name__ == "__main__":
    main()
