# Funções auxiliares
from constants import N, g, H, H_int

def i2b(n: int, size: int | None = None) -> bytes:
    b = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
    return b if size is None else b.rjust(size, b"\x00")

def b2i(b: bytes) -> int:
    return int.from_bytes(b, "big")

def pad(x: int, size: int) -> bytes:
    return i2b(x, size)

def k_param(N_len: int) -> int:
    return H_int(i2b(N, N_len), pad(g, N_len))

def u_value(A: int, B: int, N_len: int) -> int:
    return H_int(pad(A, N_len), pad(B, N_len))

def KDF(S: int) -> bytes:
    return H(i2b(S))

def m1(A: int, B: int, K: bytes, N_len: int) -> bytes:
    return H(pad(A, N_len), pad(B, N_len), K)

def m2(A: int, M1: bytes, K: bytes, N_len: int) -> bytes:
    return H(pad(A, N_len), M1, K)
