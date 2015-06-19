#!/usr/bin/env python
"""
Created on Mon May  4 18:39:39 2015

@author: John Swoboda
"""

import os, inspect, glob,pdb
import scipy as sp
from RadarDataSim.utilFunctions import makepicklefile
from RadarDataSim.IonoContainer import IonoContainer, MakeTestIonoclass
import RadarDataSim.runsim as runsim

def makeconfigfile(testpath):
    beamlist = [64094,64091,64088,64085,64082,64238,64286,64070,64061,64058,64055,64052,
                64049,64046,64043,64067,64040,64037,64034]
    radarname = 'pfisr'

    Tint=4.0*60.0
    time_lim = 3.0*Tint
    pulse = sp.ones(14)
    rng_lims = [150,500]
    IPP = .0087
    NNs = 28
    NNp = 100
    simparams =   {'IPP':IPP,
                   'TimeLim':time_lim,
                   'RangeLims':rng_lims,
                   'Pulse':pulse,
                   'Pulsetype':'long',
                   'Tint':Tint,
                   'Fitinter':Tint,
                   'NNs': NNs,
                   'NNp':NNp,
                   'dtype':sp.complex128,
                   'ambupsamp':30,
                   'species':['O+','e-'],
                   'numpoints':128,
                   'startfile':os.path.join(testpath,'startdata.h5'),
                   'SUMRULE': sp.array([[-2,-3,-3,-4,-4,-5,-5,-6,-6,-7,-7,-8,-8,-9]
                       ,[1,1,2,2,3,3,4,4,5,5,6,6,7,7]])}

    fname = os.path.join(testpath,'PFISRExample')

    makepicklefile(fname+'.pickle',beamlist,radarname,simparams)
def makeinputh5(Iono,basedir):
    Param_List = Iono.Param_List
    dataloc = Iono.Cart_Coords
    times = Iono.Time_Vector
    velocity = Iono.Velocity
    zlist,idx = sp.unique(dataloc[:,2],return_inverse=True)
    siz = list(Param_List.shape[1:])
    vsiz = list(velocity.shape[1:])

    datalocsave = sp.column_stack((sp.zeros_like(zlist),sp.zeros_like(zlist),zlist))
    outdata = sp.zeros([len(zlist)]+siz)
    outvel = sp.zeros([len(zlist)]+vsiz)

    for izn,iz in enumerate(zlist):
        arr = sp.argwhere(idx==izn)
        outdata[izn]=sp.mean(Param_List[arr],axis=0)
        outvel[izn]=sp.mean(velocity[arr],axis=0)

    Ionoout = IonoContainer(datalocsave,outdata,times,Iono.Sensor_loc,ver=0,
                            paramnames=Iono.Param_Names, species=Iono.Species,velocity=outvel)
    Ionoout.saveh5(os.path.join(basedir,'startdata.h5'))

def main():
    curpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    testpath = os.path.join(os.path.split(curpath)[0],'Testdata')
    origparamsdir = os.path.join(testpath,'Origparams')
    if not os.path.exists(testpath):
        os.mkdir(testpath)
        print "Making a path for testdata at "+testpath
    if not os.path.exists(origparamsdir):
        os.mkdir(origparamsdir)
        print "Making a path for testdata at "+origparamsdir

    # clear everything out
    folderlist = ['Origparams','Spectrums','Radardata','ACF','Fitted']
    for ifl in folderlist:
        flist = glob.glob(os.path.join(testpath,ifl,'*.h5'))
        for ifile in flist:
            os.remove(ifile)
    # Now make stuff again
    makeconfigfile(testpath)

    Icont1 = MakeTestIonoclass(testv=True,testtemp=False)
    makeinputh5(Icont1,testpath)
    Icont1.saveh5(os.path.join(origparamsdir,'0 testiono.h5'))
    funcnamelist=['spectrums','radardata','fitting']
    runsim.main(funcnamelist,testpath,os.path.join(testpath,'PFISRExample.pickle'),True)

if __name__== '__main__':

    main()