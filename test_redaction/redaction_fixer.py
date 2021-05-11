#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 12:22:42 2021

@author: joshuahewson
"""
import numpy as np
from PIL import Image

class redaction_fixer:
        
    def find_redactions(imarray):
        cursor_shape = (20,20)
        step_shape = (20,20)
        cursor = np.zeros(cursor_shape)
        for x in range(1,int(imarray.shape[0]/step_shape[0])):
            for y in range(1,int(imarray.shape[1]/step_shape[1])):
                loc = (step_shape[0]*x,step_shape[1]*y)
                cursor = imarray[loc[0]:(loc[0]+cursor_shape[0]),loc[1]:(loc[1]+cursor_shape[1])]
                if len(cursor[cursor<10]) >= 0.9 * 3 * len(cursor) * len(cursor[0]):
                    redaction_fixer.remove_redaction(imarray,loc)
        return imarray
    
    def remove_redaction(imarray, loc):
        loc, cursor_shape = redaction_fixer.fit_redaction(imarray, loc)
        redaction_fixer.transform_redaction(imarray, loc, cursor_shape)
        
    def fit_redaction(imarray, loc):
        cursor_shape = (20,2)
        # find left edge
        more_to_find = True
        while more_to_find and loc[1] >  0:
            line_of_pixels = imarray[loc[0]-1,loc[1]:loc[1]+cursor_shape[1]]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.5 * 3 * len(line_of_pixels):
                loc = (loc[0]-1,loc[1])
            else:
                more_to_find = False
        more_to_find = True
        # find top edge
        while more_to_find and loc[0] > 0:
            line_of_pixels = imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]-1]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.5 * 3 * len(line_of_pixels):
                loc = (loc[0],loc[1]-1)
            else:
                more_to_find = False
        # find right edge
        more_to_find = True
        while more_to_find and loc[1] + cursor_shape[1] < len(imarray[1]):
            line_of_pixels = imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]+cursor_shape[1]+1]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.5 * 3 * len(line_of_pixels):
                cursor_shape = (cursor_shape[0],cursor_shape[1]+1)
            else:
                more_to_find = False
                more_to_find = False
        # find bottom edge
        more_to_find = True
        while more_to_find and loc[0] + cursor_shape[0] < len(imarray[0]):
            line_of_pixels = imarray[loc[0]+cursor_shape[0]+1,loc[1]:loc[1]+cursor_shape[1]]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.1 * 3 * len(line_of_pixels):
                cursor_shape = (cursor_shape[0]+1,cursor_shape[1])
            else:
                more_to_find = False
        return loc, cursor_shape
        
    def clear_redaction(imarray, loc, cursor_shape):
        #cursor now position at top left of redaction and shaped to match the redaction
        #now we just need to turn everything in the cursor white (or into a desired character)
        imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]:loc[1]+cursor_shape[1]] = np.ones((cursor_shape[0],cursor_shape[1],3))*255
    
    def transform_redaction(imarray, loc, cursor_shape):
        redaction_fixer.clear_redaction(imarray, loc, cursor_shape)
        redaction_fixer.print_symbols(imarray, loc, cursor_shape, '+')
                
    def print_symbols(imarray, loc, cursor_shape, char):
        font = cursor_shape[0]
        spaces = int(cursor_shape[1]/font)
        if char=='+':
            for i in range(spaces):
                imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]+i*cursor_shape[0]:loc[1]+(i+1)*cursor_shape[0]] = redaction_fixer.plus((cursor_shape[0],cursor_shape[0]))
                
    def plus(shape): 
        line = 5 #lines are set to 5 pixels wide  
        array = np.zeros((shape[0],shape[1],3))
        w_square_shape = (int(shape[0]/2-line/2),int(shape[1]/2-line/2))
        array[0:w_square_shape[0],0:w_square_shape[1]] = np.ones((w_square_shape[0],w_square_shape[1],3))*255
        array[0:w_square_shape[0],shape[1]-w_square_shape[1]:shape[1]] = np.ones((w_square_shape[0],w_square_shape[1],3))*255
        array[shape[0]-w_square_shape[0]:shape[0],0:w_square_shape[1]] = np.ones((w_square_shape[0],w_square_shape[1],3))*255
        array[shape[0]-w_square_shape[0]:shape[0],shape[1]-w_square_shape[1]:shape[1]] = np.ones((w_square_shape[0],w_square_shape[1],3))*255
        return array
        
    def fix_redactions(file):    
        imarray = np.array(file)
        redaction_fixer_array = redaction_fixer.find_redactions(imarray)
        file_new = Image.fromarray(redaction_fixer_array)
        return file_new
        
        
#file = Image.open('high_res/images/page_1.png')        
#file = redaction_fixer.fix_redactions(file)
#file.show()