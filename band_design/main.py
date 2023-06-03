# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 07:45:03 2023

@author: Arthur Van Geersdaele
"""
            #####################################################
            #                                                   #
            # * Run this file to generate your pneumatic band * #
            #                                                   #
            #####################################################
# imports      
from IPCdevice_designer_v2 import draw_svg
from IPCdevice_designer_v2 import write_info
from IPCdevice_designer_v2 import gauge_value_chart
# Inner Diameter set up by our base article
schara_ID = 3.1831 #[mm]
# Inner Diameter set up to fit medical needles
gauge_16_ID = gauge_value_chart[16] #[mm]


# do a complete set or only an info-file in the folder 
complete = True

# specifications (to fill by hand)
n = 5 # pouch number [mm]
ID = 4 # inner diameter [mm]
l = 30 # pouch width [mm]
g = 30 # pouch length [mm]
L = 60 # global width [mm]
ll= 5 # interconnection width [mm]
gg= 5 # interconnexions length [mm]
Gplus = 60 # additionnal length [mm] (end) 
Gminus = 60 # additionnal length [mm] (beginning)
temperature = 200 # heating temperature [Celsius]
duration = 45 # heating time [s]

tag = '_'+'StandardL'

# Exemple d'utilisation 
def run():
    # global variables 
    global  n, ID, l, g, L, Gplus, Gminus, ll, gg, temperature, duration
    # file identification 
    name = "["+str(n)+"-"+str(ID)+"-"+str(l)+"-"+str(g)+"-"+str(L)+"-"+str(ll)+"-"+str(gg)+"-"+str(Gplus)+"-"+str(Gminus)+"]"+tag 
    if(complete):
        # draw the designs into a single folder
        draw_svg(ID = ID, n=n, l=l, g=g, L=L, Gplus=Gplus, Gminus=Gminus, ll=ll, gg=gg, name=name)
    else:
        # to create reference about elderly created bands
        write_info(ID = ID, n=n, l=l, g=g, L=L, Gplus=Gplus, Gminus=Gminus, ll=ll, gg=gg,
                   temperature = temperature, duration = duration, name=name)
run()