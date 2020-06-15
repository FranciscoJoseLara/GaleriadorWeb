from django.http import HttpResponse
from django.shortcuts import render
from django import forms
import os, sys
import shutil
from PIL import Image

def force(request):

    #--------------------------------- CODIGO DE EJECUCION ---------------------------------------------------
    ruta = os.getcwd()
    contenido = os.listdir(ruta)
    '''
    cont = 0
    imagenes = []
    imagenesmrg = []
    imagenesmr = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta, fichero)) and (fichero.endswith('.jpg') or fichero.endswith('.JPG')
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
            if os.path.isfile(os.path.join(ruta, fichero)) and fichero == 'directorios':
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
        with open('album.html','r', encoding='utf-8') as f:
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
        copiar = directorio + '/estilos.css'
        shutil.copy('estilos.css', copiar)
    #--------------------------------------------------------------------------------------------------------
    '''
    context = ({
        'path': ruta, 
        'listado': contenido,
        'p1': ruta,
        'p2': contenido
        })

    return render(request, 'layout.html', context=context)

    #return HttpResponse("Hola mundo, estoy vivo")
def ejecutor(request):
    if request.method == 'POST':
        form = request.POST.get('interfaz')
        #color = form['interfaz'].value()
        context = ({'dato': form})
        return render(request, 'prueba.html', context=context)
    else:
        return Httpresponse('No Ok!')