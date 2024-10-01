# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Converts ECEF vector components to SEZ

# Parameters:
#  o_x_km: 
#  o_y_km:
#  o_z_km:
#  x_km:
#  y_km:
#  z_km:

# Output:
#  Prints the south, east, and zenith vector
#
# Written by Nick Dickson
#

# import Python modules
import math # math module
import sys  # argv

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

## calculated denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# initialize script arguments
o_x_km = float('nan') # ECEF origin x-component in km
o_y_km = float('nan') # ECEF origin y-component in km
o_z_km = float('nan') # ECEF origin z-component in km
x_km = float('nan') # ECEF x-component in km
y_km = float('nan') # ECEF y-component in km
z_km = float('nan') # ECEF z-component in km

# parse script arguments
if len(sys.argv)==7:
  o_x_km = float(sys.argv[1])
  o_y_km = float(sys.argv[2])
  o_z_km = float(sys.argv[3])
  x_km = float(sys.argv[4])
  y_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
  )
  exit()

# write script below this line
#Doing ecef to llh to get lon and lat of origin
lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

r_x_km=x_km-o_x_km
r_y_km=y_km-o_y_km
r_z_km=z_km-o_z_km

r_km=[[r_x_km],
      [r_y_km],
      [r_z_km]]

Rzi=[[math.sin(lat_rad), 0, -1*math.cos(lat_rad)],
     [0, 1, 0],
     [math.cos(lat_rad), 0, math.sin(lat_rad)]]
Ryi=[[math.cos(lon_rad), math.sin(lon_rad), 0],
     [-1*math.sin(lon_rad), math.cos(lon_rad), 0],
     [0, 0, 1]]

recef_rot1 = [[0 for _ in range(1)] for _ in range(3)]

for i in range(len(Ryi)):
  for j in range(len(r_km[0])):
    for k in range(len(r_km)):
      recef_rot1[i][j] += Ryi[i][k] * r_km[k][j]

sez = [[0 for _ in range(1)] for _ in range(3)]

for i in range(len(Rzi)):
  for j in range(len(recef_rot1[0])):
    for k in range(len(recef_rot1)):
      sez[i][j] += Rzi[i][k] * recef_rot1[k][j]





s_km=sez[0][0]
e_km=sez[1][0]
z_km=sez[2][0]

print(s_km)
print(e_km)
print(z_km)
