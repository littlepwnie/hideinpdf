# hideinpdf
**About**
PDF is an interesting file format. Apart from text, a PDF includes information such as fonts, hyperlinks, instructions for printing, images, keywords for search and indexing. PDF document has a specific file structure and it is organized into four parts: header, body, cross reference table and trailer. When generating a PDF from any editor, all our text, images, graphs, styling etc get compiled giving the portable file we can later send to anyone or use anywhere.

Very powerful, very extensible and one of the most widely used types of file, yet so far not extensively used for steganography. This project aims to use PDF files to hide and transport information in plain sight. Specifically, a JS entity is created into the target PDF in which encrypted file data are hidden. This is not visible from a PDF viewer, since there is no actual script to be executed.

Files to hide are encoded to Base64 format, then encrypted with AES using a preshared key between the parties in exchange. Recovering the files is the exact opposite procedure.

**HowTo**

Before downloading, make sure you have Python3 installed (tested on python 3.9) and that pycryptodome (tested on 3.12.0) and PyPDF2 (tested on 1.26.0) are installed. If not
```
pip3 install pycryptodome
pip3 install PyPDF2
```
Then, download the repo, or
```
git clone https://github.com/littlepwnie/hideinpdf.git
```
and finally
```
- To hide a file inside a PDF:
	python3 hideinpdf.py -h <file to hide> <target PDF>

- To recover it back:
	python3 hideinpdf.py -d <target PDF>
```
Tested with hiding .txt, .js, .py, .pdf, .jpg, .png, .mp3, so should work with more as well!

**Special Thanks <3**

@DimosKap @nov3mb3r
