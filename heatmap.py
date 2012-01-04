# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 20:42:25 2011

http://stackoverflow.com/questions/5089030/how-do-i-create-a-radial-cluster-like-the-following-code-example-in-python

colorbar:
    http://matplotlib.sourceforge.net/api/colorbar_api.html
    http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.colorbar
    http://matplotlib.sourceforge.net/examples/api/colorbar_only.html

@author: Xiao Jianfeng
"""

import scipy
import pylab
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as dist
from matplotlib import mpl

#def heatmap(x, colside_colors=None, rowside_colors=None):
def heatmap(x=None, **kwds):
    """
    x is a m by n ndarray, m observations, n genes

    ### kwds:

    dendrogram : ["both"|"row"|"column"|"none"]
    scale      : ["none"|"row"|"column"]
    cmap/colors: pylab.cm.YlGnBu
    cellnote   : None
    notecolor  : "black"
    colside_colors = None,
    rowside_colors = None,
    figsize = (12, 12)

    ## plot labels
    main=None,                                     # NULL,
    xlab=None,                                     # NULL,
    ylab=None,                                     # NULL,
    """

    if not x:
        x = scipy.rand(20, 30)
        #x = scipy.loadtxt("f:/learn/heatmap/tst.data")
        x = x*10

    cmap=pylab.cm.YlGnBu
    norm = mpl.colors.Normalize(vmin=x.min(), vmax=x.max())

    if 'figsize' not in kwds:
        kwds['figsize'] = (12, 12)
    fig = pylab.figure(figsize=kwds['figsize'])

    ## calculate positions for all elements
    # ax1, dendrogram 1, on the left of the heatmap
    [ax1_x, ax1_y, ax1_w, ax1_h] = [0.05,0.1,0.2,0.6]
    width_between_ax1_axr = 0.01
    height_between_ax1_axc = 0.01

    # axr, row side colorbar 
    [axr_x, axr_y, axr_w, axr_h] = [0.31,0.1,0.02,0.6]
    axr_x = ax1_x + ax1_w + width_between_ax1_axr
    axr_y = ax1_y; axr_h = ax1_h
    width_between_axr_axm = 0.01

    # axc, column side colorbar
    [axc_x, axc_y, axc_w, axc_h] = [0.4,0.63,0.5,0.02]
    axc_x = axr_x + axr_w + width_between_axr_axm
    axc_y = ax1_y + ax1_h + height_between_ax1_axc
    height_between_axc_ax2 = 0.01

    # axm, heatmap for the data matrix
    [axm_x, axm_y, axm_w, axm_h] = [0.4,0.1,0.5,0.5]
    axm_x = axr_x + axr_w + width_between_axr_axm
    axm_y = ax1_y; axm_h = ax1_h
    axm_w = axc_w

    # ax2, dendrogram 2, on the top of the heatmap
    [ax2_x, ax2_y, ax2_w, ax2_h] = [0.3,0.72,0.6,0.2]
    ax2_x = axr_x + axr_w + width_between_axr_axm
    ax2_y = ax1_y + ax1_h + height_between_ax1_axc + axc_h + height_between_axc_ax2
    ax2_w = axc_w

    # axcb
    [axcb_x, axcb_y, axcb_w, axcb_h] = [0.10,0.75,0.15,0.1]

    # Compute and plot left dendrogram.
    d1 = dist.pdist(x)
    D1 = dist.squareform(d1)  # full matrix
    # postion = [left(x), bottom(y), width, height]
    ax1 = fig.add_axes([ax1_x, ax1_y, ax1_w, ax1_h], frame_on=True) # frame_on may be False
    Y1 = sch.linkage(D1, method='single')
    #Y = sch.linkage(D1, method='centroid')
    Z1 = sch.dendrogram(Y1, orientation='right')
    #ax1.set_xticks([])
    #ax1.set_yticks([])

    # Plot rowside colors
    # axr --> axes for row side colorbar
    axr = fig.add_axes([axr_x, axr_y, axr_w, axr_h])  # axes for column side colorbar
    dr = scipy.random.randint(low=0, high=5, size=(x.shape[0], 1))
    # there are two methods to generate discrete colormap:
    # matplotlib.cm.get_cmap() and mpl.colros.ListedColormap()
    #cmap_r = mpl.cm.get_cmap('hot', lut=5)
    cmap_r = mpl.colors.ListedColormap(['r', 'g', 'b', 'y', 'w'])
    im_c = axr.pcolor(dr, cmap=cmap_r)
    axr.set_xticks([])
    axr.set_yticks([])

    # Compute and plot top dendrogram.
    d2 = dist.pdist(x.T)
    D2 = dist.squareform(d2)
    ax2 = fig.add_axes([ax2_x, ax2_y, ax2_w, ax2_h], frame_on=True)
    Y2 = sch.linkage(D2, method='single')
    Z2 = sch.dendrogram(Y2)
    #ax2.set_xticks([])
    #ax2.set_yticks([])

    # Plot distance matrix.
    axm = fig.add_axes([axm_x, axm_y, axm_w, axm_h])  # axes for the data matrix
    idx1 = Z1['leaves']
    idx2 = Z2['leaves']
    xt = x[idx1,:]   # xt is transformed x
    xt = xt[:,idx2]
    im = axm.pcolor(xt, cmap=cmap)
    axm.set_xticks([])
    #fix_verts(ax1,1)
    #fix_verts(ax2,0)

    # Add text
    texts_row = [("%s_" % i)*4 for i in range(x.shape[0])]
    texts_col = [("%s_" % i)*4 for i in range(x.shape[1])]
    for i in range(x.shape[0]):
        axm.text(x.shape[1]+0.5, i, texts_row[idx1[i]])
    for i in range(x.shape[1]):
        axm.text(i, -0.5, texts_col[idx2[i]], rotation=270, verticalalignment="top") # rotation could also be degrees

    # Plot colside colors
    # axc --> axes for column side colorbar
    axc = fig.add_axes([axc_x, axc_y, axc_w, axc_h])  # axes for column side colorbar
    dc = scipy.random.randint(low=0, high=5, size=(1, x.shape[1]))
    # there are two methods to generate discrete colormap:
    # matplotlib.cm.get_cmap() and mpl.colros.ListedColormap()
    #cmap_c = mpl.cm.get_cmap('hot', lut=5)
    cmap_c = mpl.colors.ListedColormap(['r', 'g', 'b', 'y', 'w'])
    im_c = axc.pcolor(dc, cmap=cmap_c)
    axc.set_yticks([])

    # Plot colorbar
    axcb = fig.add_axes([axcb_x, axcb_y, axcb_w, axcb_h], frame_on=False)  # axes for colorbar
    cb = mpl.colorbar.ColorbarBase(axcb, cmap=cmap, norm=norm, orientation='horizontal')
    axcb.set_title("colorkey")
    cb.set_label("add label here")
    #axcb.set_xticks([])
    #axcb.set_yticks([])

    pylab.show()

#-----------------------------------------
if __name__ == '__main__':
    heatmap()
