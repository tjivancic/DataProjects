import numpy as np
from scipy.io import netcdf as nc
import os
import matplotlib.pyplot as plt
import matplotlib.animation as ani

def read_from_ncfolder(infolder, files=False):
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
    Nt = P.shape[0]
    runsum = 0
    for i in range(Nt):
        runsum += sum(sum(P[i,:,:]*weight_mask))
    return runsum

def countcells(P):
    return sum(sum(sum(P>0)))

def allignPrecip(Pold,Pnew, weight_mask=1):
    Pflat = Pnew.flatten()
    Pflat.sort()
    lowval = Pflat[-countcells(Pold)]
    Pnew1=Pnew-lowval
    Pnew1[Pnew1<=0]=0
    Pnew1=Pnew1*netvalue(Pold, weight_mask)/netvalue(Pnew1, weight_mask)
    return Pnew1
    
    

def buildSpectrum(P):
    Pf = np.fft.fftn(P)
    Ps = np.abs(Pf)**2
    return Ps

def plotSpectrum(Ps):
    plt.figure(1)
    plt.clf()
    plt.imshow( np.log10( Ps[0,:,:] ))
    plt.xlabel('Spatial Frequency')
    plt.ylabel('Power Spectrum')
    plt.show()

def plotRainvid(P):
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
    if seed:
        np.random.seed(seed)
    Pf = np.sqrt(Ps)*np.exp(complex(0,1)*np.random.uniform(0.0,np.pi*2,Ps.shape))
    Prough = np.real(np.fft.ifftn(Pf))
    return Prough



