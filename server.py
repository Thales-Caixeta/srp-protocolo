# Servidor SRP
import json, socket, secrets
from constants import N, g
from utils import i2b, pad, k_param, u_value, KDF, m1, m2

HOST, PORT = "127.0.0.1", 5000
DB = "users.json"

def load_user(i: str):
    with open(DB, "r", encoding="utf-8") as f:
        db = json.load(f)
    if i not in db:
        return None
    u = db[i]
    return bytes.fromhex(u["salt"]), int(u["v"])

def handle(conn):
    N_len = (N.bit_length() + 7) // 8

    # Recebe I e A
    msg = json.loads(conn.recv(8192).decode())
    I = msg["I"]
    A = int(msg["A"])
    if A % N == 0:
        conn.sendall(b'{"err":"A invalido"}')
        return

    user = load_user(I)
    if user is None:
        conn.sendall(b'{"err":"user not found"}')
        return
    s, v = user

    # Gera b, k, B
    b = secrets.randbelow(N - 1) or 1
    k = k_param(N_len)
    B = (k * v + pow(g, b, N)) % N
    if B % N == 0:
        conn.sendall(b'{"err":"B invalido"}')
        return

    # Envia s e B
    conn.sendall(json.dumps({"s": s.hex(), "B": str(B)}).encode())

    # Calcula u, S, K
    u = u_value(A, B, N_len)
    S = pow((A * pow(v, u, N)) % N, b, N)
    K = KDF(S)

    # Recebe M1 e valida
    msg = json.loads(conn.recv(8192).decode())
    M1_cli = bytes.fromhex(msg["M1"])
    M1_srv = m1(A, B, K, N_len)
    if M1_cli != M1_srv:
        conn.sendall(b'{"err":"M1 invalido"}')
        return

    # Envia M2
    M2_srv = m2(A, M1_srv, K, N_len)
    conn.sendall(json.dumps({"ok": True, "M2": M2_srv.hex()}).encode())

    print(f"[OK] Sessão autenticada: {I}")

def main():
    with socket.create_server((HOST, PORT), reuse_port=False) as srv:
        print(f"Servidor SRP ativo em {HOST}:{PORT}")
        while True:
            conn, _ = srv.accept()
            with conn:
                handle(conn)

if __name__ == "__main__":
    main()
