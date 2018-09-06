import base64
import binascii
import os
import struct
import zipfile

from Crypto.Cipher import AES, XOR

SECRET_FILE = 'secret.txt'
GIF_HEADER = 'GIF89a'
GIF_COMMENT_HEADER = '\x21\xfe'
GIF_COMMENT_TRAILER = '\x00'
PNG_HEADER = '\x89PNG\r\n\x1a\n'
PNG_ANC_BLOCK_TYPE = 'maTt'
AES_KEY = 'this_isnt_a_flag'
AES_BLOCK_SIZE = 16

def derive_transform_iv(src_blk, dst_blk, key):
	# Determine the IV required to encrypt `src_blk` to `dst_blk` using
	# AES-128-CBC with `key`. Assumes src_blk and dst_blk are one block
	# in size (128 bits/16 bytes)
	cipher = AES.new(key, AES.MODE_CBC, '\0' * AES_BLOCK_SIZE)
	dec = cipher.decrypt(dst_blk)
	return XOR.new(src_blk).encrypt(dec)

def padding(size, blk_len):
	pad_len = blk_len - (size % blk_len)
	return chr(pad_len) * pad_len

def jpg_to_png(src, dst, out_path, key):
	src_img = None
	with open(src, 'rb') as jpg:
		src_image = jpg.read()
		src_image += padding(len(src_image), AES_BLOCK_SIZE)

	# The magic
	src_block0 = src_image[:AES_BLOCK_SIZE]
	dst_block0 = PNG_HEADER + struct.pack('>I4s', len(src_image) - len(src_block0), PNG_ANC_BLOCK_TYPE)
	iv = derive_transform_iv(src_block0, dst_block0, key)

	encrypted = ''

	# Add source
	cipher = AES.new(key, AES.MODE_CBC, iv)
	encrypted += cipher.encrypt(src_image)

	crc = binascii.crc32(encrypted[len(PNG_HEADER) + 4:])  # Skip header and chunk size
	encrypted += struct.pack('>I', crc & 0xffffffff)

	# Add destination
	with open(dst, 'rb') as png:
		png.seek(len(PNG_HEADER))  # Skip
		encrypted += png.read()

	encrypted += padding(len(encrypted), AES_BLOCK_SIZE)

	with open(out_path, 'wb') as out:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		out.write(cipher.decrypt(encrypted))
	return iv

def gif_to_html(src, dst, out_path, comment=None):
	html = '--><img/><script>'

	# Add ROT13 decoder/image loader
	html += '(x=>(document.getElementsByTagName("img")[0].src='
	html += 'String.fromCharCode(...atob(x).split("")'
	html += '.map(x=>(x.charCodeAt(0)-0xd)%0xff))))('

	with open(dst, 'rb') as img:
		b64 = 'data:image/jpeg;base64,' + base64.b64encode(img.read())
		b64 = [chr(ord(x) + 13) for x in b64]  # ROT13
		b64 = base64.b64encode(''.join(b64))
		html += '"%s"' % b64

	html += ')</script>';

	with open(src, 'rb') as gif:
		with open(out_path, 'wb') as out:
			out.write(gif.read(len(GIF_HEADER)))  # Skip

			# Replace canvas size with HTML comment (ignored by most readers anyway)
			out.write('<!--')
			gif.read(4)

			# Rest of GIF header
			flags = ord(gif.read(1))
			out.write(chr(flags))
			out.write(gif.read(2))

			# Global color table
			if flags & 0x80:
				gctf_len = (1 << ((flags & 7) + 1)) * 3
				out.write(gif.read(gctf_len))

			if comment:
				out.write(GIF_COMMENT_HEADER)
				out.write(struct.pack('B', len(comment)))
				out.write(comment)
				out.write(GIF_COMMENT_TRAILER)

			out.write(gif.read())
			out.write(html)

def create_zip(img_path, out_path):
	with open(SECRET_FILE, 'w') as f:
		f.write(binascii.hexlify(AES_KEY))

	with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
		z.write('begin.txt')
		z.write(SECRET_FILE)

	with open(out_path, 'ab') as out:
		with open(img_path, 'rb') as img:
			out.write(img.read())

if __name__ == '__main__':
	# 1) Create JPEG that becomes PNG when encrypted
	jpg_in = 'hacking-2.jpg'
	png_in = 'hacking-3.png'
	jpg_out = '%s.jpg' % jpg_in
	iv = jpg_to_png(jpg_in, png_in, jpg_out, AES_KEY)

	# 2) Hide JPEG from (1) in GIF, with a text comment block containing the AES IV
	gif_in = 'hacking-1.gif'
	gif_out = '%s.gif.html' % gif_in
	gif_to_html(gif_in, jpg_out, gif_out, binascii.hexlify(iv))

	# 3) Create a ZIP containing the AES key and append the JPEG from (2) to it
	zip_out = 'Challenge.zip'
	create_zip(gif_out, zip_out)

	# 4) Cleanup
	os.remove(jpg_out)
	os.remove(gif_out)
	os.remove(SECRET_FILE)
