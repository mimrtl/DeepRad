import numpy as np
from keras import backend as K

smooth = 1.

def mean_squared_error(y_true, y_pred):
    return K.mean(K.square(y_pred - y_true), axis=-1)

def mean_absolute_error(y_true, y_pred):
    return K.mean(K.abs(y_pred - y_true), axis=-1)

def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)
    
def dice_coef_of_percent_nparray(x,y,pct):
    max_x = np.max(x)
    max_y = np.max(y)
    
    masked_x = (x/max_x) > pct
    masked_y = (y/max_y) > pct
    
    intersection = np.logical_and(masked_x, masked_y)

    return 2. * intersection.sum() / (masked_x.sum() + masked_y.sum())
    
def get_list_of_good_slices(img1,img2):
    good_slices = np.zeros((img1.shape[0],1))
    for curr_slice in range(0, img1.shape[0]):
        img1_slice = img1[curr_slice,:,:]
        img2_slice = img2[curr_slice,:,:]
        
        curr_dice = dice_coef_of_percent_nparray( img1_slice, img2_slice, 0.05 )
        
        if ( curr_dice > 0.6 ):
            good_slices[curr_slice] = 1
            #print( repr(curr_slice) + " good slice " + repr(curr_dice) )
        else:
            good_slices[curr_slice] = 0
            #print( repr(curr_slice) + " bad slice " + repr(curr_dice) )
    
    return good_slices

def resliceToAxial( data ):
    return np.transpose( data, (2,0,1) ) if ( data.ndim == 3 ) else np.transpose( data, (2,0,1,3) )
def resliceToCoronal( data ):
    return np.transpose( data, (1,0,2) ) if ( data.ndim == 3 ) else np.transpose( data, (1,0,2,3) )
def resliceToSagittal( data ):
    return np.transpose( data, (0,1,2) ) if ( data.ndim == 3 ) else np.transpose( data, (0,1,2,3) )
def resliceFromAxial( data ):
    return np.transpose( data, (1,2,0) ) if ( data.ndim == 3 ) else np.transpose( data, (1,2,0,3) )
def resliceFromCoronal( data ):
    return np.transpose( data, (1,0,2) ) if ( data.ndim == 3 ) else np.transpose( data, (1,0,2,3) )
def resliceFromSagittal( data ):
    return np.transpose( data, (0,1,2) ) if ( data.ndim == 3 ) else np.transpose( data, (0,1,2,3) )

def get25DImageGoodSlices( img, channels, good_slices ):
    img2 = get25DImage( img, channels )
    for curr_slice in range(0, img2.shape[0]):
        if ( good_slices[curr_slice] == 0 ):
            img2[curr_slice,:,:,:] = np.zeros( (img.shape[1],img.shape[2],channels ) )
            
    return img2

# get25DImage extracts adjacent slices from a 3D volume
## img <- a 3D image volume of size [nx,ny,nz]
## channels <- the number of adjacent slices to take (should really be an odd number)
## output -> a 4D image of size [nx,ny,nz,channels] reliced such that adjacent slices are grouped together in the 4th dimension
def get25DImage( img, channels ):
    # if 1 image channel, just take the slice and make it '4D'
    if channels == 1:
        curr_img_channels = np.expand_dims(img,3)
    else:
        cen_chan_slice = np.floor( (channels+1)/2 ) - 1
        curr_img_channels = np.zeros( (img.shape[0], img.shape[1],img.shape[2], channels) )
        for curr_slice in range(0, img.shape[0]):
            for chan_slice in range(0, channels):
                act_slice = curr_slice + (cen_chan_slice-channels+1) + chan_slice

                #print( "curr_slice: " + repr(curr_slice) + " chan_slice: " + repr(chan_slice) + " act_slice: " + repr(act_slice) )
                
                if   ( act_slice < 0 ):
                    curr_img_channels[curr_slice,:,:,chan_slice] = np.zeros( (img.shape[1],img.shape[2] ) )
                elif ( act_slice > (img.shape[0]-1 ) ):
                    curr_img_channels[curr_slice,:,:,chan_slice] = np.zeros( (img.shape[1],img.shape[2] ) )
                else:
                    curr_img_channels[curr_slice,:,:,chan_slice] = img[act_slice.astype(int),:,:]
                    
    return curr_img_channels
          
        
