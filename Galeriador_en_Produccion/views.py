from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django import forms
import os, sys
import shutil
from PIL import Image

#JASR: Enlace la voy a usar en distintas funciones, por lo que la declaro como global
#JASR: EL PROBLEMA NO ERA ESE, PORQUE LO ESTAS LLAMANDO EN UNA FUNCIÓN Y PASANDOLO A LA OTRA (LO COMENTO)
#enlace = ''


def home(request):
    return render(request, 'home.html' , context={})

def constructor(request):
    #Voy a utilizar enlace como global en esta funcion
	#global enlace
    if request.method == 'POST':
        eleccion = request.POST.get('interfaz')
        files = request.FILES.getlist('imagen')
        for f in files:
            fs = FileSystemStorage()
            fs.save(f.name, f)
        enlace = arranca(eleccion)
        iframe = '<iframe width="600" height="400" src="' + enlace + '" frameborder="0"></iframe>'
        context = ({
        'path': enlace,
        'iframe': iframe,
        'data': eleccion
        })
        return render(request, 'end.html', context=context)
    else:
        return HttpResponse('ERROR!')

def arranca(eleccion):
	#Voy a utilizar enlace como global en esta funcion
    #global enlace
    #--------------------------------- CODIGO DE EJECUCION ---------------------------------------------------
    ruta = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	
	#JASR: AQUI PASA ALGO RARO Y POR ESO FALLA LO DEL ENLACE (CAMBIE LAS / porque daba error)
    workpath = ruta + '/media'
    os.chdir(workpath) # <------------------ Change the current working directory to the specified path.
    contenido = os.listdir(workpath)
    
    cont = 0
    imagenes = []
    imagenesmrg = []
    imagenesmr = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(workpath, fichero)) and (fichero.endswith('.jpg') or fichero.endswith('.JPG')
                or fichero.endswith('.png') or fichero.endswith('.PNG')
                or fichero.endswith('.gif') or fichero.endswith('.GIF')
                or fichero.endswith('.jpeg') or fichero.endswith('.JPEG')
                or fichero.endswith('.tif') or fichero.endswith('.TIF')
                or fichero.endswith('.tiff') or fichero.endswith('.TIFF')
                or fichero.endswith('.svg') or fichero.endswith('.SVG')
                or fichero.endswith('.png') or fichero.endswith('.png')
                or fichero.endswith('.webp') or fichero.endswith('.WEBP')
                or fichero.endswith('.bmp') or fichero.endswith('.BMP')
                or fichero.endswith('.dib') or fichero.endswith('.DIB')):
            # Si es identificada como una imagen pasamos a cambiarle el nombre por precaucion
            cont = cont + 1
            name, ext = os.path.splitext(fichero)
            ficheroname = 'fotocbf' + str(cont) + ext
            os.rename(fichero, ficheroname)
            image = Image.open(ficheroname)
            razon = image.size[1]/image.size[0]
            
            if image.size[1] > 380:
                newim1 = image.resize((int(375/razon),375))
            else:
                newim1 = image

            if image.size[1] > 110:
                newim2 = image.resize((int(100/razon),100))
            else:
                newim2 = image
            
            name, ext = os.path.splitext(ficheroname)
            fichero_mrg = name + '_mrg' + ext
            fichero_mr = name + '_mr' + ext
            newim1.save(fichero_mrg)
            newim2.save(fichero_mr)
            imagenesmrg.append(fichero_mrg)
            imagenesmr.append(fichero_mr)
            imagenes.append(ficheroname)
            image.close()

    if cont == 0:                       # comprobamos si hay imagenes cargadas
        print('Se le pudo olvidar cargar las imagenes? Por favor, compruebelo y vuelva a ejecutar el script.')
    else:                               # si han cargado las imagenes, continua el proceso de creacion de la galeria
        start = 0
        # comprobacion del fichero de registro de los directorios de alojamiento de las galerias
        for fichero in contenido:
            if os.path.isfile(os.path.join(workpath, fichero)) and fichero == 'directorios':
                start = 1

        if start == 0:                  # si es la primera, se crea el archivo de registro
            cadena = 'En este fichero se almacenan los nombres de los distintos alojamientos de cada album\n'
            #Con la instancia 'with' cerramos el documento despues de escribir en el
            with open('directorios', 'w') as f:
                f.write(cadena)
                f.write('album1\n')
                directorioN = 'album1'
        else:                           # si no lo es, se añade el siguiente
            with open('directorios','r') as f:
                f.seek(0)
                nl = len(f.readlines())
            albumS = 'album' + str(nl)
            directorioN = albumS
            with open('directorios', 'a') as f:
                f.write(albumS + '\n')
        
        # creacion del directorio que alojara la galeria en cuestion
        directorio = 'uma/' + directorioN
        os.mkdir(directorio)

        # preparacion del archivo html

        if eleccion == 'clara':
            doc_html = workpath + '/uma/album_claro.html'
        elif eleccion == 'oscura':
            doc_html = workpath + '/uma/album_oscuro.html'
        
        with open(doc_html,'r', encoding='utf-8') as f:
            lecturaAlbum = f.read()

        lista = ''
        for i in imagenes:
            lista = lista + '"' + i + '", '
        lista = lista.rstrip(', ')
        newdoc = lecturaAlbum.replace('//MARCADOR','fotito = [' + lista + '];')

        listamrg = ''
        for i in imagenesmrg:       
            listamrg = listamrg + '"' + i + '", '
        listamrg = listamrg.rstrip(', ')
        newdoc2 = newdoc.replace('//mrgMARCADOR','fotitomrg = [' + listamrg + '];')

        listamr = ''
        for i in imagenesmr:       
            listamr = listamr + '"' + i + '", '
        listamr = listamr.rstrip(', ')
        newdoc3 = newdoc2.replace('//mrMARCADOR','fotitomr = [' + listamr + '];')

        with open('galeriauma.html','w', encoding='utf-8') as f:
            f.write(newdoc3)

        # movimiento de las imagenes y archivos necesarios, desde el directorio raiz al de su alojamiento definitivo
        for i in imagenes:
            shutil.move(i, directorio)

        # creamos directorio para las imagenes de visualizaccion redimensionadas para ajustar tu peso y movemos a el dichas imagenes
        dirmrg = directorio + '/mrg'
        os.mkdir(dirmrg)
        for i in imagenesmrg:
            shutil.move(i, dirmrg)

        # creamos directorio para miniaturas y las movemos al mismo
        dirmr = directorio + '/mr'
        os.mkdir(dirmr)
        for i in imagenesmr:
            shutil.move(i, dirmr)

        shutil.move('galeriauma.html', directorio)
        rb = 'https://osm.uma.es/galeriador/media/'  # <------------ ruta en servidor de produccion
        link = rb + directorio + '/galeriauma.html'

    os.chdir(ruta)

    return link
    #--------------------------------------------------------------------------------------------------------