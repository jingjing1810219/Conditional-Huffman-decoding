# Input your message between 1 to 4, devide by ",",then will start your transmit process
#############################################
# Goal: Encode and decode Huffman codes  
# Name: Ku Jingjing(库敬景)
# Contact: s1810219@jaist.ac.jp
#############################################
import math 
import numpy as np
from math import log2
import random
################################################
# generate stationiary distribution
def Gen_stat_dis(px1, P):
    # generate idenity matrix that has same shape to the transtion matrix
    q = np.eye(P.shape[0])
    q_h = q - P  # Find the matrix Q
    q_h[:, 0] = 1  # Find Q hat by change the first colum of Q to all 1
    q_h_inv = np.linalg.inv(q_h)  # Find the iverse of matrix of Q hat
    s = q[0]  # The vector that all vaule is 0 except the first s*Q_hat = [1,0,0.....] the length of this vector is same as the row length of idenity matrix
    z = np.dot(s, q_h_inv)  # Find the stationary distribution
    return z


#################################################
# generate the each colum's huffman code
def generate_en_mat():
    col_matrix = [['1', '01', '001', '000'], ['01', '001', '000', '1'],
                  ['001', '000', '1', '01'], ['000', '1', '01', '001']]
    return col_matrix


##################################################
# encoding the given message
def encode_hoffman(x):
    encode_list = []  # To save the encode list
    col_matrix = generate_en_mat()  # generate the decoding matrix
    for k in range(len(x)):  # traversal the message list
        if k == 0:  # encoding the first elem in message list
            # find the first colum to encode the first elem in message list
            for i in range(len(col_matrix[0])):
                if x[k] == i+1:
                    encode_list.append(col_matrix[0][i])

        else:
            s = k - 1  # find the previours elem in message for encoding message
            t = x[s] - 1  # find the vaule of the previours message
            # traversal the postion of the message
            for j in range(len(col_matrix[0])):
                if j == x[k] - 1:
                    encode_list.append(col_matrix[t][j])

    return encode_list


####################################################
# decdoing function for huffman code
def decode_Huffman(x_encode, x):
    decode_list = []
    col_matrix = generate_en_mat()
    # if the elem is the first elem ,just find which colum is the most early that have the code, and return the colum num of that.
    for i in range(len(x_encode)):
        if i == 0:
            for j in range(len(col_matrix[0])):
                if col_matrix[0][j] == x_encode[i]:
                    decode_list.append(j+1)

    # by using the pervious decoding list to decode the next message for given encoding message
    for k in range(1, len(x_encode)):
        s = decode_list[k-1]
        for m in range(len(col_matrix[0])):
            if col_matrix[s-1][m] == x_encode[k]:
                decode_list.append(m+1)
    return decode_list


####################################################
#compuate code rate
def code_rate0(x, px1, x_encode):
    sum_c = 0
    for i in range(len(x)):
        sum_c += len(x_encode[i])
        R = sum_c / len(x)
    return R 


####################################################
# compute the entropy rate
def entropy_rate(z, p):
    m = np.zeros((4, 1))
    for i in range(len(p)):
        for j in range(len(p[0])):
            m[i] += -(p[i][j] * log2(p[i][j]))

    return np.dot(z, m)


#######################################################
def check_error(y1, y2):
    if y1 == y2:
        return True
    else:
        return False

#######################################################


px1 = np.array([1/2, 1/4, 1/8, 1/8])
P = np.array([[1/2, 1/4, 1/8, 1/8],
              [1/4, 1/8, 1/8, 1/2],
              [1/8, 1/8, 1/2, 1/4],
              [1/8, 1/2, 1/4, 1/8]])
n = 10

# generate the markov chain
x = []
s = input("Enter your number between 1~4: ")
x = s.split(',')
##############################
for i in range(len(x)):
    x[i] = int(x[i])
for j in range(len(x)):
    if x[j] < 1 or x[j] > 4:
        print("You enter wrong message format!!!")
        break
#############################

z = Gen_stat_dis(px1, P)
encode_list = encode_hoffman(x)
R = code_rate0(x, px1, encode_list)
Hx = entropy_rate(z, P)
x_decode = decode_Huffman(encode_list, x)
print("Your message is: \n", x)
print("Your codewords is: \n", encode_list)
print("Your code rate is: \n", R)
print("Your entropy rate is: \n ", Hx)
print("The decode sequence is: \n", x_decode)
print("Your decoding schme is: \n", check_error(x, x_decode))
