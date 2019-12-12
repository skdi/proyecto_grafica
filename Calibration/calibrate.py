
import cv2
import numpy as np 
import glob
from tqdm import tqdm
import PIL.ExifTags
import PIL.Image

#============================================
# Calibracion de camara
#============================================

#Definiendo tamaño del ajedrez para la calibración 

tablero_size = (7,5)

#Arrays usados para  almacenar los puntos trabajados
obj_points = [] #puntos 3d en el mundo real
img_points = [] #puntos 3d en el plano de la imagen

#preparando malla y puntos a mostrar
objp = np.zeros((np.prod(tablero_size),3),dtype=np.float32)

objp[:,:2] = np.mgrid[0:tablero_size[0], 0:tablero_size[1]].T.reshape(-1,2)

#lectura de imagenes

calibration_paths = glob.glob('./calibration_images/*')

#iteracion sobre las imagenes para encontrar la matriz intrinseca
for image_path in tqdm(calibration_paths):

	#cargando imagen
	image = cv2.imread(image_path)
	#filtro en escala de grises de la imagen
	imagen_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	print("Imagen cargada, analizando...")
	#encontrando las esquinas del tablero
	ret,esquinas = cv2.findChessboardCorners(imagen_gris, tablero_size, None)

	if ret == True:
		print("Tablero detectado")
		print(image_path)
		#definiendo el criterio para la precision de los subpixeles
		criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		#refinando la localicacion de las esquinas basado en el criterio(precision de subpixeles)
		cv2.cornerSubPix(imagen_gris, esquinas, (5,5), (-1,-1), criterio)
		obj_points.append(objp)
		img_points.append(esquinas)

#Calibracion de camara
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,imagen_gris.shape[::-1], None, None)

#guardado de los datos obtenidos en archivos numpy
np.save("./camera_params/ret", ret)
np.save("./camera_params/K", K)
np.save("./camera_params/dist", dist)
np.save("./camera_params/rvecs", rvecs)
np.save("./camera_params/tvecs", tvecs)

#Obteniendo data resultante para obtener la longitud focal
exif_img = PIL.Image.open(calibration_paths[0])

exif_data = {
	PIL.ExifTags.TAGS[k]:v
	for k, v in exif_img._getexif().items()
	if k in PIL.ExifTags.TAGS}

#obteniendo la longitud focal en forma de tuplas
focal_length_exif = exif_data['FocalLength']

#Obteniendo la longitud focal en forma decimal
focal_length = focal_length_exif[0]/focal_length_exif[1]

#guardando longitud focal
np.save("./camera_params/FocalLength", focal_length)

#Calculo del error de la proyeccion
error_medio = 0
for i in range(len(obj_points)):
	img_points2, _ = cv2.projectPoints(obj_points[i],rvecs[i],tvecs[i], K, dist)
	error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2)/len(img_points2)
	error_medio += error

derror_total = error_medio/len(obj_points)
print (derror_total)
