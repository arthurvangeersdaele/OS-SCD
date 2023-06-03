# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 07:45:03 2023

@author: Arthur Van Geersdaele
"""
# Imports
import svgwrite
import numpy as np
import time
import os
from pathlib import Path

# Define constants and/or mechanical standards 
gauge_value_chart = [3.404, 3.048, 2.769, 2.413, 2.109, 1.829, 1.651, 1.473, 1.27, 1.067,
                                             0.908, 0.819, 0.718,0.642, 0.566, 0.515, 0.464, 0.413, 0.362, 0.337,
                                             0.312, 0.261, 0.235, 0.210, 0.159] # source: https://www.hamiltoncompany.com/laboratory-products/needles-knowledge/needle-gauge-chart
gauge_value_chart = [None for i in range(0,10)] + gauge_value_chart



# @pre: ID inner diameter of the pneumatic band
#       n       Desired number of pouches in the band
#       l,g     Desired width and length of a signle pouch
#       ll,gg   Desired width and length of an interconnexion 
#       L       Desired width of the final band
#       Gplus   Additionnal length at the end of the band to add Velcro 
#       Gminus  Additionnal length at the beginning of the band to add Velcro 
#       elbow1, elbow2  Dimensions of the elbow (advised to not touch)
#
# @post: Create a folder named "[..args..]_tag_FOLDER" at the script emplacement.
#       That folder contains: 
#       1) An info file containing all the specifications relative to the identity of the pouch 
#       2) A .svg file to lasercut the 2x heat_sealable layers in one manipulation
#       3) A .svg file to lasercut the 1x intermediate_layer in one manipulation
#       4) Two .svg file to create the metal patron in 2 manipulations
#       5) A global rendering of the geometry of the pneumatic band
def draw_svg(ID, n, l, g, L, Gplus, Gminus=30, ll=5, gg=5, elbow1 = 50, elbow2 = 20, name = 'no_name_set'):
    # Assertions based on parameters
    assert(ID != None), f"\nInner Diameter (ID = {ID}) is not valid.\n Please check the way you define it."
    assert(ID < ll), f"\nInner Diameter (ID = {ID}) is not valid compared to the width of the intersections between the pouch. \nPlease check the way you define it."
    assert(L-l > 2), f'Regarding l = {l}mm and L = {L}mm, \nthere is not enough join-width left (L-l)/2 = {(L-l)/2}mm'
    assert(elbow1 + l/2 - ll/2 > l+10), "Please, do not touch to the elbow values."
    # Additionnal values deduction/hardcoded for math simplifications 
    border_width = (L-l)/2
    G = elbow2 + n*g + (n-1)*gg + Gplus + Gminus + 2*border_width # length of the final pouch band
    ll_input = ID*np.pi/2 + 0.5 # Computation based on the wanted inner-diameter
    water_cutter_clearance=1 #[mm] 
    outer_frame_width = 5 #[mm]  
    # Useful values for cutting preparation 
    intermediate_layer_id_box = (elbow2 + n*g + (n-1)*gg, l/2+ll/2+5 + elbow1)
    heat_sealable_layer_id_box = (G , 2*L+5)
    # Useful values for the Niiyama hypothesis validation
    theta = (46/180)*np.pi
    niiyama_volume_estimation = n*((theta - np.cos(theta)*np.sin(theta))/theta**2) * (g**2 * l)/2
    corrected_niiyama_volume_estimation = ((theta - np.cos(theta)*np.sin(theta))/theta**2) * (n*(g**2 * l)/2 + (n-1)*(gg**2 * ll)/2)
    
    # Saving work in a single file for further studies and easy identification
    folder_name = name + "_FOLDER"
    print("Folder name was set as "+ folder_name)
    script_dir = Path(__file__).resolve().parent
    (script_dir / folder_name).mkdir()
    # writing informations in a text file
    timestr = time.strftime(" date : %y/%m/%d - time : %Hh%Mmin%Ss ")
    others = ["TPU Textile dimensions needed for the 2 heat_sealable_layers: "+str(heat_sealable_layer_id_box[0])+"x"+str(heat_sealable_layer_id_box[1])+"mm",
              "Baking paper dimensions needed for the intermediate_layer: "+str(intermediate_layer_id_box[0])+"x"+str(intermediate_layer_id_box[1])+"mm",
              "Nyamara Volume of the band: "+str(niiyama_volume_estimation)+ "mm3",
              "Nyamara Volume of the band considering interconnections: "+str(corrected_niiyama_volume_estimation)+"mm3"]
    write(folder_name, timestr, ID, n, l, g, L, G, Gplus, Gminus, ll, gg, elbow1=elbow1, elbow2=elbow2, others=others, name = name)
    
    ### INTERMEDIATE LAYER ###
    # SVG creation + dimension definition from parameters
    w_ = G + 10
    h_ = l + elbow1
    SIZE = (str(w_)+"mm", str(h_)+'mm')
    VIEWBOX = ('0 0 '+str(w_)+' '+str(h_))
    tmp = "("+str(intermediate_layer_id_box[0])+"x"+str(intermediate_layer_id_box[1])
    filename = name+"_intermediate_layer"+tmp+"mm).svg"
    dwg = svgwrite.Drawing(folder_name+"/"+filename, profile="tiny", size=SIZE, viewBox=VIEWBOX, stroke_width=1)
    # Automatic point definition (x, y) with upper-left origin
    # Elbow smoothening (hardcoded) :: TODO switch to a interpolated curve 
    prct1 = 7/10
    prct2 = 1/2
    a = (elbow2, l/2+ll/2+5)
    b = (elbow2 * (1 - prct2), a[1])
    c = (ll_input , a[1]-ll+elbow1*(1-prct1))
    d = (ll_input , a[1]+elbow1)
    e = (0, d[1])
    dbis = (d[0], (L+l)/2)
    ebis = (e[0], (L+l)/2)
    f = (e[0], b[1] - ll)#(e[0], c[1] - ll)
    h = (b[0]-ll, b[1]-ll)
    j = (a[0], h[1]-5)
    # Creating the pouches arcs 
    # 1 - upper arcs
    last = j
    upper_pouch_points = []
    for i in range(n):
        i_arc = arc(last, l, g, ll, gg, orientation='up')
        upper_pouch_points += i_arc
        last = i_arc[-1]
    
    upper_pouch_points = upper_pouch_points[:-1]
    last = upper_pouch_points[-1]
    w = (last[0], l)
    # 2 - lower arcs
    last = w
    lower_pouch_points = []
    for i in range(n):
        i_arc = arc(last, l, g, ll, gg, orientation='down')
        lower_pouch_points += i_arc
        last = i_arc[-1]
    lower_pouch_points = lower_pouch_points[:-1]
    lower_pouch_points = lower_pouch_points[:-1]
    intermediate_layer_points = [a, b, c, dbis, d, e, ebis, f, h, j] + upper_pouch_points + [w] + lower_pouch_points + [a]
    intermediate_layer_points = [a, b, c, dbis, d, e, ebis, f, j] + upper_pouch_points + [w] + lower_pouch_points + [a] # h is removed
    # Drawing the points and saving
    dwg.add(dwg.polyline(intermediate_layer_points, stroke='black', fill='none'))
    dwg.save()
    
    ### HEAT SEALABLE LAYER ###
    # SVG creation + dimension definition from parameters
    filename = name+"_heat_sealable_layer"+"("+str(heat_sealable_layer_id_box[0])+"x"+str(heat_sealable_layer_id_box[1])+"mm).svg"
    w_ = G + 10
    h_ = 2*(l + elbow1)
    SIZE = (str(w_)+"mm", str(h_)+'mm')
    VIEWBOX = ('0 0 '+str(w_)+' '+str(h_))
    dwg2 = svgwrite.Drawing(folder_name+"/"+filename, profile="tiny", size=SIZE, viewBox=VIEWBOX, stroke_width=0.5)
    # Setting the points of the heat_sealable_layer
    p = (0,0)
    q = (G, p[1])
    r = (q[0], L)
    s = (p[0], r[1])
    heat_sealable_layer_points = [p, q, r, s, p]
    # Duplicating for faster fabrication in lasercut machines (5mm distance)
    heat_sealable_layer_points2 = []
    for pt in heat_sealable_layer_points:
        heat_sealable_layer_points2 += [(pt[0], pt[1] + L + 5)]
    # Drawing the points and saving
    dwg2.add(dwg.polyline(heat_sealable_layer_points, stroke='black', fill='none'))
    dwg2.add(dwg.polyline(heat_sealable_layer_points2, stroke='black', fill='none'))
    dwg2.save()
    
    ### GLOBAL RENDERING WITH COLORS ###
    # SVG creation + dimension definition from parameters
    filename = name+"_global_render.svg"
    w_ = G + 10
    h_ = l + elbow1
    SIZE = (str(w_)+"mm", str(h_)+'mm')
    VIEWBOX = ('0 0 '+str(w_)+' '+str(h_))
    dwg3 = svgwrite.Drawing(folder_name+"/"+filename, profile="tiny", size=SIZE, viewBox=VIEWBOX, stroke_width=1)
    dwg3.add(dwg.polyline(heat_sealable_layer_points, stroke='red', fill='none'))
    # Setting the offset 
    positionned_intermediate_layer_points = []
    for pt in intermediate_layer_points:
        positionned_intermediate_layer_points+=[(pt[0] + Gminus + border_width, pt[1] + border_width)]
    dwg3.add(dwg.polyline(positionned_intermediate_layer_points, stroke='blue', fill='none'))
    dwg3.save()
    
    ### METAL PATRON GENERATOR ###
    filename = name+"_metalpatron_inner.svg"
    w_ = G + 10
    h_ = 2*L + 15
    SIZE = (str(w_)+"mm", str(h_)+'mm')
    VIEWBOX = ('0 0 '+str(w_)+' '+str(h_))
    # Creating the 2 inner plates
    dwg4 = svgwrite.Drawing(folder_name+"/"+filename, profile="tiny", size=SIZE, viewBox=VIEWBOX, stroke_width=1)
    # Add the offset to a, b, c, dbis, ebis, ...]
    a_ = (a[0]+border_width + Gminus, a[1]+border_width)
    b_ = (b[0]+border_width + Gminus, b[1]+border_width)
    c_ = (c[0]+border_width + Gminus, c[1]+border_width)
    d_ = (d[0]+border_width + Gminus, d[1]+border_width)
    dbis_ = (dbis[0]+border_width + Gminus, dbis[1]+border_width)
    e_ = (e[0]+border_width, e[1]+border_width)
    ebis_ = (ebis[0]+border_width + Gminus, ebis[1]+border_width)
    f_ = (f[0]+border_width + Gminus, f[1]+border_width)
    h_ = (h[0]+border_width + Gminus, h[1]+border_width)
    j_ = (j[0]+border_width + Gminus, j[1]+border_width)
    w_ = (w[0]+border_width + Gminus, w[1]+border_width)
    upper_pouch_points_ = []
    for pt in upper_pouch_points:
        upper_pouch_points_+=[(pt[0] + border_width + Gminus, pt[1] + border_width)]
    lower_pouch_points_ = []
    for pt in lower_pouch_points:
        lower_pouch_points_+=[(pt[0] + border_width + Gminus, pt[1] + border_width)]
    inner_patron_points = [a_, b_, c_, dbis_, r, q, p, s, ebis_, f_, h_, j_] + upper_pouch_points_ + [w_] + lower_pouch_points_ + [a_]
    inner_patron_points = [a_, b_, c_, dbis_, r, q, p, s, ebis_, f_, j_] + upper_pouch_points_ + [w_] + lower_pouch_points_ + [a_] # h is removed
    # Duplicating for faster fabrication in lasercut machines (5mm distance)
    inner_patron_points2 = []
    for pt in inner_patron_points:
        inner_patron_points2 += [(pt[0], pt[1] + L + 10)]
    # Drawing the points and saving
    dwg4.add(dwg.polyline(inner_patron_points, stroke='black', fill='none'))   
    dwg4.add(dwg.polyline(inner_patron_points2, stroke='black', fill='none'))   
    dwg4.save()      

    # Creating the outer frame
    filename = name+"_metalpatron_outer.svg"
    w_ = G + 10
    h_ = L + outer_frame_width*2 + 10
    SIZE = (str(w_)+"mm", str(h_)+'mm')
    VIEWBOX = ('0 0 '+str(w_)+' '+str(h_))
    # Creating the outer plate
    dwg5 = svgwrite.Drawing(folder_name+"/"+filename, profile="tiny", size=SIZE, viewBox=VIEWBOX, stroke_width=1)
    # Setting the points
    p1 = (outer_frame_width,outer_frame_width)
    q1 = (G+outer_frame_width, p1[1])
    r1 = (q1[0], L+outer_frame_width)
    s1 = (p1[0], r1[1])
    p2 = (0,0)
    q2 = (G+2*outer_frame_width, p2[1])
    r2 = (q2[0], L+2*outer_frame_width)
    s2 = (p2[0], r2[1])
    outer_patron_points1 = [p1, q1, r1, s1, p1]
    outer_patron_points2 = [p2, q2, r2, s2, p2] 
    # Drawing the points and saving
    dwg5.add(dwg.polyline(outer_patron_points1, stroke='black', fill='none'))   
    dwg5.add(dwg.polyline(outer_patron_points2, stroke='black', fill='none'))   
    dwg5.save()         
    print("Design files created at "+timestr)
    return 1

def write_info(ID, n, l, g, L, Gplus, Gminus=30, ll=5, gg=5, temperature = 200, duration = 30, elbow1 = 30, elbow2 = 20, name ='no_name_set'):
    # creating a folder
    timestr = time.strftime("%m%d-%H%M%S") # for file identification 
    folder_name = name + "_FOLDER"
    script_dir = Path(__file__).resolve().parent
    (script_dir / folder_name).mkdir()
    # additional values
    border_width = (L-l)/2
    G = elbow2 + n*g + (n-1)*gg + Gplus + 2*border_width
    # writing informations in a text file
    write(folder_name, timestr, ID, n, l, g, L, G, Gplus, Gminus, ll, gg, temperature, duration, elbow1, elbow2)
    print("Info file created ["+name+"]")
    
def write(folder_name, timestr, ID, n, l, g, L, G, Gplus, Gminus=30, ll=5, gg=5, temperature = 200, duration = 30, elbow1 = 30, elbow2 = 20, name = 'no_name_set', others = []):
    filename = name+"_INFO.txt"
    with open(folder_name+"/"+filename, 'w') as file:
        file.write(f"WARNING: SVG has to be converted to paths before being converted to RXF for laser-cutting.\n")
        file.write(f"         For better cutting, you can combine the curves using the cutting program.\n")
        file.write(f"Tips: The ID of the band is structured as follow \n")
        file.write(f"      [n - ID - l - g - L - ll - gg - Gplus - Gminus]_tag\n")
        file.write(f"=========================================================================================\n\n")
        file.write(f"Design specifications\n")
        file.write(f"- Reference ID: {name}\n")
        file.write(f"- Input diameter: {ID}mm\n")
        file.write(f"- Number of pouches: {n}\n")
        file.write(f"- Dimensions of a pouch: {l}x{g}mm\n")
        file.write(f"- Dimensions of the band: {G}x{L}mm\n")
        file.write(f"- Distance between each pouch: {gg}mm\n")
        file.write(f"- Inner tube width: {ll}mm\n")
        file.write(f"- Additionnal length at the beginning of the pouch-chain (air input to the left): {Gminus}mm\n")
        file.write(f"- Additionnal length at the end of the pouch-chain: {Gplus}mm\n")
        file.write(f"- Elbow dimensions: {elbow2}x{elbow1}mm\n")
        if(len(others)>0) : 
            file.write(f"Others\n")
        for spec in others:
            file.write(f"- "+spec+"\n")
        file.write(f"\n")
        file.write(f"NB: The id-box dimensions needed for laser-cutting are written at the end of the filenames.\n")
        file.write(f"NB2: Depending on the material used, it can be a retractation of the fabric during the laser-cutting.\n")
        file.write(f"     Take that in account while setting your parameters.\n")
        file.write(f"\n")
        file.write(f"Additionnal information on the fabrication process, handwritten\n")
        file.write(f"- Material: One-sided TPU coated Textile (70d)\n")
        file.write(f"- Fusion process parameters: T={temperature}Celsius, t={duration}s (set to 200C, 30s default for TPU)\n")
        file.write(f"\n")
        file.write(f"Other notes, remarks..., about {name}\n")
        file.write(f"***************************************************************************************\n")
        file.write(f"\n\n\n")
        file.write(f"***************************************************************************************\n")
        file.write(f"\n\n Info file automatically generated at" + timestr + " using IPCdevice_designer_v2.py\n")
    file.close()
    return 0

def arc(last, l, g, ll, gg, orientation='up'):
    if(orientation=='up'):
        pt1x = last[0]
        pt1y = 0
        pt1 = (pt1x, pt1y)
        pt2x = pt1[0] + g
        pt2y = pt1[1]
        pt2 = (pt2x, pt2y)
        pt3x = pt2[0]
        pt3y = l/2 - ll/2
        pt3 = (pt3x, pt3y)
        pt4x = pt3[0] + gg
        pt4y = pt3[1]
        pt4 = (pt4x, pt4y)
        return [pt1, pt2, pt3, pt4]
    if(orientation=='down'):
        pt1x = last[0]
        pt1y = l
        pt1 = (pt1x, pt1y)
        pt2x = pt1[0] - g
        pt2y = pt1[1]
        pt2 = (pt2x, pt2y)
        pt3x = pt2[0]
        pt3y = l/2 + ll/2
        pt3 = (pt3x, pt3y)
        pt4x = pt3[0] - gg
        pt4y = pt3[1]
        pt4 = (pt4x, pt4y)
        return [pt1, pt2, pt3, pt4]
    return [-1]
