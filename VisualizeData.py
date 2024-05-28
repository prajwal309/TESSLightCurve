import numpy as np
import matplotlib.pyplot as plt
import glob
from astropy.io import fits
import os

def getFileNames(path):
    filePaths = []
    print("The path is given by:", path)
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if x.endswith(".fits"):
                filePaths.append(os.path.join(dirpath, x))
    return filePaths


AllTargetNames = glob.glob("data/*")

for Target in AllTargetNames:
    TargetName = Target.split("/")[1]
    print("Visualizing data for " + Target)

    TESSFileNames = getFileNames(Target+"/mastDownload/TESS/")
    K2FileNames = getFileNames(Target+"/mastDownload/K2/")
    KeplerFileNames = getFileNames(Target+"/mastDownload/Kepler/")
    print("The length of the file names is:", len(TESSFileNames))

    if len(TESSFileNames) >0:   
        print("The number of TESS files is:", TESSFileNames) 
        #Generate the light curve using TESS files
        TESS_TimeSeries = []
        TESS_FluxSeries = []

        for FileCounter, FileName in enumerate(TESSFileNames):
            print("Reading file: ", FileName)
            with fits.open(FileName) as hdulist:
                data = hdulist[1].data
                time = data["TIME"]
                flux = data["PDCSAP_FLUX"]
                
                NanIndex = np.isnan(flux)
                time = np.array(time[~NanIndex])
                flux = np.array(flux[~NanIndex])
                
                TESS_TimeSeries.extend(time)
                TESS_FluxSeries.extend(flux)

                SaveNameTxt = "ProcessedData/"+TargetName+"_"+str(FileCounter+1).zfill(5)+"_TESS.txt"
                SaveNamePng = "Figures/"+TargetName+"_"+str(FileCounter+1).zfill(5)+"_TESS.png"
                
                plt.figure(figsize=(12,6))
                #plt.plot(TESS_TimeSeries, TESS_FluxSeries, "k.")
                plt.plot(time, flux, "k.")
                plt.xlabel("Time (days)")
                plt.ylabel("Flux")
                plt.title("Target:"+Target.split("/")[1])
                plt.savefig(SaveNamePng)
                #plt.show()
                plt.close('all')

                np.savetxt(SaveNameTxt, np.array([time, flux]).T)

