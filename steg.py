import cv2
import numpy as np
import sys

def get_binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(_), '08b') for _ in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(_, "08b") for _ in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Unsupported image type.")


def encode_data(image, data):
    img = cv2.imread(image)
    img_size = img.shape[0] * img.shape[1] * 3 // 8
    data += "|||||"
    data_bin = get_binary(data)      
    data_len=len(data_bin)
    if len(data_bin) > img_size:
        raise ValueError(
            "[!] Image size is smaller than data to be encoded. Please try again with a bigger image or less data.")
    print("Encoding message in image...")
    i = 0
    for row in img:
        for px in row:
            r, g, b = get_binary(px)
            if i < data_len:
                px[0]=int(r[:-1] + data_bin[i], 2)
                i += 1
            if i < data_len:
                px[1]=int(g[:-1] + data_bin[i], 2)
                i += 1
            if i < data_len:
                px[2]=int(b[:-1] + data_bin[i], 2)
                i += 1
            if i >= data_len:
                break
    return img

def decode(image):
    print("Decoding...")
    img = cv2.imread(image)
    data_bin = ""
    for row in img:
        for px in row:
            r, g, b = get_binary(px)
            data_bin += r[-1]
            data_bin += g[-1]
            data_bin += b[-1]
    all_bytes = [ data_bin[i: i+8] for i in range(0, len(data_bin), 8) ]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "|||||":
            break
    return decoded_data[:-5]


if __name__ == "__main__":
    if len(sys.argv)>1:
        if(sys.argv[1].lower() == 'encode'):
            if(len(sys.argv)>=5):
                image = sys.argv[2]
                target = sys.argv[3]
                message = sys.argv[4]
                cv2.imwrite(target, encode_data(image,message))
            else:
                print('Usage:\n [encode] [inputfile] [targetfile] [message]\n [decode] [inputfile]')
        elif(sys.argv[1].lower() == 'decode'):
            if(len(sys.argv)<4):
                image = sys.argv[2]
                print(f'Message : {decode(image)}')
            else:
                print('Usage:\n [encode] [inputfile] [targetfile] [message]\n [decode] [inputfile]')
        else:
            print('Usage:\n [encode] [inputfile] [targetfile] [message]\n [decode] [inputfile]')
    else:
        print('Usage:\n [encode] [inputfile] [targetfile] [message]\n [decode] [inputfile]')