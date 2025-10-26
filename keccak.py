import sys
import numpy as np

BYTE_LENGTH = 8
PERMUTATION_WIDTHS = [25, 50, 100, 200, 400, 800, 1600]
PARAMETERS = {}

def init(_b=1600):
    if _b not in PERMUTATION_WIDTHS:
        print('Invalid permutation width.')
        sys.exit()
    
    # Инициализация параметров
    PARAMETERS['b'] = _b
    PARAMETERS['w'] = int(_b / 25)
    PARAMETERS['l'] = int(np.log2(PARAMETERS['w']))


def binary_array(byte_string):
    _a = np.array([int(_b) for _b in byte_string], dtype=np.uint8)
    return np.unpackbits(_a)


def hex_digest(_binary_array):
    return ''.join([
        bytes(np.packbits(np.flip(_binary_array[i:i + BYTE_LENGTH]))).hex()
        for i in range(0, len(_binary_array), BYTE_LENGTH)
    ])


def zeros(num):
    return np.zeros(num, dtype=np.uint8)


def concat(*args):
    return np.concatenate((args))


class StateArray:
    def __init__(self, S):
        w = PARAMETERS['w']
        A = np.empty((5, 5, w), dtype=np.uint8)
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    A[x, y, z] = S[w * (5 * y + x) + z]
        self.A = A

    def S(self):
        _plane = [concat(*[self.A[i, j] for i in range(5)]) for j in range(5)]
        return concat(*_plane)

    def theta(self):
        A = self.A
        w = PARAMETERS['w']
        C = np.empty((5, w), dtype=np.uint8)
        D = np.empty((5, w), dtype=np.uint8)

        for x in range(5):
            for z in range(w):
                C[x, z] = np.logical_xor.reduce(A[x, :, z])

        for x in range(5):
            for z in range(w):
                D[x, z] = C[(x - 1) % 5, z] ^ C[(x + 1) % 5, (z - 1) % w]

        for x in range(5):
            for y in range(5):
                for z in range(w):
                    self.A[x, y, z] ^= D[x, z]

    def rho(self):
        A = np.copy(self.A)
        w = PARAMETERS['w']
        (x, y) = (1, 0)
        for t in range(24):
            for z in range(w):
                A[x, y, z] = self.A[x, y, int((z - (t + 1) * (t + 2) / 2)) % w]
            (x, y) = (y, (2 * x + 3 * y) % 5)
        self.A = A

    def pi(self):
        A = np.copy(self.A)
        w = PARAMETERS['w']
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    self.A[x, y, z] = A[(x + 3 * y) % 5, x, z]

    def chi(self):
        A = np.copy(self.A)
        w = PARAMETERS['w']
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    self.A[x, y, z] = A[x, y, z] ^ (
                        (A[(x + 1) % 5, y, z] ^ 1) & A[(x + 2) % 5, y, z])

    def iota(self, ir):
        def rc(t):
            if t % 255 == 0:
                return 1
            R = [1, 0, 0, 0, 0, 0, 0, 0]
            for _ in range(1, t % 255 + 1):
                R = concat([0], R)
                R[0] ^= R[8]
                R[4] ^= R[8]
                R[5] ^= R[8]
                R[6] ^= R[8]
                R = R[:8]
            return R[0]

        A = np.copy(self.A)
        w = PARAMETERS['w']
        l = PARAMETERS['l']
        RC = zeros(w)
        for j in range(l + 1):
            RC[2**j - 1] = rc(j + 7 * ir)
        for z in range(w):
            A[0, 0, z] ^= RC[z]
        self.A = A

    def Rnd(self, ir):
        self.theta()
        self.rho()
        self.pi()
        self.chi()
        self.iota(ir)


def keccak_p(b, nr):
    def _func(S):
        l = PARAMETERS['l']
        A = StateArray(S)
        for ir in range(12 + 2 * l - nr, 12 + 2 * l):
            A.Rnd(ir)
        return A.S()

    init(b)
    return _func


def sponge(f, pad, r):
    b = PARAMETERS['b']

    def _func(N, d):
        P = concat(N, pad(r, len(N)))
        n = int(len(P) / r)
        
        # Инициализация параметров
        c = b - r
        # print(c, " ", r)
        S = zeros(b)
        for i in range(n):
            S = f(np.logical_xor(S, concat(P[i * r:(i + 1) * r], zeros(c))))
        Z = zeros(0)
        while True:
            Z = concat(Z, S[:r])
            if d <= len(Z):
                return Z[:d]

    return _func


def pad10s1(x, m):
    j = (-m - 2) % x
    return concat([1], zeros(j), [1])


def keccak(c):
    init()
    b = PARAMETERS['b']
    l = PARAMETERS['l']
    return sponge(keccak_p(b, 12 + 2 * l), pad10s1, b - c)


def shake_128(M, d):
    return keccak(512)(concat(M, [1, 1, 1, 1]), d)


def sha3(byte_string):
    byte_num = 32
    res = shake_128(binary_array(byte_string), byte_num * BYTE_LENGTH)
    res_hex = hex_digest(res)
    return res_hex
