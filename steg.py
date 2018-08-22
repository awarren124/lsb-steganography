from scipy import misc
import numpy as np
import sys

def loadImage(fileName):
	image = misc.imread(fileName)
	return image

def saveImage(image, fileName):
	misc.imsave(fileName, image)

def encodeText(text, image):

	data = textToBinaryString(text)
	data += "0"*8
	i = 0
	for x in range(len(image)):
		for y in range(len(image[0])):
			for c in range(len(image[0][0])):
				if i > len(data) - 1:
					return image
				byte = "{0:08b}".format(image[x][y][c])
				byte = byte[:-1] + data[i]
				image[x][y][c] = int(byte, 2)
				i += 1
	return image

def decodeText(image):
	binaryText = ""
	i = 0
	for x in range(len(image)):
		for y in range(len(image[0])):
			for c in range(len(image[0][0])):
				byte = "{0:08b}".format(image[x][y][c])
				bit = byte[-1]
				binaryText += bit
				if (i % 8 == 7) and (binaryText[-8:] == "0"*8):
					text = binaryStringToText(binaryText[:-8])
					return text
				i += 1


	return "No null byte found"
def textToBinaryString(text):
	bytesText = int.from_bytes(text.encode(), 'big')
	binaryText = bin(bytesText)
	binaryText = "0"*(len(binaryText)%8) + binaryText[2:]
	return binaryText

def binaryStringToText(binaryText):
	if binaryText[:2] != "0b":
		binaryText = "0b" + binaryText
	intText = int(binaryText, 2)
	text = intText.to_bytes((intText.bit_length() + 7) // 8, 'big').decode()
	return text

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Too few arguments. Use -h for help")

	option = sys.argv[1]

	if option == "-e":
		fileName = sys.argv[2]
		text = sys.argv[3]
		newFileName = sys.argv[4]
		image = loadImage(fileName)
		newImage = encodeText(text, image)
		saveImage(newImage, newFileName)
	elif option == "-d":
		fileName = sys.argv[2]
		image = loadImage(fileName)
		text = decodeText(image)
		print("Text:")
		print(text)
	elif option == "-h":
		print("Encoding: python steg.py -e [original file path] \"[text to encode]\" [new file path]")
		print("Decoding: python steg.py -d [encoded file path]")
	else:
		print("invalid argument(s)")



