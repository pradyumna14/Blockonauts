import binascii

hex_data = "9834998439843943984"   # sample hex data

byte_data = binascii.unhexlify(hex_data)

decoded_text = byte_data.decode('utf-8', errors='ignore')

print(decoded_text)
