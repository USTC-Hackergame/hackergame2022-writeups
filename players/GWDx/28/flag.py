import binascii

string = '666C61677B73654E7061315F3831305F4631726D776172335F353933366165643337367D'

# convert hex to binary representation
binData = binascii.unhexlify(string)
print(binData)
