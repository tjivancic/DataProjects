import numpy as np
from scipy.io import netcdf as nc
import os
import matplotlib.pyplot as plt
import matplotlib.animation as ani

def read_from_ncfolder(infolder, files=False):
    """
    opens a folder full of nc files which are in order when alphabetized
    nc files must each have a 2-d variable 'precip_rate' which holds precipitation valueas at each gridcell
    """
    if not files:
        files = sorted(os.listdir(infolder))
    P = []
    Nt = len(files)
    for i in range(Nt):
        pfile = nc.netcdf_file(infolder + files[i], 'r')
        P.append(pfile.variables['precip_rate'][:])
        pfile.close()
    P=np.array(P)
    return P

def netvalue(P, weight_mask=1):
    """
    computes the total precipitation volume for the entire storm for use when re-aligning the projected storm with the original
    setting weight mask to a 2-d array of weights from 0-1 changes the weight of each cell. This is useful when a non-square control area is needed ie. a watershed
    """
    Nt = P.shape[0]
    runsum = 0
    for i in range(Nt):
        runsum += sum(sum(P[i,:,:]*weight_mask))
    return runsum

def countcells(P):
    """
    counts the number of cells with a precip value across the entire dataset for use when re-aligning the projected storm with the origninal 
    """
    return sum(sum(sum(P>0)))

def allignPrecip(Pold,Pnew, weight_mask=1):
    """
    confirms that the same number of cells have precipitaion values in the projected storm as in the original and that the total precipitaion is the same
    """
    Pflat = Pnew.flatten()
    Pflat.sort()
    lowval = Pflat[-countcells(Pold)]
    Pnew1=Pnew-lowval
    Pnew1[Pnew1<=0]=0
    Pnew1=Pnew1*netvalue(Pold, weight_mask)/netvalue(Pnew1, weight_mask)
    return Pnew1
    
    

def buildSpectrum(P):
    """
    reduces the storm to a 3-d power spectrum using a fft
    """
    Pf = np.fft.fftn(P)
    Ps = np.abs(Pf)**2
    return Ps

def plotSpectrum(Ps):
    """
    plots the power spectrum if you are into that
    """
    plt.figure(1)
    plt.clf()
    plt.imshow( np.log10( Ps[0,:,:] ))
    plt.xlabel('Spatial Frequency')
    plt.ylabel('Power Spectrum')
    plt.show()

def plotRainvid(P):
    """
    shows a video of the precipitation event
    """
    Nt = P.shape[0]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    im = ax.imshow(P[0,:,:])
    im.set_clim([0,1])
    fig.set_size_inches([5,5])
    
    def update_img(n):
        return ax.imshow(P[n,:,:])
    
    vid = ani.FuncAnimation(fig,update_img,np.arange(0,Nt),interval=30)
    plt.show()


def reproject(Ps, seed=False):
    """
    using the powerspectrum from the original storm, creates a new storm with the same power specturm but redistributed over space and time
    """
    if seed:
        np.random.seed(seed)
    Pf = np.sqrt(Ps)*np.exp(complex(0,1)*np.random.uniform(0.0,np.pi*2,Ps.shape))
    Prough = np.real(np.fft.ifftn(Pf))
    return Prough



