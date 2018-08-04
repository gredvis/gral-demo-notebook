import numpy as np
import struct
import os
import glob
import json

def conc_domain(dir_conc):
	'''
	dir_conc = directory where GRAL.geb is located (usually the same directory as the con file)

	returns a dictionary of all the parameters for the domain (e.g. xmin, xmax, ymin, ymax)
	'''
	
	dom = {} # dictionary containing GRAL domain
	geb = [] #empty list for the values of domain parameters
	# read xmin, ymin, nx, ny, dx, dy from Gral.geb file
	with open(dir_conc+'GRAL.geb', 'r') as f:
		for line in f:
			geb.append(line.split()[0])

	dom['dx'] = int(float(geb[0]))
	dom['dy'] = int(float(geb[1]))
	dom['nx'] = int(float(geb[3]))
	dom['ny'] = int(float(geb[4]))
	dom['xmin'] = int(float(geb[7]))
	dom['xmax'] = int(float(geb[8]))
	dom['ymin'] = int(float(geb[9]))
	dom['ymax'] = int(float(geb[10]))

	with open('GRAL_domain.txt', 'w') as file:
		json.dump(dom, file)

	return dom

def conc_field(dir_conc, field):

	'''
	dir_conc = con file directory
	field = filename of con file (excluding the *con)

	return array contaning the concentration at each cell
	'''
	filename = dir_conc+field+'.con'

	geb = [] #empty list for domain parameters
	# read xmin, ymin, nx, ny, dx, dy from Gral.geb file
	with open(dir_conc+'GRAL.geb', 'r') as f:
		for line in f:
			geb.append(line.split()[0])

	dx = int(float(geb[0]))
	dy = int(float(geb[1]))
	nx = int(float(geb[3]))
	ny = int(float(geb[4]))
	xmin = int(float(geb[7]))
	ymin = int(float(geb[9]))

	conc = np.zeros((nx,ny),np.float)

	with open(filename, "rb") as f:

		# skip header
		f.read(4)

		while True:

			# read data
			data = f.read(12)

			if not data:
				break

			x,y,c = struct.unpack("iif", data)

			i = int(np.floor((x-xmin)/dx))
			j = int(np.floor((y-ymin)/dy))
			conc[i,j] = c

		
		np.savetxt('Concentration '+ str(field)+'.txt', np.transpose(np.array(conc)))

		return np.transpose(np.array(conc))

def conc_allfield(dir_conc,layer):

	'''
	dir_conc = con file directory
	layer = read all files for a specific horizontal slice
	
	returns an nd array which contains the concentration at each cell at each timestep
	'''

	filename = glob.glob(os.path.join(dir_conc, '*'+layer+'.con'))

	geb = [] #empty list for domain parameters
	# read xmin, ymin, nx, ny, dx, dy from Gral.geb file
	with open(dir_conc+'GRAL.geb', 'r') as f:
		for line in f:
			geb.append(line.split()[0])

	dx = int(float(geb[0]))
	dy = int(float(geb[1]))
	nx = int(float(geb[3]))
	ny = int(float(geb[4]))

	xmin = int(float(geb[7]))
	ymin = int(float(geb[9]))

	conc = np.zeros((len(filename),nx,ny),np.float)

	for k in range(len(filename)):
		with open(filename[k], "rb") as f:

			# skip header
			f.read(4)

			while True:

				# read data
				data = f.read(12)

				if not data:
					break

				x,y,c = struct.unpack("iif", data)

				i = int(np.floor((x-xmin)/dx))
				j = int(np.floor((y-ymin)/dy))
				conc[k,i,j] = c


	return np.transpose(conc,(0,2,1))

##########################################################
# Antoine Berchet's Extraction Code
##########################################################

# def old():
# 	dir_conc = r'C:\Users\mrp\Desktop\Concentration Files'
# 	field = r'\00001-201'


# 	fic=dir_conc+field+'.con'
# 	f=open(fic,'rb')
# 	data=f.read()
# 	f.close()

# 	print(data)

# 	body=struct.unpack("iiifi" * ((len(data)) // 20), data[:])
# 	conc=np.zeros((nx,ny),np.float)
# 	for k in range(len(body)/5):
# 	      x=float(body[5*k+1])
# 	      y=float(body[5*k+2])
# 	      c=float(body[5*k+3])
# 	      i=int(np.floor((x-xmin)/dx))
# 	      j=int(np.floor((y-ymin)/dy))
# 	      conc[i,j]=c