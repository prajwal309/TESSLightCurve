import numpy as np
import lightkurve as lk
import matplotlib.pyplot as plt
import os
TargetHotStars = ["HD 189733 b",  "WASP-12","WASP-17", "WASP-19", "WASP-39", "WASP-121"]#, "55 Cnc"] #Adding 55 CNc to the end 
TargetCoolStars = ["TRAPPIST-1", "GJ 1214", "GJ 436", "K2-18", "AU Mic", "K2-3", "HAT-P-12", "HAT-P-11"]
TargetNames = TargetHotStars + TargetCoolStars

print("The target names are given by:", TargetNames)


for Target in TargetNames:
    print("Downloading data for " + Target)
    search_result = lk.search_lightcurve(Target)
    SaveDirectory = "data/" + Target.replace(" ", "_")
    if not os.path.exists(SaveDirectory):
        os.makedirs(SaveDirectory)
    try:
        lc = search_result.download_all(download_dir=SaveDirectory)
    except:
        print("Error in downloading: " + Target)