# get25DImage2 extracts adjacent slices from a 3D volume
## img <- a 3D image volume of size [nx,ny,nz]
## channels <- the number of adjacent slices to take (should be equal to 1, 3, 5, or 7)
## output -> a 4D image of size [nx,ny,nz,channels] reliced such that adjacent slices are grouped together in the 4th dimension
def get25DImage2( img, channels ):
    # if 1 image channel, just take the slice and make it '4D'
    if channels == 1:
        curr_img_channels = np.expand_dims(img,3)
    # if 3 image channels, set channels as three adjacent slices
    elif channels == 3:
        curr_img_channels = np.zeros( (img.shape[0], img.shape[1],img.shape[2], 3) )
        for curr_slice in range(0, img.shape[0]):
            curr_img_channel1 = img[curr_slice,:,:]
            if ( curr_slice - 1 < 0 ):
                curr_img_channel0 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel2 = img[curr_slice+1,:,:]
            elif ( (curr_slice + 1) > (img.shape[0]-1) ):
                curr_img_channel0 = img[curr_slice-1,:,:]
                curr_img_channel2 = np.zeros( (img.shape[1], img.shape[2]) )
            else:
                curr_img_channel0 = img[curr_slice-1,:,:]
                curr_img_channel2 = img[curr_slice+1,:,:]

            curr_img_channels[curr_slice,:,:,0] = curr_img_channel0
            curr_img_channels[curr_slice,:,:,1] = curr_img_channel1
            curr_img_channels[curr_slice,:,:,2] = curr_img_channel2
    # if 5 image channels, set channels as five adjacent slices
    elif channels == 5:
        curr_img_channels = np.zeros( (img.shape[0], img.shape[1],img.shape[2], 5) )
        for curr_slice in range(0, img.shape[0]):
            curr_img_channel2 = img[curr_slice,:,:]
            if ( curr_slice - 2 < 0 ):
                curr_img_channel0 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel1 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel3 = img[curr_slice+1,:,:]
                curr_img_channel4 = img[curr_slice+2,:,:]
            elif ( curr_slice - 1 < 0 ):
                curr_img_channel0 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel1 = img[curr_slice-1,:,:]
                curr_img_channel3 = img[curr_slice+1,:,:]
                curr_img_channel4 = img[curr_slice+2,:,:]
            elif ( (curr_slice + 2) > (img.shape[0]-1) ):
                curr_img_channel0 = img[curr_slice-2,:,:]
                curr_img_channel1 = img[curr_slice-1,:,:]
                curr_img_channel3 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel4 = np.zeros( (img.shape[1], img.shape[2]) )
            elif ( (curr_slice + 1) > (img.shape[0]-1) ):
                curr_img_channel0 = img[curr_slice-2,:,:]
                curr_img_channel1 = img[curr_slice-1,:,:]
                curr_img_channel3 = img[curr_slice+1,:,:]
                curr_img_channel4 = np.zeros( (img.shape[1], img.shape[2]) )                
            else:
                curr_img_channel0 = img[curr_slice-2,:,:]
                curr_img_channel1 = img[curr_slice-1,:,:]                            
                curr_img_channel3 = img[curr_slice+1,:,:]
                curr_img_channel4 = img[curr_slice+2,:,:]      

            curr_img_channels[curr_slice,:,:,0] = curr_img_channel0
            curr_img_channels[curr_slice,:,:,1] = curr_img_channel1
            curr_img_channels[curr_slice,:,:,2] = curr_img_channel2
            curr_img_channels[curr_slice,:,:,3] = curr_img_channel3
            curr_img_channels[curr_slice,:,:,4] = curr_img_channel4
    # if 7 image channels, set channels as seven adjacent slices
    elif channels == 7:
        curr_img_channels = np.zeros( (img.shape[0], img.shape[1],img.shape[2], 7) )
        for curr_slice in range(0, img.shape[0]):
            curr_img_channel3 = img[curr_slice,:,:]
            if ( curr_slice - 3 < 0 ):
                curr_img_channel0 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel1 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel2 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel4 = img[curr_slice+1,:,:]
                curr_img_channel5 = img[curr_slice+2,:,:]
                curr_img_channel6 = img[curr_slice+3,:,:]                
            if ( curr_slice - 2 < 0 ):
                curr_img_channel0 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel1 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel2 = img[curr_slice-1,:,:]
                curr_img_channel4 = img[curr_slice+1,:,:]
                curr_img_channel5 = img[curr_slice+2,:,:]
                curr_img_channel6 = img[curr_slice+3,:,:]
            elif ( curr_slice - 1 < 0 ):
                curr_img_channel0 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel1 = img[curr_slice-2,:,:]
                curr_img_channel2 = img[curr_slice-1,:,:]
                curr_img_channel4 = img[curr_slice+1,:,:]
                curr_img_channel5 = img[curr_slice+2,:,:]
                curr_img_channel6 = img[curr_slice+3,:,:]                
            elif ( (curr_slice + 3) > (img.shape[0]-1) ):
                curr_img_channel0 = img[curr_slice-3,:,:]
                curr_img_channel1 = img[curr_slice-2,:,:]
                curr_img_channel2 = img[curr_slice-1,:,:]
                curr_img_channel4 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel5 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel6 = np.zeros( (img.shape[1], img.shape[2]) )  
            elif ( (curr_slice + 2) > (img.shape[0]-1) ):
                curr_img_channel0 = img[curr_slice-3,:,:]
                curr_img_channel1 = img[curr_slice-2,:,:]
                curr_img_channel2 = img[curr_slice-1,:,:]
                curr_img_channel4 = img[curr_slice+1,:,:]
                curr_img_channel5 = np.zeros( (img.shape[1], img.shape[2]) )
                curr_img_channel6 = np.zeros( (img.shape[1], img.shape[2]) ) 
            elif ( (curr_slice + 1) > (img.shape[0]-1) ):
                curr_img_channel0 = img[curr_slice-3,:,:]
                curr_img_channel1 = img[curr_slice-2,:,:]
                curr_img_channel2 = img[curr_slice-1,:,:]
                curr_img_channel4 = img[curr_slice+1,:,:]
                curr_img_channel5 = img[curr_slice+2,:,:]
                curr_img_channel6 = np.zeros( (img.shape[1], img.shape[2]) )                
            else:
                curr_img_channel0 = img[curr_slice-3,:,:]
                curr_img_channel1 = img[curr_slice-2,:,:]
                curr_img_channel2 = img[curr_slice-1,:,:]
                curr_img_channel4 = img[curr_slice+1,:,:]
                curr_img_channel5 = img[curr_slice+2,:,:]
                curr_img_channel6 = img[curr_slice+3,:,:]

            curr_img_channels[curr_slice,:,:,0] = curr_img_channel0
            curr_img_channels[curr_slice,:,:,1] = curr_img_channel1
            curr_img_channels[curr_slice,:,:,2] = curr_img_channel2
            curr_img_channels[curr_slice,:,:,3] = curr_img_channel3
            curr_img_channels[curr_slice,:,:,4] = curr_img_channel4
            curr_img_channels[curr_slice,:,:,5] = curr_img_channel5
            curr_img_channels[curr_slice,:,:,6] = curr_img_channel6            
            
    else:
        raise ValueError('Number of channels must be 1, 3, 5, or 7')

    return curr_img_channels
