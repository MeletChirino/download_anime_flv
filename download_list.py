'''
Programa para descargar listas de animes de anime flv
'''
import requests
import os
from function_downloadZippy import get_mango_mp4 #mango.get_mp4() mango.get_link()
from function_downloadZippy import get_zippy_mp4 #zippy.get_mp4() zippy.get_link()
#OpenLoad.get_mp4() OpenLoad.get_link() Mega.get_link() Mega.download()
from function_downloadZippy import get_zippy_link
from function_downloadZippy import get_mango_link
from function_downloadZippy import create_info_file
from function_downloadZippy import get_episodes_list
from function_downloadZippy import printing
from function_downloadZippy import trim_link
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#import wget


def download_link(link_1):
    print 'Bienvenidos\n'
    #link_1 = raw_input('Que anime deseas descargar?\n')
    print link_1 + '\n'
    global driver
    #options = Options()
    #options.headless = True
    driver = webdriver.Chrome()
    cap_list = get_episodes_list(link_1, driver)
    print "Capitulos encontrados"
    print cap_list
    create_info_file(cap_list) #crear el archivo info que guarda la informacion importante de la serie
    caps = len(cap_list) #este comando me da la cantidad de capitulos
    i = 3
    zippy_link = []
    ajuste = 4 #hay que hacer un ajuste de 3 al momento de descargar
    print 'numero de capitulos = ' + str(caps)
    while i < caps - 1:
        if(cap_list[i][-1] == '#'):
            i += 1
            ajuste = 5 #si esta en emision hay que hacer un ajuste de 4 al momento de descargar
        print "\n\nObteniendo link mp4 del capitulo " + str(i)
        linky = get_zippy_link(cap_list[i], driver)
        print "Obteniendo link mp4: " + linky
        print linky != "Fail"
        if linky != "Fail":
            linky = get_zippy_mp4(linky, driver)
            print "Obteniendo link mp4: " + linky
        if(linky == "Fail"):
            #Try download thru mango
            print "Zippy fallo, intentando con mango"
            linky = get_mango_link(cap_list[i], driver)
            print "Obteniendo link mp4"
            if linky != "Fail":
                linky = get_mango_mp4(linky, driver)
        if (linky == "Fail"):
            print "Mango Fallo, intentando con OpenLoad"
            #colocar aqui adentro las funciones de openload

        zippy_link.append(linky)
        i+=1
    driver.quit()
    #aqui comienza el proceso de descarga
    printing(zippy_link)
    print "Zippy link con " + str(len(zippy_link))
    i = caps - ajuste - 1
    print zippy_link
    numero_de_capitulo = 1
    print "\ni = " + str(i)
    name = cap_list[0]
    new_path = "/home/melet/Videos/" + name
    while i >= 0:
        downloaded = False
        url = zippy_link[i]
        print '\ndescargando capitulo ' + str(numero_de_capitulo)
        print 'link = ' + url
        name_path = new_path + "/Episode-" + str(numero_de_capitulo) + ".mp4"
        print 'Guardando en ' + name_path
        #primero revisa a ver si el archivo ya esta Descargado
        downloaded = os.path.isfile(name_path)
        if downloaded:
            print "Archivo ya descargado"
        while not downloaded:#mientras no este descargado el archivo haga esto
            try:
                r = requests.get(url)
                with open(name_path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    command = "echo -ne '\007'"
                    os.system(command)
                    downloaded = True
                    numero_de_capitulo += 1
                print "Descargado"
            except Exception as e:
                print 'error'
                print e
                print 'descargando el archivo nuevamente'
        i -= 1
    command = "echo -ne '\007'"
    os.system(command)
    os.system(command)
    print link_1
    pass

def main():
    #
    proximas = [
    'https://animeflv.net/anime/5297/relife',
    'https://animeflv.net/anime/3935/kono-subarashii-sekai-ni-shukufuku-wo',
    'https://animeflv.net/anime/4658/noragami',
    'https://animeflv.net/anime/5437/shingeki-no-bahamut-genesis',
    'https://animeflv.net/anime/3397/saenai-heroin-no-sodatekata',
    'https://animeflv.net/anime/3808/haikyuu',
    'https://animeflv.net/anime/2989/plastic-memories',
    'https://animeflv.net/anime/3655/samurai-champloo',
    'https://animeflv.net/anime/281/cowboy-bebop',
    #'https://animeflv.net/anime/1374/akira', No se que paso
    #'https://animeflv.net/anime/395/moshidora', Solo se puede descargar por mega
    ]
    loop = len(proximas)
    i = 0
    while i < loop:
        download_link(proximas[i])
        i+=1


if __name__== "__main__":
    #import_packages()
    main()


    '''
    command = 'wget ' + zippy_link[i] + ' -P ' + new_path
    #command = 'wget ' + zippy_link[i]
    print "\nEjecutando " + command
    os.system(command)
    '''
