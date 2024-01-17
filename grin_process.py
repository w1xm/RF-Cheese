import numpy as np

er_pla = 2.7
f = 17.39
t = 4
cx, cy = 90, 90

def extrusion_weight(line_center):
    x, y, z = line_center
    r = np.sqrt(((x-cx)/10)**2 + ((y-cy)/10)**2)
    if (r > 9):
        return 0.2
    e_r = (np.sqrt(er_pla)+(f-np.sqrt(f**2+r**2))/t)**2
    rho = (e_r - 1) / (er_pla-1)
    scale = 3.3333333333*rho
    # print(scale)
    return scale

infile = "lens.gcode"
outfile = "lens_out.gcode"

z = 0
x = 0
y = 0
e = 0

lastz = 0
lastx = 0
lasty = 0

lineidx = 0

with open(infile, 'r') as gcode_in:
    with open(outfile, 'w') as gcode_out:
        for line in gcode_in:
            if(line[:2] == "G1"): #Linear move
                #Strip comments
                cmts = line.split(';')
                if "Z" in cmts[0]: #Update Z position
                    z = float(line.split('Z')[1].split()[0])
                if "X" in cmts[0]: #Update X position
                    x = float(line.split('X')[1].split()[0])
                if "Y" in cmts[0]: #Update Y position
                    y = float(line.split('Y')[1].split()[0])

                if "E" in cmts[0]: #Modify extrusion multiplier
                    e = float(line.split('E')[1].split()[0])
                    #Calculate the center of the line
                    line_center = [(x + lastx)/2, (y + lasty)/2, (z + lastz)/2]
                    line = line.split('E')[0] + 'E' + ("%.5f" % (extrusion_weight(line_center)*e)) + '\n'

                lastx = x
                lasty = y
                lastz = z
            gcode_out.write(line)
            lineidx += 1


            
            

