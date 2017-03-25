# -*- coding: utf-8 -*-
"""
Data Augmentation Script
Each method will take in input as a numpy array
Every method may also require additional inputs
@author: dovhaletsd
"""
from skimage import filters
from skimage import img_as_float
from PIL import Image
import numpy as np
from skimage.transform import warp
from skimage.transform import SimilarityTransform
from skimage import transform
from scipy import stats
import PIL
from numpy import array
import skimage

"""
This function will blur the image
Should take the bluz_size as a small random number
"""
def blur(numpy_array, blur_size):
    image = img_as_float(Image.fromarray(numpy_array))
    blurred_image = skimage.filters.gaussian(image, blur_size)
    array_image = np.array(blurred_image)
    array_image = array_image*255
    array_image = np.round(array_image)
    array_image = array_image.astype(np.uint8)
    return array_image

"""
This fucntion will translate the picture in x and y direction
Takes the cut out pixels and puts on the other side
"""
def translation(numpy_array ,x, y):
    tform = SimilarityTransform(translation=(x, y))
    image = Image.fromarray(numpy_array)
    translation_image = warp(image, tform, mode ='wrap')
    array_image = np.array(translation_image)
    array_image = array_image*255
    array_image = np.round(array_image)
    array_image = array_image.astype(np.uint8)
    return array_image

"""
This function roatates the image a cloclwise=1 or counter clockwise=0
Also takes in the degree amount it should rotote and the direction
"""
def rotate(numpy_array, degrees, direction):
    image = img_as_float(Image.fromarray(numpy_array))
    shift_y, shift_x = np.array(image.shape[:2]) / 2.
    tf_rotate = transform.SimilarityTransform(rotation=np.deg2rad(degrees))
    tf_shift = transform.SimilarityTransform(translation=[-shift_x, -shift_y])
    tf_shift_inv = transform.SimilarityTransform(translation=[shift_x, shift_y])
    if direction == 1:    
        image_rotated = transform.warp(image, (tf_shift + (tf_rotate + tf_shift_inv)))
        array_image = np.array(image_rotated)
        array_image = array_image*255
        array_image = np.round(array_image)
        array_image = array_image.astype(np.uint8)
    else:
        image_rotated = transform.warp(image, (tf_shift + (tf_rotate + tf_shift_inv)).inverse)
        array_image = np.array(image_rotated)
        array_image = array_image*255
        array_image = np.round(array_image)
        array_image = array_image.astype(np.uint8)
    return array_image

"""
This function mirrors the image
"""
def mirror(numpy_array):
    fliped_array = np.fliplr(numpy_array)
    image = Image.fromarray(fliped_array)
    return fliped_array

"""
This function adds noise to the image
Checks to make sure no values are out of range of 0-255
Input noise_amount contorls the standard deviattion of distribution
noise_amount 0 = no noise 
"""
def noise(numpy_array, noise_amount):
    my_noise=stats.distributions.norm.rvs(0,noise_amount,size=numpy_array.shape)
    my_noise = np.round(my_noise)
    my_noise = my_noise.astype(np.uint8)
    numpy_array+=my_noise
    np.rint(numpy_array)
    #checking the range of RGB values
    numpy_array = np.clip(numpy_array, 0, 255)
    #noise_image = Image.fromarray(numpy_array)
    return numpy_array

"""
This function will crop the image from the center with a little bit of distortaton
moving the center a few pixels in a new direction
Then it will resize the new image to the origional images size
Takes as input cut_pixels (int) for the size to crop out a border like shape from the image,
center_distortation (tuple(x,y)) integers to manipulate the center
The images need to be square or the parameters in crop and basewidth need to be changed
around to work correctly
"""
def zoom(numpy_arrayy, cut_pixels, xy):
    image = Image.fromarray(numpy_arrayy)
    x, y = xy
    origional_h, origional_w = image.size
    half_the_width = (image.size[0] / 2)+x
    half_the_height = (image.size[1] / 2)+y
    w = (origional_w/2)-cut_pixels
    h = (origional_h/2)-cut_pixels
    new_image = image.crop((half_the_width-w ,half_the_height-h,half_the_width+w,half_the_height+h))
    """
    Resizing it back to the origional size after cropping
    """
    basewidth = origional_w
    wpercent = (basewidth/float(new_image.size[0]))
    hsize = int((float(new_image.size[1])*float(wpercent)))
    new_image = new_image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    new_array = np.array(new_image)
    return new_array
