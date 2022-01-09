from base64 import b64decode, b64encode
import re
import sys
from Crypto import Random
from Crypto.Cipher import AES
from hashlib import md5
import PyPDF2 as pypdf
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def readFile(fn):
	try:
		fBinary = open(fn, 'rb')
	except:
		return None
	try:
		content = fBinary.read()
	except:
		return None
	finally:
		fBinary.close()
	return content

def b64enc(string):
	if type(string) is bytes:
		return b64encode(string)
	else:
		return b64encode(string.encode())

class AESCipher:
    def __init__(self, key):
        self.key = md5(key.encode('utf8')).digest()

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)))

    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)

def hideFile(fn, pdfname):

	b64fn = b64enc(fn)

	data = readFile(fn)
	b64data = b64enc(data)

	# object of AES class
	passwd = input("Password: ")
	aes = AESCipher(passwd)
	
	payload = "*"*3 + b64fn.decode() + "|"*3+ b64data.decode() + "*"*3
	
	datatowrite = aes.encrypt(payload)

	output = pypdf.PdfFileWriter()
	
	pdf=pypdf.PdfFileReader(pdfname)

	for i in range(pdf.getNumPages()):
		page = pdf.getPage(i)
		output.addPage(page)

	with open(pdfname, "wb") as f:
		output.addJS(datatowrite)

		output.addMetadata(pdf.documentInfo)
		output.write(f)

	print("[*] Successfully hidden!")


def unhide(stegpdf):
	
	with open(stegpdf, 'rb') as f:
		
		l = []
		lines = f.readlines()

		for line in lines:
			try:
				l.append(line.decode())
			except:
				continue
		
		data = "".join(l).replace("\n", "").replace(" ", "")

		# Use regex to distinguish file name and file data
		hidden_data = re.findall(r"JavaScript.*JavaScript", data)[0].split("<<")[0].split("(")[1].split(")")[0].replace("'", "")

		hidden_data = hidden_data[1:]

		passwd = input("Password: ")
		aes = AESCipher(passwd)
		b64data = aes.decrypt(hidden_data).decode()
		
		encfileName = b64data.split("|||")[0].replace("***", "")
		encfileData = b64data.split("|||")[1].replace("***", "")

		decrFileName = b64decode(encfileName).decode("ascii")
		decrData = b64decode(encfileData)

		#Write the data to the filename
		new = open(decrFileName,'wb')
		new.write(decrData)
		new.close()

		print("[*] Successfully extracted! File hidden:")

		print("- File name:", decrFileName)
	
def main():
	if (sys.argv[1] == None):
		print("[*] Usage:")
		print("1. hideinpdf.py -h <file to hide> <target PDF>")
		print("2. hideinpdf.py -d <target PDF>")
	elif (sys.argv[1] == "-h"):
		filetohide = sys.argv[2]
		pdftouse = sys.argv[3]
		#hide(filetohide, pdftouse)
		hideFile(filetohide,pdftouse)
	elif (sys.argv[1] == "-d"):
		stegpdf = sys.argv[2]
		unhide(stegpdf)

main()
