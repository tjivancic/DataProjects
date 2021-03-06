import stormbuilder as sb
import os
os.system('tar -zxvf OnionCreekJun13.tar.gz')
P = sb.read_from_ncfolder('OnionCreekJun13/')
VP = sb.netvalue(P, weight_mask=1)
NP = sb.countcells(P)
Ps = sb.buildSpectrum(P)
Prough = sb.reproject(Ps)
sb.plotRainvid(P)
sb.plotRainvid(Prough)
Pnew = sb.allignPrecip(P,Prough)
sb.plotRainvid(Pnew)
