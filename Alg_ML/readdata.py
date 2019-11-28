# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 10:47:10 2019

@author: m1850
"""

import os
import struct
import numpy as np
import cv2
import matplotlib.pyplot as plt

'''
def load_minst(path='',kind = 'train'):
    labels_path = os.path.join(path,"%s-labels.idx1-ubyte"%kind)
    images_path = os.path.join(path,'%s-images.idx3-ubyte'%kind)
    with open(labels_path,'rb') as lbpath:
        magic,n = struct.unpack('>II',lbpath.read(8))
        labels = np.fromfile(lbpath,dtype = np.uint8)
        
    
    with open(images_path,'rb') as imgpath:
        magic,num,rows,cols = struct.unpack('>IIII',imgpath.read(16))
        images = np.fromfile(imgpath,dtype = np.uint8).reshape(len(labels),784)
    return images, labels
'''
def load_minst(path='',kind = 'train'):
    lp = os.path.join(path,'%s-labels.idx1-ubyte'%kind)
    ip = os.path.join(path,'%s-images.idx3-ubyte'%kind)
    with open(lp,'rb') as l:
        l_data = l.read()
        magic = int.from_bytes(l_data[:4],byteorder = 'big',signed = False)
        num = int.from_bytes(l_data[4:8],byteorder = 'big',signed = False)
        labels = [i for i in l_data[8:]]
    with open(ip,'rb') as i:
        i_data  = i.read()
        magic = int.from_bytes(i_data[:4],'big')
        num = int.from_bytes(i_data[4:8],'big')
        nrow = int.from_bytes(i_data[8:12],'big')
        ncol = int.from_bytes(i_data[12:16],'big')
        images = np.array([i for i in i_data[16:]]).reshape(num,nrow,ncol)
        
    return labels,images

os.chdir('D:\yyr\PROJECT\zyh\Alg_ML')
label,image = load_minst()
    
#test
cv2.imwrite('1.jpg',image[0])