import numpy as np

'''
AES - Advanced Encryption Standard

key - 128 bits
text - 128 bits

key and text --> Convert to matrices of size 4x4 with each element containing 1 Byte (8 bits)


1. Encrytion:
1.1 Add Round Key - XOR key and text matrices
1.2 Substitute Bits - Taking first 4 bits of text as row number and last 4 bits as column number,
    each element of the text matrix to mapped to an element in the S-Box.
1.3 Shift Rows - Shift left the rows of the text matrix with the rown number of times.
1.4 Mix Columns - Perform matrix multiplication in golias field with a matrix.
1.5 Add Round key
    + 9 * ( Substitute Keys + Shift Rows + Mix Columns + Add Round key)
    + Substitute Keys + Shift Rows + Add Round Key


2. Decryption
2.1 Add Round Key - XOR key and text matrices
2.2 Inverse Substitute Bits - Taking first 4 bits of text as row number and last 4 bits as column number,
    each element of the text matrix to mapped to an element in the Inverse S-Box.
2.3 Inverse Shift Rows - Shift right the rows of the text matrix with the rown number of times.
2.4 Inverse Mix Columns - Perform matrix multiplication in golias field with a matrix.
2.5 Add Round key
    + 9 * ( Inverse Substitute Keys + Inverse Shift Rows + Inverse Mix Columns + Add Round key)
    + Inverse Substitute Keys + InverseShift Rows + Add Round Key

'''





Sbox = (
    '63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76',
    'CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0',
    'B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15',
    '04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75',
    '09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84',
    '53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF',
    'D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8',
    '51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2',
    'CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73',
    '60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB',
    'E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79',
    'E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08',
    'BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A',
    '70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E',
    'E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF',
    '8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16',
)
    
InvSbox = (
    '52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB',
    '7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB',
    '54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E',
    '08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25',
    '72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92',
    '6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84',
    '90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06',
    'D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B',
    '3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73',
    '96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DF', '6E',
    '47', 'F1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B',
    'FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4',
    '1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F',
    '60', '51', '7F', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF',
    'A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'C8', 'EB', 'BB', '3C', '83', '53', '99', '61',
    '17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D',
)


eTable =(
     '01', '03', '05', '0F', '11', '33', '55', 'FF', '1A', '2E', '72', '96', 'A1', 'F8', '13', '35',
     '5F', 'E1', '38', '48', 'D8', '73', '95', 'A4', 'F7', '02', '06', '0A', '1E', '22', '66', 'AA',
     'E5', '34', '5C', 'E4', '37', '59', 'EB', '26', '6A', 'BE', 'D9', '70', '90', 'AB', 'E6', '31',
     '53', 'F5', '04', '0C', '14', '3C', '44', 'CC', '4F', 'D1', '68', 'B8', 'D3', '6E', 'B2', 'CD',
     '4C', 'D4', '67', 'A9', 'E0', '3B', '4D', 'D7', '62', 'A6', 'F1', '08', '18', '28', '78', '88',
     '83', '9E', 'B9', 'D0', '6B', 'BD', 'DC', '7F', '81', '98', 'B3', 'CE', '49', 'DB', '76', '9A',
     'B5', 'C4', '57', 'F9', '10', '30', '50', 'F0', '0B', '1D', '27', '69', 'BB', 'D6', '61', 'A3',
     'FE', '19', '2B', '7D', '87', '92', 'AD', 'EC', '2F', '71', '93', 'AE', 'E9', '20', '60', 'A0',
     'FB', '16', '3A', '4E', 'D2', '6D', 'B7', 'C2', '5D', 'E7', '32', '56', 'FA', '15', '3F', '41',
     'C3', '5E', 'E2', '3D', '47', 'C9', '40', 'C0', '5B', 'ED', '2C', '74', '9C', 'BF', 'DA', '75',
     '9F', 'BA', 'D5', '64', 'AC', 'EF', '2A', '7E', '82', '9D', 'BC', 'DF', '7A', '8E', '89', '80',
     '9B', 'B6', 'C1', '58', 'E8', '23', '65', 'AF', 'EA', '25', '6F', 'B1', 'C8', '43', 'C5', '54',
     'FC', '1F', '21', '63', 'A5', 'F4', '07', '09', '1B', '2D', '77', '99', 'B0', 'CB', '46', 'CA',
     '45', 'CF', '4A', 'DE', '79', '8B', '86', '91', 'A8', 'E3', '3E', '42', 'C6', '51', 'F3', '0E',
     '12', '36', '5A', 'EE', '29', '7B', '8D', '8C', '8F', '8A', '85', '94', 'A7', 'F2', '0D', '17',
     '39', '4B', 'DD', '7C', '84', '97', 'A2', 'FD', '1C', '24', '6C', 'B4', 'C7', '52', 'F6', '01',
)

