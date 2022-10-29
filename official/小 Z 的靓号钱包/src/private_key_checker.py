# pip install eth-keys

import re
import sys
import eth_keys

hexstr = input('Input your private key: ').strip()
if not re.fullmatch('^0x[0-9a-f]{64}$', hexstr):
    print('Invalid private key format')
    print('Example:', '0x' + '0123456789abcdef' * 4)
    sys.exit(0)
privkey = eth_keys.keys.PrivateKey(bytes.fromhex(hexstr[2:]))
pubkey = privkey.public_key
print('Pubkey =', pubkey)  # uncompressed
addr = pubkey.to_checksum_address()
print('Address =', addr)
if addr == '0xFFfFFfFFfFFf0aa0914DF1465327f33d591B30D8':
    print(open('/flag').read())
else:
    print('Address not match')
