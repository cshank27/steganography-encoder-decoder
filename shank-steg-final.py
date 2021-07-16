#!/usr/bin/env python3

#Clayton Shank
import os
import hashlib
import png
import base64

PROMPT = """

Welcome. Please choose:

1. Encode message
2. Decode message
3. Exit
"""

#end of message delimeter
Delimeter = "0100100101010101010101100100111101010010010001010011100101000111010101000101010101010110010101000101010100110000010001100100100001010010010100110100010100111101"

def encode_message(message):
    b64 = message.encode('utf8')
    bytes_ = base64.encodebytes(b64)
    bytestring = "".join(["{:08b}".format(x) for x in bytes_])
    bytestring += Delimeter
    return bytestring

#grabs the pixels info from rows
def get_pixels_from_image(fname):
    img = png.Reader(fname).read()
    pixels = img[2]
    return pixels

def encode_pixels_with_message(pixels, bytestring):
    
    enc_pixels = []
    string_i = 0
    for row in pixels:
        enc_row = []
        for i, char in enumerate(row):
            if string_i >= len(bytestring):
                pixel = row[i]
            else:
                if row[i] % 2 != int(bytestring[string_i]):
                    if row[i] == 0:
                        pixel = 1
                    else:
                        pixel = row[i] - 1
                else:
                    pixel = row[i]
            enc_row.append(pixel)
            string_i += 1
        enc_pixels.append(enc_row)
    return enc_pixels

def write_pixels_to_image(pixels, fname):
    png.from_array(pixels, 'RGB').save(fname)


def decode_pixels(pixels):
    bytestring = []
    for row in pixels:
        for c in row:
            bytestring.append(str(c % 2))
    bytestring = ''.join(bytestring)
    message = decode_message_from_bytestring(bytestring)
    return message

def decode_message_from_bytestring(bytestring):
	bytestring = bytestring.split(Delimeter)[0]
	message = int(bytestring, 2).to_bytes(len(bytestring) // 8, byteorder='big')
	message = base64.decodebytes(message).decode("utf8")
	return message

def main():
    print(PROMPT)
    user_inp = ""
    while user_inp not in ("1", "2", "3"):
        user_inp = input("Your choice: ")

    if user_inp == "1":
        in_image = input("Please enter filename of PNG image: ")
        in_message = input("Please insert secret message: ")
        
        print("-ENCODING-")
        pixels = get_pixels_from_image(in_image)
        bytestring = encode_message(in_message)
        epixels = encode_pixels_with_message(pixels, bytestring)
        write_pixels_to_image(epixels, in_image + "-enc.png")
        print("md5 hash of original file: ", hashlib.md5(open(in_image,'rb').read()).hexdigest())
        print("md5 hash of new file: ", hashlib.md5(open(in_image + "-enc.png",'rb').read()).hexdigest())

        f = open(in_image)
        f.seek(0, os.SEEK_END)
        print("Size of the original file is: ", f.tell(), "bytes")
        f.close()
        newf = open(in_image + "-enc.png")
        newf.seek(0, os.SEEK_END)
        print("Size of new file is: ", newf.tell(), "bytes")
        f.close()
    
    elif user_inp == "2":
        in_image = input("Please enter the filename you wish to decode: ")
        print("-DECODING-")
        pixels = get_pixels_from_image(in_image)
        print(decode_pixels(pixels))

if __name__ == "__main__":
    main()
