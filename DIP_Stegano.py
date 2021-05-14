import cv2

def charToBin(data):
        binary = []
        for i in data:
            binary.append(format(ord(i), '08b'))
        return binary

def modifyPixel(pixel, data):
 
    datalist = charToBin(data)
    lendata = len(datalist)
    W=pixel.shape[0]
    x=0
    y=0
    
    for i in range(lendata):
        
        pixels_range=[]
        while not(len(pixels_range)==3):
            if x==W:
                x=0
                y=y+1
            else:
                pixels_range.append(pixel[x,y])
                x=x+1
        pix=[]
        for c in range (0,3):
            for k in range (0,3):
                pix.append(pixels_range[c][k])


        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
 
        # 3rd value  of 3rd pixel  tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


# Encode data into image
def encode(data,img):
    newimg = img
    w = newimg.shape[0]
    (x, y) = (0, 0)
 
    for pixel in modifyPixel(newimg, data):
        newimg[x, y]=pixel
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
    return newimg

# Decode the data in the image
def decode(img):
    image=img
    data = ''
    W=image.shape[0]
    (x,y)=(0,0)

    while (True):
        pixels_range=[]
        while not(len(pixels_range)==3):
            if x==W:
                x=0
                y=y+1
            else:
                pixels_range.append(image[x,y])
                x=x+1
        pix=[]
        for c in range (0,3):
            for k in range (0,3):
                pix.append(pixels_range[c][k])
        
        
        binstr = ''
 
        for i in pix[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pix[-1] % 2 != 0):
            return data