lTable = (
 '11', '00', '19', '01', '32', '02', '1A', 'C6', '4B', 'C7', '1B', '68', '33', 'EE', 'DF', '03',
 '64', '04', 'E0', '0E', '34', '8D', '81', 'EF', '4C', '71', '08', 'C8', 'F8', '69', '1C', 'C1',
 '7D', 'C2', '1D', 'B5', 'F9', 'B9', '27', '6A', '4D', 'E4', 'A6', '72', '9A', 'C9', '09', '78',
 '65', '2F', '8A', '05', '21', '0F', 'E1', '24', '12', 'F0', '82', '45', '35', '93', 'DA', '8E',
 '96', '8F', 'DB', 'BD', '36', 'D0', 'CE', '94', '13', '5C', 'D2', 'F1', '40', '46', '83', '38',
 '66', 'DD', 'FD', '30', 'BF', '06', '8B', '62', 'B3', '25', 'E2', '98', '22', '88', '91', '10',
 '7E', '6E', '48', 'C3', 'A3', 'B6', '1E', '42', '3A', '6B', '28', '54', 'FA', '85', '3D', 'BA',
 '2B', '79', '0A', '15', '9B', '9F', '5E', 'CA', '4E', 'D4', 'AC', 'E5', 'F3', '73', 'A7', '57',
 'AF', '58', 'A8', '50', 'F4', 'EA', 'D6', '74', '4F', 'AE', 'E9', 'D5', 'E7', 'E6', 'AD', 'E8',
 '2C', 'D7', '75', '7A', 'EB', '16', '0B', 'F5', '59', 'CB', '5F', 'B0', '9C', 'A9', '51', 'A0',
 '7F', '0C', 'F6', '6F', '17', 'C4', '49', 'EC', 'D8', '43', '1F', '2D', 'A4', '76', '7B', 'B7',
 'CC', 'BB', '3E', '5A', 'FB', '60', 'B1', '86', '3B', '52', 'A1', '6C', 'AA', '55', '29', '9D',
 '97', 'B2', '87', '90', '61', 'BE', 'DC', 'FC', 'BC', '95', 'CF', 'CD', '37', '3F', '5B', 'D1',
 '53', '39', '84', '3C', '41', 'A2', '6D', '47', '14', '2A', '9E', '5D', '56', 'F2', 'D3', 'AB',
 '44', '11', '92', 'D9', '23', '20', '2E', '89', 'B4', '7C', 'B8', '26', '77', '99', 'E3', 'A5',
 '67', '4A', 'ED', 'DE', 'C5', '31', 'FE', '18', '0D', '63', '8C', '80', 'C0', 'F7', '70', '07'
)

Rcon = ['01','02','04','08','10','20','40','80','1B','36']

mixMatrix=(
    '02','03','01','01',
    '01','02','03','01',
    '01','01','02','03',
    '03','01','01','02'
)

invMixMatrix=(
   '0e','0b','0d','09',
   '09','0e','0b','0d',
   '0d','09','0e','0b',
   '0b','0d','09','0e'
)

def mixColumns(matrix):
    result=np.zeros((4,4),dtype='str')
    temp=0
    for i in range (0,4):
        for j in range (0,4):
            for k in range (0,4):
                temp=temp^int(product(matrix[i,k],mixMatrix[k,j]),16)
                result[i,j] = format(temp,'x')
    return matrix

def product(c,d):
    [x,y]=c[0],c[1]
    [a,b]=d[0],d[1]
    e=int(lTable[int(x,16),int(y,16)],16)+int(lTable[int(b,16),int(b,16)],16)
    if e>255:
            e=e-255
    e=format(e,'x')
    f=int(e[0],16)
    if len(e)==1:
        g=0
    else:
        g=int(e[1],16)
    result=str(eTable[f,g])
    return result

def invMixColumns(matrix):
    result=np.zeros((4,4),dtype='str')
    temp=0
    for i in range (0,4):
        for j in range (0,4):
            for k in range (0,4):
                temp=temp^int(product(matrix[i,k],invMixMatrix[k,j]),16)
                result[i,j] = format(temp,'x')
    return matrix
    
def gFunction(key,n):
    key=np.roll(key,-1,axis=1)
    key=subBytes(key)
    temp=int(key[0,0],16)
    temp = temp^ Rcon[n]
    temp=format(temp,'x')
    key[0,0]=temp
    return key

def addRoundKey(matrix,key):
    for i in range (0,4):
        for j in range (0,4):
            a=int(matrix[i,j],16)
            b=int(key[i,j],16)
            c=a^b
            c=format(c,'x')
            if len(c)<2:
                c='0'+c
            matrix[i,j]=c
    return matrix

def shiftRows(x):
    for i in range(1, 4):
        x[i] = np.append(x[i, i:], x[i, :i])
    return x

