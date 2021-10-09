#!/usr/bin/env python
# coding: utf-8

# In[1]:


input_text = "0123456789ABCDEF"
key = "133457799BBCDFF1"


# In[2]:


# function that prints bin number in "xxxx xxxx xxxx ..." format
def print_bin(number):
    chunk = 4 #len(number)//8
    bin_str = ""
    for i in range(len(number)//chunk):
        temp = "".join(number[chunk*i:chunk*(i+1)])
        bin_str += " " + temp
    print(bin_str)


# In[3]:


# convert hex to bin (with filling zeros to 4 digit bin number)
def hex_to_bin(number):
    n_bin_lst = []
    for digit in number:
        n_int = int(digit, 16)
        n_bin = bin(n_int)[2:].zfill(4)
        for n in n_bin:
            n_bin_lst.append(n)
    return n_bin_lst


# In[4]:


# convert key and input message to binary form
M = hex_to_bin(input_text)
K = hex_to_bin(key)


# In[5]:


print_bin(M)


# In[6]:


print_bin(K)


# In[7]:


# L = M[:len(M)//2]
# R = M[len(M)//2:]


# In[8]:


PC_1 = [
    57,   49,    41,   33,    25,    17,    9,
    1,    58,    50,   42,    34,    26,   18,
    10,    2,    59,   51,    43,    35,   27,
    19,   11,     3,   60,    52,    44,   36,
    63,   55,    47,   39,    31,    23,   15,
    7,    62,    54,   46,    38,    30,   22,
    14,    6,    61,   53,    45,    37,   29,
    21,   13,     5,   28,    20,    12,    4
]

PC_2 = [
     14,   17,   11,  24,    1,   5,
      3,   28,   15,   6,   21,  10,
     23,   19,  12,    4,   26,   8,
     16,    7,  27,   20,   13,   2,
     41,   52,  31,   37,   47,  55,
     30,   40,  51,   45,   33,  48,
     44,   49,  39,   56,   34,  53,
     46,   42,  50,   36,   29,  32
]


# In[9]:


# function that maps bin number to new number based on positions in array( eg. PC_1)
def permute(array, number):
    result = []
    for idx in array:
        item = number[idx-1]
        result.append(item)
    return result


# In[10]:


K_PC_1 = permute(PC_1, K)


# In[11]:


print_bin(K_PC_1)


# In[12]:


# split key to 2 halves
C_0 = K_PC_1[:len(K_PC_1)//2]
D_0 = K_PC_1[len(K_PC_1)//2:]


# In[13]:


print_bin(C_0)
print_bin(D_0)


# In[14]:


# function that  shifts bin number to left by 1 bit
def shift_L(number):
    first = number[0]
    result = number[1:]
    result.append(first)
    return result


# In[15]:


K_halves = []
current_C = C_0
current_D = D_0
C_n = None
D_n = None

# shift those indexes by 1 bit, others by 2 bits
shift_1 = [1,2,9,16]

# create new key halves (C,D) based on previous shifted
for i in range(1,17):
    if i in shift_1:
        C_n = shift_L(current_C)
        D_n = shift_L(current_D)
    else:
        C_n = shift_L(current_C)
        C_n = shift_L(C_n)
        
        D_n = shift_L(current_D)
        D_n = shift_L(D_n)
    C_D_tup = (C_n, D_n)
    K_halves.append(C_D_tup)
    
    current_C = C_n
    current_D = D_n


# In[16]:


# print halves for each key
for c,d in K_halves:  
    print_bin(c)
    print_bin(d)
    print('------------------------------------')


# In[17]:


K_n_lst = []

# create key by joining halves C and D, perute key with PC_2 table
for c,d in K_halves:
    joined = c + d
    K_n = permute(PC_2, joined)
    K_n_lst.append(K_n)


# In[18]:


# all keys after joining and permutation
for k in K_n_lst:
    print_bin(k)


# In[19]:


IP = [
    58 ,   50 ,  42   , 34   , 26   ,18 ,   10  ,  2,
    60 ,   52 ,  44   , 36   , 28   ,20 ,   12  ,  4,
    62 ,   54 ,  46   , 38   , 30   ,22 ,   14  ,  6,
    64 ,   56  , 48   , 40   , 32   ,24 ,   16  ,  8,
    57 ,   49  , 41   , 33   , 25   ,17 ,    9  ,  1,
    59 ,   51  , 43   , 35   , 27   ,19 ,   11  ,  3,
    61 ,   53  , 45   , 37   , 29   ,21 ,   13  ,  5,
    63 ,   55  , 47   , 39   , 31   ,23 ,   15  ,  7
]


# In[20]:


# permute input message with Initial Permuation (IP) table
M_IP = permute(IP, M)


# In[21]:


# split permutated message into halves
L_0 = M_IP[:len(M_IP)//2]
R_0 = M_IP[len(M_IP)//2:]


# In[22]:


# message
print_bin(M_IP)

# message halves
print_bin(L_0)
print_bin(R_0)


# In[23]:


E = [
    32  ,   1   , 2   ,  3   ,  4  ,  5,
      4  ,   5  ,  6   ,  7  ,   8 ,   9,
      8 ,    9  , 10  ,  11  ,  12 ,  13,
     12  ,  13  , 14  ,  15  ,  16 ,  17,
     16  ,  17  , 18  ,  19  ,  20 ,  21,
     20  ,  21  , 22  ,  23  ,  24 ,  25,
     24  ,  25   ,26  ,  27  ,  28 ,  29,
     28  ,  29   ,30  ,  31  ,  32 ,   1
]


# In[24]:


S_boxes = [
#                             S1
     [14,  4  ,13 , 1 ,  2, 15 , 11,  8,   3, 10 ,  6, 12  , 5 , 9,   0 , 7,
      0 ,15   ,7  ,4  ,14 , 2  ,13,  1 , 10,  6 , 12, 11 ,  9,  5 ,  3 , 8,
      4 , 1  ,14  ,8  ,13 , 6  , 2, 11 , 15 ,12,   9,  7 ,  3, 10 ,  5 , 0,
     15 ,12  , 8  ,2  , 4 , 9  , 1 , 7 ,  5 ,11 ,  3, 14,  10 , 0 ,  6,13],

#                              S2
     [15 , 1 ,  8 ,14 ,  6 ,11 ,  3 , 4 ,  9 , 7  , 2, 13  ,12 , 0 ,  5, 10,
      3 ,13 ,  4 , 7 , 15 , 2  , 8 ,14 , 12  ,0 ,  1, 10  , 6,  9 , 11,  5,
      0, 14 ,  7, 11,  10 , 4 , 13,  1 , 5  ,8 , 12 , 6  , 9 , 3  , 2, 15,
     13 , 8 , 10,  1 ,  3 ,15 ,  4,  2 , 11 , 6 ,  7 ,12  , 0 , 5 , 14,  9],

#                              S3
     [10 , 0 ,  9 ,14 ,  6 , 3 , 15 , 5  , 1, 13,  12 , 7 , 11, 4  , 2 , 8,
     13 , 7  , 0 , 9 ,  3 , 4  , 6, 10  , 2,  8 ,  5, 14 , 12, 11 , 15 , 1,
     13 , 6 ,  4 , 9  , 8, 15  , 3,  0  ,11,  1  , 2, 12  , 5, 10  ,14 , 7,
      1, 10  ,13 , 0  , 6,  9  , 8,  7  , 4 ,15 , 14 , 3 , 11 , 5 ,  2 ,12],

#                              S4
      [7 ,13 , 14,  3 ,  0 , 6  , 9, 10 ,  1,  2 ,  8 , 5  ,11, 12 ,  4 ,15,
     13 , 8 , 11 , 5 ,  6 ,15 ,  0  ,3 ,  4 , 7 ,  2 ,12 ,  1 ,10,  14 , 9,
     10,  6 ,  9 , 0,  12 ,11,   7 ,13 , 15 , 1,   3 ,14,   5 , 2,   8 , 4,
      3, 15,   0  ,6 , 10 , 1,  13,  8  , 9 , 4 ,  5, 11,  12,  7,   2 ,14],

#                              S5
     [2, 12 ,  4,  1 ,  7, 10  ,11,  6 ,  8,  5,   3 ,15 , 13,  0,  14,  9,
     14, 11 ,  2 ,12,   4 , 7 , 13 , 1 ,  5 , 0,  15 ,10,   3 , 9 ,  8,  6,
      4 , 2 ,  1 ,11,  10 ,13 ,  7 , 8 , 15,  9,  12 , 5,   6 , 3 ,  0, 14,
     11 , 8  ,12 , 7,   1 ,14 ,  2, 13 ,  6 ,15,   0 , 9 , 10 , 4 ,  5 , 3],

#                              S6
     [12 ,1  ,10, 15 ,  9 , 2  , 6 , 8  , 0, 13  , 3,  4 , 14 , 7  , 5 ,11,
     10 ,15 ,  4, 2  , 7, 12 ,  9 , 5 ,  6 , 1  ,13, 14 ,  0 ,11 ,  3 , 8,
      9 ,14  ,15 , 5 ,  2 , 8 , 12 , 3 ,  7 , 0  , 4 ,10 ,  1 ,13 , 11  ,6,
      4 , 3 ,  2 ,12 ,  9 , 5 , 15, 10,  11 ,14 ,  1 , 7 ,  6 , 0 ,  8, 13],

#                              S7
      [4, 11 ,  2 ,14 , 15,  0,   8, 13 ,  3, 12 ,  9 , 7 ,  5 ,10  , 6 , 1,
     13,  0 , 11 , 7 ,  4 , 9 ,  1, 10 , 14 , 3 ,  5 ,12 ,  2, 15  , 8 , 6,
      1 , 4  ,11 ,13 , 12 , 3 ,  7, 14 , 10 ,15  , 6 , 8 ,  0,  5  , 9,  2,
      6 ,11 , 13  ,8  , 1  ,4 , 10,  7  , 9  ,5 ,  0 ,15 , 14,  2  , 3, 12],

#                              S8
     [13 , 2  , 8 , 4 ,  6 ,15 , 11 , 1 , 10  ,9  , 3 ,14,   5  ,0 , 12, 7,
      1, 15 , 13  ,8 , 10, 3  , 7 , 4 , 12 , 5 ,  6 ,11 ,  0, 14 ,  9, 2,
      7 ,11 ,  4 , 1 ,  9 ,12 , 14 , 2 ,  0 , 6 , 10, 13 , 15 , 3 ,  5 , 8,
      2 , 1 ,14 , 7 ,  4 ,10  , 8, 13 , 15, 12,   9, 0 ,  3 , 5  , 6, 11]
]


# In[25]:


P = [
     16 ,  7  ,20 , 21,
     29 , 12  ,28 , 17,
      1 , 15  ,23 , 26,
      5 , 18  ,31 , 10,
      2 ,  8  ,24 , 14,
     32 , 27  , 3 ,  9,
     19 , 13  ,30 ,  6,
     22 , 11  , 4 , 25    
]


# In[26]:


IP_1 = [
     40 ,    8 ,  48 ,   16  ,  56 ,  24 ,   64,   32,
    39   ,  7  , 47  ,  15   , 55  , 23  ,  63 ,  31,
    38    , 6  , 46  ,  14   , 54  , 22  ,  62 ,  30,
    37    , 5  , 45  ,  13   , 53  , 21  ,  61 ,  29,
    36    , 4  , 44  ,  12   , 52  , 20  ,  60 ,  28,
    35    , 3  , 43  ,  11   , 51  , 19  ,  59 ,  27,
    34    , 2  , 42  ,  10   , 50  , 18  ,  58 ,  26,
    33    , 1  , 41  ,   9   , 49  , 17  ,  57 ,  25
]


# In[27]:


# function that returns result - xor of 2 binary numbers (A, B)
def bit_xor(A, B):
    result = []
    for a,b in zip(A, B):
        if a == b:
            result.append('0')
        else:
            result.append('1')
    return  result


# In[28]:


# function that uses values from s_box table to map 6-digit bin values to 4-digit ones
def s_box(s_boxes, number):
    splitted_6_lst = []
    chunk = 6
    # split bin number to 6-digit parts
    for i in range(len(number)//chunk):
        temp = number[chunk*i: chunk*(i+1)]
        splitted_6_lst.append(temp)
    
    s_output = []
    
    # for each 6-digit number read row and column id, for calculated coordinates read s_box value 
    for idx, six in enumerate(splitted_6_lst):
        box = s_boxes[idx]
        
        row = str(six[0]) + str(six[-1])
        row_id = int(row, 2)
        
        column = ""
        for d in six[1:-1]:
            column += str(d)
        column_id = int(column, 2)
        
        s_value = box[row_id*16+column_id]
        
#         print("r c s", row_id, column_id, s_value)
        
        four = bin(s_value)[2:].zfill(4)
        four = [str(f) for f in four]
#         print("four", four)
        
        s_output += four
#     print("s out", s_output)

    # permute P array and output of s_box mapping
    s_P = permute(P, s_output)
    
    return s_P


# In[29]:


# caluclate values of f function 
def f(R, K):
    E_R = permute(E, R)
    xored = bit_xor(K, E_R)
    
    boxed = s_box(S_boxes, xored)
    
    return boxed


# In[30]:


prev_L = L_0
prev_R = R_0
encrypted_msg = None

# perform all iterations
for i in range(1,17):
    L_n = prev_R
    K_n = K_n_lst[i-1]

    f_n = f(prev_R, K_n)
    
    R_n = bit_xor(prev_L, f_n)

    prev_L = L_n
    prev_R = R_n
    
    if i == 16:
        reversed_blocks = R_n + L_n
        encrypted_msg = permute(IP_1, reversed_blocks)
        
        print("Last iteration R16")
        print_bin(R_n)
        print("Last iteration L16")
        print_bin(L_n)
        enc_str = "".join(encrypted_msg)
        # convert binary encoded message to hex form
        encrypted_msg = hex(int(enc_str, 2))


# In[31]:


hex_encrypted = encrypted_msg[2:].upper()


# In[32]:


print("Original message: ", input_text)
print("Encrypted message:", hex_encrypted)

