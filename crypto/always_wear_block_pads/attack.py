import argparse
import json
import struct
import sys
import urllib2
from Crypto.Cipher import AES, XOR

AES_BLOCK_SIZE = 16

ORACLE_URL = 'http://localhost:1337/keyverify?key='


def has_valid_padding(ciphertext, iv):
	res = json.loads(urllib2.urlopen(ORACLE_URL + (iv + ciphertext).encode('hex')).read())
	return res['error'] == 'Invalid license key'

'''
# Padding oracle (offline demo)
def has_valid_padding(ciphertext, iv):
	key = 'this_isnt_a_flag'
	cipher = AES.new(key, AES.MODE_CBC, iv)
	try:
		decrypted = cipher.decrypt(ciphertext)
		last_byte = ord(decrypted[-1])
		if last_byte == 0 or last_byte > AES_BLOCK_SIZE or last_byte > len(decrypted):
			return False
		return all(ord(b) == last_byte for b in decrypted[-last_byte:])
	except:
		return False
'''

def pad(plaintext, blk_len=AES_BLOCK_SIZE):
	pad_len = blk_len - (len(plaintext) % blk_len)
	return plaintext + (chr(pad_len) * pad_len)

def split_into_blocks(buf, blk_len=AES_BLOCK_SIZE):
	blks = []
	for i in xrange(0, len(buf), blk_len):
		blks.append(buf[i:i + blk_len])
	return blks

def decrypt_block(blk, iv):
	iv_new = list(iv)
	decrypted = ['\0'] * len(blk)
	pad = 1

	# Construct iv_new such that XORing it with the decryption of blk
	# yields a block with valid padding (i.e., the last pad bytes
	# of Dec(blk) XOR x = pad)
	for byte in xrange(len(iv_new) - 1, -1, -1):
		# Update previous pad bytes:
		#
		# Dec(blk) ^ iv = Plaintext
		# Dec(blk) ^ iv ^ x = Plaintext ^ x
		# 
		# iv ^ x = iv_new
		# and
		# Plaintext ^ x = pad
		#
		# Therefore:
		# iv_new = iv ^ x
		#        = iv ^ pad ^ Plaintext
		if pad > 1:
			for i in xrange(byte + 1, len(iv_new)):
				iv_new[i] = chr(ord(decrypted[i]) ^ pad ^ ord(iv[i]))

		for guess in xrange(256):
			iv_new[byte] = chr(guess)

			if has_valid_padding(blk, ''.join(iv_new)):
				# Check for false positive (i.e., plaintext ends
				# in 2 2, 3 3 3, 4 4 4 4, etc.)
				if pad == 1:
					iv_new[byte - 1] = chr(ord(iv_new[byte - 1]) ^ 1)
					if not has_valid_padding(blk, ''.join(iv_new)):
						# False positive
						continue

				# Padding is valid! Recover plaintext byte:
				# Dec(blk) ^ iv = Plaintext
				# Dec(blk) ^ iv ^ x = Plaintext ^ x
				# 
				# iv ^ x = guess
				# and
				# Plaintext ^ x = pad
				#
				# Therefore:
				# Plaintext = pad ^ iv ^ guess
				decrypted[byte] = chr(guess ^ ord(iv[byte]) ^ pad)
				pad += 1
				break
	return ''.join(decrypted)

def derive_encryption_iv(blk, encrypted):
	# Calculate IV required to get blk when XORed with Dec(encrypted)
	iv = list('\0' * AES_BLOCK_SIZE)
	for i, b in enumerate(decrypt_block(encrypted, iv)):
		iv[i] = chr(ord(b) ^ ord(blk[i]))
	return ''.join(iv)

def decrypt(ciphertext, iv='\0'*AES_BLOCK_SIZE):
	plaintext = ''
	blks = [iv] + split_into_blocks(ciphertext)

	blk = blks.pop()
	iv = blks.pop()
	while True:
		plaintext = decrypt_block(blk, iv) + plaintext

		# Move to previous block
		if len(blks) > 0:
			blk = iv
			iv = blks.pop()
		else:
			return plaintext[:-ord(plaintext[-1])]  # Strip padding

def encrypt(plaintext):
	plaintext = pad(plaintext)
	ciphertext = ''
	blks = split_into_blocks(plaintext)

	encrypted = 'crypto\'s alright'  # Last "encrypted" block can be anything
	blk = blks.pop()
	while True:
		iv = derive_encryption_iv(blk, encrypted)
		ciphertext = encrypted + ciphertext

		if len(blks) > 0:
			blk = blks.pop()
			encrypted = iv
		else:
			return iv, ciphertext


'''
# Decryption (offline demo)
with open('ciphertext.bin', 'rb') as f:
	print 'Plaintext:', decrypt(f.read())
'''

'''
# Encryption (offline demo)
with open('plaintext.txt', 'rb') as f:
	plaintext = f.read()
	print 'Original plaintext:', plaintext

	iv, ciphertext = encrypt(plaintext)
	print 'IV:', iv.encode('hex')
	print 'Ciphertext:', ciphertext.encode('hex')

	print 'Decrypted:', decrypt(ciphertext, iv)
'''


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Padding oracle attacker for aes-cbc.')
	subparsers = parser.add_subparsers(title='Attack modes', help='Attack mode help')

	dec_parser = subparsers.add_parser('decrypt', help='Decrypt mode help')
	dec_parser.add_argument('-i', '--iv', help='Hex-encoded CBC IV')
	dec_parser.add_argument('-c', '--ciphertext', help='Hex-encoded ciphertext')
	dec_parser.add_argument('-ic', '--iv-and-ciphertext', help='Hex-encoded IV concatenated with ciphertext')
	dec_parser.set_defaults(mode='dec')

	enc_parser = subparsers.add_parser('encrypt', help='Encrypt mode help')
	enc_parser.add_argument('-p', '--plaintext', required=True, help='Plaintext to encrypt')
	enc_parser.set_defaults(mode='enc')

	args = parser.parse_args()
	
	if args.mode == 'dec':
		if args.iv_and_ciphertext:
			iv_and_ciphertext = args.iv_and_ciphertext.decode('hex')
			iv, ciphertext = iv_and_ciphertext[:AES_BLOCK_SIZE], iv_and_ciphertext[AES_BLOCK_SIZE:]
		elif args.iv and args.ciphertext:
			iv = args.iv.decode('hex')
			ciphertext = args.ciphertext.decode('hex')
		else:
			print 'IV and ciphertext must be specified'
			dec_parser.print_help()
			sys.exit(1)

		print 'IV:', iv.encode('hex')
		print 'Ciphertext:', ciphertext.encode('hex')
		print 'Plaintext:', decrypt(ciphertext, iv)

	elif args.mode == 'enc':
		iv, ciphertext = encrypt(args.plaintext)
		print 'Plaintext:', args.plaintext
		print 'IV:', iv.encode('hex')
		print 'Ciphertext:', ciphertext.encode('hex')
		print 'IV+Ciphertext:', (iv + ciphertext).encode('hex')
