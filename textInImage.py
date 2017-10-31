
import binascii
import textwrap
#Kader Ustun- 803263136
#CPSC 353- Text In Image- Steganography


from PIL import Image

def ValueToBit(value, bit):
	value1 = bin(value)
	finalValue = '' 
	for i in range(len(value1)-1):
		finalValue += value1[i]
	finalValue += bit
	return int(finalValue, 2)
	

def PixelOfIndex(pixelNumber, imageSize):
	columns= imageSize[0]
	rows = imageSize[1]
	pixelX = (columns-1) - (pixelNumber//rows)
	pixelY = (rows-1) - (pixelNumber%rows)
	return (pixelX, pixelY)
	

def encodedImage(image, text):
	im = image.load()
	if len(text) >255:
		print("It is too long.")
		return False
	
	stringToBinary = bin(int(binascii.hexlify(text.encode()), 16))
	length = len(stringToBinary) + (3-len(stringToBinary)%3)
	stringToBinary = stringToBinary.zfill(length)
	stringToBinary = stringToBinary.replace('b', '0')
	stringToBinary = stringToBinary.replace('g', '1')
	stringToBinary = stringToBinary.replace('r', '2')
	

	#Storing length of binary in first 11 bits from bottom right
	lengthOfText = bin(length).zfill(11*3)
	lengthOfText = lengthOfText.replace('b', '0')
	lengthOfText = lengthOfText.replace('g','1')
	lengthOfText = lengthOfText.replace('r', '2')
	for i in range(11):
		x,y = PixelOfIndex(i, image.size)
		pixValue = im[x,y]
		im[x,y] = (ValueToBit(pixValue[0], 
		stringToBinary[3*i]), ValueToBit(pixValue[1],
		stringToBinary[3*i+1]), ValueToBit(pixValue[2],
		stringToBinary[3*i+2]))
		

	#Storing the text in the rest of the pixel
	for j in range(len(stringToBinary)//3):	
		k,l= PixelOfIndex(j+11, image.size)
		pixValue = im[k,l]
		im[k,l] =(ValueToBit(pixValue[0],stringToBinary[3*j]),
		ValueToBit(pixValue[1], stringToBinary[3*j+1]),
		ValueToBit(pixValue[2], stringToBinary[3*j+2]))
		#print(im[k,l])

	img.save("modified.png")

	#extracting text  from image
	binaryToString = binascii.unhexlify(stringToBinary)
	print(binaryToString)
	#extracting text length from image

	lengthText = len(binaryToString)	
	print (lengthText)

img= Image.open("cat.jpg")
text = "This is secret message"
encodedImage(img, text)





			