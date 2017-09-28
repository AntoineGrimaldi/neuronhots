import numpy as np
import matplotlib
from pylab import *
from mpl_toolkits.mplot3d import Axes3D


def dispo(pola,nb_center=None):
    if nb_center is None : nb_center =1

    if nb_center*pola >= 8:
        dispo = (((nb_center*pola)//8 )+1,8)
    else :
        dispo = (nb_center,pola)
    return dispo


def DisplaySurface3D(Surface,nb_polarities,angle=(20,90)):
    mini = np.amin(Surface)-0.01
    maxi = np.max(Surface)+0.01
    cNorm = matplotlib.colors.Normalize(vmin=mini-0.1, vmax=maxi+0.1)
    cmapo = colormaps()[2]

    idx=0
    nb_center = Surface.shape[0]
    if len(Surface.shape) == 2:
        area = int(Surface.shape[1]/nb_polarities)
        Surface = Surface.reshape((nb_center,nb_polarities,area))
    else :
        area = int(Surface.shape[2])

    size = int(np.sqrt(area))
    R = int((size-1)/2)
    subplotpars = matplotlib.figure.SubplotParams(left=0., right=1., bottom=0., top=1., wspace=0, hspace=0)
    X,Y = np.meshgrid(np.arange(-R,R+1),np.arange(-R,R+1))#,indexing='ij')
    disp = dispo(nb_polarities,nb_center)
    #fig = plt.figure(figsize=(disp[1]*3,disp[0]*3))
    fig = plt.figure(figsize=(12,12*disp[0]/disp[1]),subplotpars=subplotpars)
    for idx_surf,each_surf in enumerate(Surface):
        for idx_pol, pol_surf in enumerate(each_surf):
            ax = fig.add_subplot(disp[0],disp[1],idx+1, projection='3d')
            final = pol_surf.reshape((size,size),order='F')
            surf = ax.plot_surface(X, Y,final , rstride=1, cstride=1,
                           cmap=cmapo, norm = cNorm,
                           linewidth=0, antialiased=True)

            ax.set_zlim(mini, maxi)
            ax.view_init(angle[0],angle[1])
            axe = np.linspace(-R,R,5).astype(int)
            plt.yticks(axe)
            plt.xticks(axe)
            ax.tick_params(labelsize=6)
            ax.set_title('Cluster {0}, polarity {1}'.format(idx_surf,idx_pol),fontsize= 10)
            idx=idx+1


def DisplaySurface2D(Surface,nb_polarities):
    subplotpars = matplotlib.figure.SubplotParams(left=0., right=1., bottom=0., top=1., wspace=0.1, hspace=0.2)
    nb_center = Surface.shape[0]#len(ClusterCenter)

    if len(Surface.shape) == 2:
        area = int(Surface.shape[1]/nb_polarities)
        Surface = Surface.reshape((nb_center,nb_polarities,area))
    else :
        area = int(Surface.shape[2])
    disp = dispo(nb_polarities,nb_center)
    #fig, axs = plt.subplots(nb_cluster, nb_polarities, figsize=(10, 10*nb_cluster/nb_polarities), subplotpars=subplotpars)
    fig = plt.figure(figsize=(12,12*disp[0]/disp[1]),subplotpars=subplotpars)
    dim_patch = int(np.sqrt(area))
    idx=0
    for idx_center, each_center in enumerate(Surface):
        for idx_pol, surface in enumerate(each_center):
            ax = fig.add_subplot(disp[0],disp[1],idx+1)
            #ax = axs[idx_center][idx_pol]
            #ax = fig.add_subplot(12, 12, idx + 1)
            #cmax = np.max(np.abs(surface))
            cmin = 0
            cmax = 1
            ax.imshow(surface.reshape((dim_patch,dim_patch)), cmap=plt.cm.gray_r, vmin=cmin, vmax=cmax,
                    interpolation='nearest')
            ax.set_xticks(())
            ax.set_yticks(())
            ax.set_title('Cl {0} - Pol {1}'.format(idx_center,idx_pol),fontsize= 8)
            idx=idx+1

def GenerateAM(Event,Cluster,ImageSize, mode='separate'):
    nb_cluster = Cluster.nb_cluster
    if mode == 'separate':
        activation_map = np.zeros((nb_cluster,ImageSize[0],ImageSize[1]))
    elif mode == 'global':
        activation_map = np.zeros(ImageSize)
    else :
        raise KeyError('the mode argument is not valid')
    for idx_event,ev in enumerate(Event.polarity) :
        address_int = Event.address[idx_event,:]
        x,y = address_int[0],address_int[1]

        if mode == 'global' :
            activation_map[x,y]= ev+1
        else :
            for i in range(nb_cluster):
                activation_map[i,x,y] = 0
            try :
                activation_map[ev,x,y] = 1
            except IndexError :
                print(ev,idx_event)
    return activation_map

def DisplayAM(activation_map):
    subplotpars = matplotlib.figure.SubplotParams(left=0., right=1., bottom=0., top=1., wspace=0.1, hspace=0.2)
    nb_map = activation_map.shape[0]#len(ClusterCenter)
    disp = dispo(nb_map)
    fig = plt.figure(figsize=(10,10*disp[0]/disp[1]),subplotpars=subplotpars)
    idx=0
    for idx_map, each_map in enumerate(activation_map):
        ax = fig.add_subplot(disp[0],disp[1],idx+1)
        cmin = 0
        cmax = 1
        ax.imshow(each_map, cmap=plt.cm.gray_r, vmin=cmin, vmax=cmax,
                interpolation='nearest')
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title('Map Cluster {0}'.format(idx_map),fontsize= 8)
        idx=idx+1