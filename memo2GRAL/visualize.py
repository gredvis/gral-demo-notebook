import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import glob

def vis_field(dom,conc_field):
    '''
    dom = dictionary containing xmin, xmax, dx, ymin, ymax, ymin, dy
    
    conc_field = array containing the concentration at each cell
    '''
    lon = np.arange(dom['xmin'], dom['xmax'], dom['dx'])
    lat = np.arange(dom['ymin'], dom['ymax'], dom['dy'])

    levels =np.linspace(0,np.amax(conc_field),100)
    cmap = cm.jet

    fig, ax = plt.subplots(figsize = (12,8))
    
    im = ax.contourf(lon, lat, conc_field, 
                        cmap = cmap,
                        levels = levels, 
                        vmin= 0, 
                        vmax = np.amax(conc_field), 
                        alpha= 0.9)
    ax.grid(linewidth =0.5, linestyle= 'dotted', alpha = 0.75)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.title('Dispersion')

    ##############################################################
    # Colorbar customization
    #############################################################

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size = '5%', pad = 0.10)
    fig.colorbar(im, cax =cax)

    plt.tight_layout()
    plt.show()   
    return ax

def vis_allfield(dom,conc_field):
    lon = np.arange(dom['xmin'], dom['xmax'], dom['dx'])
    lat = np.arange(dom['ymin'], dom['ymax'], dom['dy'])

    levels =np.linspace(0,np.amax(conc_field),100)
    cmap = cm.jet

    fig, ax = plt.subplots(figsize = (12,8))


    # ims is a list of lists, each row is a list of artists to draw in the
    # current frame; here we are animating three artists, the contour and 2 
    # annotatons (title), in each frame
    ims = []

    for i in range(len(conc_field)):
        im = ax.contourf(lon, lat, conc_field[i,:,:], 
                        cmap = cmap,
                        levels = levels, 
                        vmin= 0, 
                        vmax = np.amax(conc_field), 
                        alpha= 0.9)
        ax.grid(linewidth =0.5, linestyle= 'dotted', alpha = 0.75)

        add_arts = im.collections
        text = 'Dispersion={0!r}'.format(i+1)
        # te = ax.text(90, 90, text)
        an = ax.annotate(text, xy=(0.45, 1.05), xycoords='axes fraction')
        ims.append(add_arts + [an])


    ########################################################################
    # colorbar customization
    ########################################################################

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size = '5%', pad = 0.05)
    fig.colorbar(im, cax =cax)

    ########################################################################
    # Animation of figure
    ani = animation.ArtistAnimation(fig, ims)


    # Uncomment the next two line to save animation into .mp4 file
    FFwriter = animation.FFMpegWriter()
    ani.save('basic_animation.mp4', writer = FFwriter)

    return ax
