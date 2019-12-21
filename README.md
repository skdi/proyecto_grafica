# Reconstrucción 3D
# Carpeta Calibration:
Carpeta que contiene el codigo calibrate.py el cual usa las fotos en la carpeta aledaña para la fase de la calibración de la camara, exporta sus parámetros en formato .npy el cual es leido en la segunda fase.

El primer paso para obtener los parametros de la camara es tomar varias fotos de un tablero, las necesarias para obtener el largo del foco:

![Calibracion](/imagenes/calibracion.png)


# Carpeta Reconstruction:
Carpeta contenedora del codigo principal, el cual adquiere los parametros de la camara exportados por calibrate.py, dos imagenes de dos puntos de vista del mismo objeto, (imagen de ojo izquierdo y ojo derecho) para la reconstrucción del objeto 3D, exportando el resultado de la nube de puntos en un formato .ply el cual es abierto por un programa que permite la lectura de este como meshlab.

Para tomar las fotos al objetivo se imito la vision binocular humana:

![Estereo](/imagenes/estereo.png)

Para obtener los datos de objetivo, se tomaron dos fotos para encontrar la dimension de profundidad y proyectar la imagen:

![Disparidad](/imagenes/disparidad.png)

# Integrantes:
- André Mogrovejo Martínez.
- Nicolas Jimenez Artica.
- Franco Chavez Ponce.
- Jesus Lazo Quevedo.

![Figura 1](/imagenes/1_reconstruido.png)

![Figura 2](/imagenes/c1.png)

![Figura 3](/imagenes/c2.png)

![Figura 4](/imagenes/c3.png)

# Repositorio:
https://github.com/skdi/proyecto_grafica

# Video:
https://drive.google.com/drive/folders/1-TctCnj9BZu8FpPXR18isVsjHyM2Or8a
