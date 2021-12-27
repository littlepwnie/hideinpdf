import base64
import re
import sys
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import PyPDF2 as pypdf


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
		return base64.b64encode(string)
	else:
		return base64.b64encode(string.encode())

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def hideFile(fn, pdfname):

	b64fn = b64enc(fn)

	data = readFile(fn)
	b64data = b64enc(data)

	# object of AES class
	passwd = input("Password: ")
	aes = AESCipher(passwd)

	encfn = aes.encrypt(b64fn.decode())
	encdata = aes.encrypt(b64data.decode())
	
	datatowrite = "*"*3+ encfn.decode()+ "|"*3+ encdata.decode()+ "*"*3

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
		hidden_data = re.findall(r'\*\*\*(.*?)\*\*\*', data)[0]

		encfileName = hidden_data.split("|||")[0]
		encfileData = hidden_data.split("|||")[1]

		passwd = input("Password: ")
		aes = AESCipher(passwd)

		encfn = aes.decrypt(encfileName)
		encdata = aes.decrypt(encfileData)

		decrFileName = base64.b64decode(encfn).decode("ascii")
		decrData = base64.b64decode(encdata)
		

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