def invShiftRows(x):
    for i in range(1,4):
        x[i]=np.append(x[i,-i:],x[i,:-i])
    return x

def subBytes(matrix):
    for i in range (0,4):
        for j in range (0,4):
            [x,y]=[matrix[i,j][0],matrix[i,j][1]]
            temp=Sbox[int(x,16),int(y,16)]
            matrix[i,j]=temp
    return matrix

def invSubBytes(matrix):
    for i in range (0,4):
        for j in range (0,4):
            [x,y]=[matrix[i,j][0],matrix[i,j][1]]
            temp=InvSbox[int(x,16),int(y,16)]
            matrix[i,j]=temp
    return matrix

def charToHex(string):
    hexOfString=[]
    for i in string:
        temp=format(ord(i),'x')
        if len(temp)<2:
            temp='0'+temp
        hexOfString.append(temp)
    
    return hexOfString

def hexToChar(hexa):
    char=''
    for i in hexa:
        char=char+chr(int(i, 16))

    return char

def textToMatrix(text):
    
    text=charToHex(text)
    matrix=np.array(text)
    matrix=np.reshape(matrix,(4,4), order='F')
    return matrix

def matrixToText(matrix):
    text=''
    matrix=np.reshape(matrix,(1,16),order='F')
    matrix=list(matrix)[0]
    text=hexToChar(matrix)
    return text


Sbox=np.array(Sbox,dtype='str')
Sbox=np.reshape(Sbox,(16,16))

InvSbox=np.array(InvSbox,dtype='str')
InvSbox=np.reshape(InvSbox,(16,16))

mixMatrix=np.array(mixMatrix,dtype='str')
mixMatrix=np.reshape(mixMatrix,(4,4))

invMixMatrix=np.array(invMixMatrix,dtype='str')
invMixMatrix=np.reshape(invMixMatrix,(4,4))

eTable=np.array(eTable,dtype='str')
eTable=np.reshape(eTable,(16,16))

lTable=np.array(lTable,dtype='str')
lTable=np.reshape(lTable,(16,16))

for i in range (0,len(Rcon)):
    Rcon[i]=int(Rcon[i],16)

def bagOfKeys(key):
    purse=[]
    for i in range(0,10):
        purse.append(gFunction(key,i))
    return purse

def AESencryptAlgo(text,key):
    m=textToMatrix(text)
    keyMat=textToMatrix(key)

    purse=bagOfKeys(keyMat)

    m=addRoundKey(m,keyMat)
    y=m
    key=m
    for i in range (0,9):
        q=subBytes(y)
        s=shiftRows(q)
        y=mixColumns(s)
        key=purse[i]
        y=addRoundKey(y,key)

    t=subBytes(y)
    u=shiftRows(t)
    y=addRoundKey(u,purse[9])
    a=matrixToText(y)
    return a



def AESdecryptAlgo(a,key):
    b=textToMatrix(a)
    
    keyMat=textToMatrix(key)
    purse=bagOfKeys(keyMat)

    b=addRoundKey(b,purse[9])
    v=invShiftRows(b)
    b=invSubBytes(v)
    
    r=b
    for j in range (0,9):
        key=purse[8-j]
        r=addRoundKey(r,key)
        z=invMixColumns(r)
        t=invShiftRows(z)
        r=invSubBytes(t)

    r=addRoundKey(r,keyMat)
    z=matrixToText(r)
    return z

def encoding(text):
    result=[]
    if len(text)==16:
        result.append(text)
    elif len(text)<16:
        text=increment(text)
        result.append(text)
    else:
        L=len(text)
        q=int(L/16)
        for i in range (0,q):
            result.append(text[16*i:16*(i+1)])
        temp=text[16*q:]
        temp=increment(temp)
        result.append(temp)
    return result

def increment(text):
    r=16-len(text)
    for i in range (0,r-1):
        text+=' '
    text+=str(format(r-1,'x'))
    return text

def decrement(text):
    hexRange=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    if text[15] not in hexRange:
        return text
    n=int(text[15],16)
    if n==0:
        return text[0:15]
    count=0
    for i in range (15-n,14):
        if text[i]==' ':
            count+=1
    if count==n-1:
        return text[0:15-n]
    else:
        return text

def decoding(block):
    L=len(block)
    result=''
    for i in range (0,L):
        a=decrement(block[i])
        result += a
    return result

def AES_Encrypt(text,key):
    v=encoding(text)
    c=''
    for i in range (0,len(v)):
        c+=AESencryptAlgo(v[i],key)
    return c

def AES_Decrypt(text,key):
    q=int(len(text)/16)
    temp=[]
    for i in range (0,q):
        temp.append(text[16*i:16*(i+1)])
    stor=[]
    for i in range (0,len(temp)):
        stor.append(AESdecryptAlgo(temp[i],key))
    result=decoding(stor)
    return result
