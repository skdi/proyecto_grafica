import cv2
import numpy as np 
import glob
from tqdm import tqdm

import PIL.ExifTags
import PIL.Image
from matplotlib import pyplot as plt 

#=====================================
# Declaracion de funciones
#=====================================

#Funcion para crear el archivo de la nube de puntos
def generar_salida(vertices, colores, archivo):
	colores = colores.reshape(-1,3)
	vertices = np.hstack([vertices.reshape(-1,3),colores])

	ply_header = '''ply
		format ascii 1.0
		element vertex %(vert_num)d
		property float x
		property float y
		property float z
		property uchar red
		property uchar green
		property uchar blue
		end_header
		'''
	with open(archivo, 'w') as f:
		f.write(ply_header %dict(vert_num=len(vertices)))
		np.savetxt(f,vertices,'%f %f %f %d %d %d')

#Function that Downsamples image x number (reduce_factor) of times. 
#funcion que
def downsample_image(imagen, reduce_factor):
	for i in range(0,reduce_factor):
		#revisando que la imagen este en escala de grises
		if len(imagen.shape) > 2:
			row,col = imagen.shape[:2]
		else:
			row,col = imagen.shape

		imagen = cv2.pyrDown(imagen, dstsize= (col//2, row // 2))
	return imagen


#=========================================================
# Reconstruccion stereo 3D
#=========================================================

#cargando parametros de la camara
ret = np.load('./camera_params/ret.npy')
K = np.load('./camera_params/K.npy')
dist = np.load('./camera_params/dist.npy')

#especificando paths de imagenes
img_path1 = './reconstruct_this/left2.jpg'
img_path2 = './reconstruct_this/right2.jpg'

#carga de imagenes
img_1 = cv2.imread(img_path1)
img_2 = cv2.imread(img_path2)

#obteniendo altura y ancho de la imagen (ambas son del mismo tamaño
h,w = img_2.shape[:2]

#obteniendo la matriz obtima para menor distorcion
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K,dist,(w,h),1,(w,h))

#imagenes sin distorcion
img_1_undistorted = cv2.undistort(img_1, K, dist, None, new_camera_matrix)
img_2_undistorted = cv2.undistort(img_2, K, dist, None, new_camera_matrix)

#Downsample each image 3 times (because they're too big)
img_1_downsampled = downsample_image(img_1_undistorted,3)
img_2_downsampled = downsample_image(img_2_undistorted,3)

#cv2.imwrite('undistorted_left.jpg', img_1_downsampled)
#cv2.imwrite('undistorted_right.jpg', img_2_downsampled)


#Set disparity parameters
#Note: disparity range is tuned according to specific parameters obtained through trial and error. 
win_size = 5
min_disp = -1
max_disp = 63 #min_disp * 9
num_disp = max_disp - min_disp # Needs to be divisible by 16

#Create Block matching object. 
stereo = cv2.StereoSGBM_create(minDisparity= min_disp,
	numDisparities = num_disp,
	blockSize = 5,
	uniquenessRatio = 5,
	speckleWindowSize = 5,
	speckleRange = 5,
	disp12MaxDiff = 2,
	P1 = 8*3*win_size**2,#8*3*win_size**2,
	P2 =32*3*win_size**2) #32*3*win_size**2)

#Compute disparity map
print ("\nComputing the disparity  map...")
disparity_map = stereo.compute(img_1_downsampled, img_2_downsampled)

#Show disparity map before generating 3D cloud to verify that point cloud will be usable. 
plt.imshow(disparity_map,'gray')
plt.show()

#Generate  point cloud. 
print ("\nGenerating the 3D map...")

#Get new downsampled width and height 
h,w = img_2_downsampled.shape[:2]

#Load focal length. 
focal_length = np.load('./camera_params/FocalLength.npy')

#Perspective transformation matrix
#This transformation matrix is from the openCV documentation, didn't seem to work for me. 
Q = np.float32([[1,0,0,-w/2.0],
				[0,-1,0,h/2.0],
				[0,0,0,-focal_length],
				[0,0,1,0]])

#This transformation matrix is derived from Prof. Didier Stricker's power point presentation on computer vision. 
#Link : https://ags.cs.uni-kl.de/fileadmin/inf_ags/3dcv-ws14-15/3DCV_lec01_camera.pdf
Q2 = np.float32([[1,0,0,0],
				[0,-1,0,0],
				[0,0,focal_length*0.05,0], #Focal length multiplication obtained experimentally. 
				[0,0,0,1]])

#Reproject points into 3D
points_3D = cv2.reprojectImageTo3D(disparity_map, Q2)
#Get color points
colores = cv2.cvtColor(img_1_downsampled, cv2.COLOR_BGR2RGB)

#Get rid of points with value 0 (i.e no depth)
mask_map = disparity_map > disparity_map.min()

#Mask colores and points. 
output_points = points_3D[mask_map]
output_colors = colores[mask_map]

#Define name for output file
output_file = 'reconstructed.ply'

#Generate point cloud 
print ("\n Creating the output file... \n")
generar_salida(output_points, output_colors, output_file)

