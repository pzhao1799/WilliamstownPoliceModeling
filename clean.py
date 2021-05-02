#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 12:22:42 2021

@author: joshuahewson
"""
import numpy as np
from PIL import Image

class Cleaner:
    
    def clean_redacted(array):
        for x in range(int(array.shape[0]/10)):
            for y in range(int(array.shape[1]/10)):
                pixel = array[x,y]
                if np.sum(pixel) > 400:
                    pixel = [255,0,0]
        return array
        
    def find_redactions(imarray):
        cursor_shape = (20,20)
        step_shape = (20,20)
        cursor = np.zeros(cursor_shape)
        for x in range(1,int(imarray.shape[0]/step_shape[0])):
            for y in range(1,int(imarray.shape[1]/step_shape[1])):
                loc = (step_shape[0]*x,step_shape[1]*y)
                cursor = imarray[loc[0]:(loc[0]+cursor_shape[0]),loc[1]:(loc[1]+cursor_shape[1])]
                if len(cursor[cursor<10]) >= 0.9 * 3 * len(cursor) * len(cursor[0]):
                    # print('redaction found at ' + str(loc))
                    Cleaner.remove_redaction(imarray,loc)
        return imarray
    
    def remove_redaction(imarray, loc):
        cursor_shape = (20,2)
        # find left edge
        more_to_find = True
        while more_to_find:
            line_of_pixels = imarray[loc[0]-1,loc[1]:loc[1]+cursor_shape[1]]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.5 * 3 * len(line_of_pixels):
                loc = (loc[0]-1,loc[1])
            else:
                more_to_find = False
        more_to_find = True
        # find top edge
        while more_to_find:
            line_of_pixels = imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]-1]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.5 * 3 * len(line_of_pixels):
                loc = (loc[0],loc[1]-1)
            else:
                more_to_find = False
        # find right edge
        more_to_find = True
        while more_to_find:
            line_of_pixels = imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]+cursor_shape[1]+1]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.5 * 3 * len(line_of_pixels):
                cursor_shape = (cursor_shape[0],cursor_shape[1]+1)
            else:
                more_to_find = False
                more_to_find = False
        # find bottom edge
        more_to_find = True
        while more_to_find:
            line_of_pixels = imarray[loc[0]+cursor_shape[0]+1,loc[1]:loc[1]+cursor_shape[1]]
            if len(line_of_pixels[line_of_pixels < 10]) >= 0.1 * 3 * len(line_of_pixels):
                cursor_shape = (cursor_shape[0]+1,cursor_shape[1])
            else:
                more_to_find = False
        
        #cursor now position at top left of redaction and shaped to match the redaction
        #now we just need to turn everything in the cursor white (or into a desired character)
        imarray[loc[0]:loc[0]+cursor_shape[0],loc[1]:loc[1]+cursor_shape[1]] = np.ones((cursor_shape[0],cursor_shape[1],3))*255
        
                
        
        
        
# file = Image.open('high_res/images/page_1.png')
# imarray = np.array(file)
# clean_array = clean.find_redactions(imarray)
# file = Image.fromarray(clean_array)
# file.show()

def redact(png_path):
    file = Image.open(png_path)
    imarray = np.array(file)
    clean_array = Cleaner.find_redactions(imarray)
    file = Image.fromarray(clean_array)
    file.save(png_path, 'PNG')

redact("clean_test/page_9.png")