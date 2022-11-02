import z3


def main() -> None:
    # 32 hex digits, 16 bytes
    poly=0x883ddfe55bba9af41f47bd6e0b0d8f8f
    weak_keys = [
        bytes.fromhex('0101010101010101'),
        bytes.fromhex('FEFEFEFEFEFEFEFE'),
        bytes.fromhex('E0E0E0E0F1F1F1F1'),
        bytes.fromhex('1F1F1F1F0E0E0E0E'),
    ]

    assert poly & -1 == poly
    assert poly & 0 == 0

    x = z3.Int('x')
    y = z3.Int('y')
    z3.solve(x > 2, y < 10, x + 2*y == 7)

    # target = int.from_bytes(weak_keys[0])
    # crc = target ^ ((1 << 128) - 1)
    # for _ in range(8):
    #     # solve crc
    #     # Will there be multiple possibilities?
    #     # Uh, we have a problem, there are two things, crc and b to solve.
    #     # Actually what we know is the initial value of crc.
    #     # Can we just stuff everything to z3?
    #     pass
    # bs = [z3.Int(f'b{i}') for i in range(16)]
    # crc = (1 << 128) - 1
    # for b in bs:
    #     crc = crc ^ b
    #     for _ in range(8):
    #         crc = (crc >> 1) ^ (poly & -(crc & 1))
    # z3.solve(crc == int.from_bytes(weak_keys[0]))

    # bs = [z3.BitVec(f'b{i}', 8) for i in range(16)]
    # crc = (1 << 128) - 1
    # for b in bs:
    #     # Type of crc is now BitVec(8)!
    #     crc = crc ^ b
    #     print(crc.sort())
    #     return
    #     for _ in range(8):
    #         # I guess the -1 makes z3 confused.
    #         crc = (crc >> 1) ^ (poly & -(crc & 1))
    # z3.solve(crc == int.from_bytes(weak_keys[0], 'big'))
    # [b2 = 136,
    # b11 = 193,
    # b10 = 166,
    # b6 = 129,
    # b12 = 198,
    # b9 = 203,
    # b1 = 251,
    # b13 = 189,
    # b8 = 51,
    # b3 = 48,
    # b14 = 255,
    # b15 = 148,
    # b7 = 167,
    # b4 = 141,
    # b0 = 170,
    # b5 = 21]

    data = z3.BitVec('data', 128)
    # print((data >> 1).sort())
    # print((data & 1).sort())
    # z3.solve(poly * (data & 1) == poly)
    # z3.solve(poly * (z3.Extract(1, 0, data)) == poly)
    # z3.solve(poly * (z3.Extract(1, 0, data)) == poly)
    # exit()
    # crc = (1 << 128) - 1
    # for i in range(16):
    #     crc = crc ^ ((data >> (i * 8)) & ((1 << 8) - 1))
    #     for _ in range(8):
    #         # crc = (crc >> 1) ^ (poly & -(crc & 1))
    #         crc = (crc >> 1) ^ (poly * (crc & 1))
    # z3.solve(crc == int.from_bytes(weak_keys[0], 'big'))
    # [data = 77910712249349005960810985634603018148]

    crc = z3.BitVecVal((1 << 128) - 1, 128)
    for i in range(16):
        crc = crc ^ z3.LShR(data << (8 * i), 8 * 15)
        for _ in range(8):
            crc = z3.LShR(crc, 1) ^ (poly * (crc & 1))
    crc = crc ^ z3.BitVecVal((1 << 128) - 1, 128)
    z3.solve(crc == z3.BitVecVal(int.from_bytes(weak_keys[0], 'big') << (8 * 8), 128))

    # Let's try forward analysis.
    # crc will xor poly when lsb is 1
    # We can directly tell if xor happened by looking at bit 2 ** 127
    # So we can recover the old crc
    # lsb = crc >> 127
    # old_crc = (((poly if lsb else 0) ^ crc) << 1) | lsb
    # How about xor with b? Both look unconstrained.


if __name__ == "__main__":
    main()
