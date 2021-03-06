"""
Cliente de descargas de animeflv.com
"""
#import tkinter
import requests
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

mother_path = '/home/melet/Videos/Animes'

class anime:
    '''
    atributos: name, state, capitulos[], driver, numero_de_capitulos, cover
    metodos: check_url() download() info_file() get_cover()
    '''
    def __init__(self, url):

        headless = raw_input('Desea ver el driver?(y/n)')
        if headless == 'Y' or headless == 'y' or headless == 'yes' or headless == 'Yes':
            self.driver = webdriver.Chrome()
        else:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

        check_url(self.driver, url, 5, '//*[@id="episodeList"]')
        #busca el nombre del anime
        self.name = str(self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/h2').text)
        #busca el estado del anime
        self.state = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/aside/p/span').text
        #busca la sinopsis del anime
        self.sinopsis = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/main/section[1]/div[2]').text
        # busca los links de los capitulos del animes
        self.capitulos = []
        xpath_index = 1
        epis = True
        while epis:
            try:
                # Este try busca los capitulos uno por uno en la tabla, en el caso de ser un solo capitulo saltara al
                # siguiente try
                xpath = '//*[@id="episodeList"]/li[' + str(xpath_index) + ']/a' #
                links = str(self.driver.find_element_by_xpath(xpath).get_attribute('href'))
                if (links == '#'):
                    xpath_index += 1
                if (xpath != ''):
                    print 'capitulo ', xpath_index, ' ', links, 'xpath=', xpath
                self.capitulos.append(links)
                xpath_index += 1

            except NoSuchElementException:
                try:
                    '''
                    Este try solo existe porque cuando el anime es una pelicula no encuentra el xpath de arriba
                    '''
                    xpath = '//*[@id="episodeList"]/li/a'
                    links = str(self.driver.find_element_by_xpath(xpath).get_attribute('href'))
                    print  'capitulo ', xpath_index , '', links
                    self.capitulos.append(links)
                    epis = False
                except NoSuchElementException:
                    epis = False
                    print "No hay capitulos disponibles"
                epis = False
                print "\nNo hay mas capitulos disponibles"
            except Exception as e:
                epis = False
                print "error: "
                print e # este while extrae los capitulos uno por uno
        self.numero_de_capitulos = xpath_index - 1#self.driver.quit()
        self.info_file()
        self.cover = self.get_cover()

    def info_file(self):
        #crear carpeta
        path = mother_path + '/' + self.name
        print 'guardando en ' + path
        if (not os.path.isdir(path)):
            #si no existe el path, lo crea
            print "Anime no descargado aun, creando carpeta\n" + path
            os.mkdir(path)
        else:
            print "Al parecer ya habias descargado este anime"
            os.system('pause')
        name_path = path + '/info.md'
        #Escribir archivo en path
        if os.isfile(name_path):
            print 'archivo info.md ya esta creado'
            return None
        with open(name_path, 'wb') as f:
            f.write(self.name.encode('utf-8') + '\n')
            f.write(self.state.encode('utf-8') + '\n')
            f.write(self.sinopsis.encode('utf-8') + '\n')
            f.write('Episodios:\n')
            caps = len(self.capitulos)
            i = caps - 1
            while i > 2:
                f.write(self.capitulos[i].encode('utf-8') + '\n')
                i -= 1
            f.close()
        return None

    def get_cover(self):
        timeout = 5
        attemps = 0
        print 'getting cover'
        while attemps < 3:
            try:
                href = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/aside/div[1]/div/figure/img')
                link = href.get_attribute('src').encode('ascii','ignore')
                print "link mp4: " + link
                r = requests.get(link)
                name_path = mother_path + "/" + self.name + '/cover.jpg'
                print 'Guardando cover en ' + name_path
                with open(name_path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                break
            except TimeoutException:
                attemps +=1
                print "Timed out waiting for page to load"
                fail = 'Fail'
                #return "Fail" # while que descarga la imagen
        return name_path

    def download(self):
        #
        server_name = ['Mango', 'Zippy', 'Openload', 'Mega']
        capitulo = self.numero_de_capitulos - 1
        cap = 1
        while capitulo >= 0:
            server_index = 0
            downloaded = False
            while not downloaded:# mientras no este descargado siga intentando con el siguiente servidor
                server = switcher.get(server_index, 'nothing')
                print "Probando con ", server_name[server_index]
                server.check(self.capitulos[capitulo], self.driver, cap, self.name)
                if server.available:
                    server.download()
                    cap += 1
                    downloaded = True
                    print 'Archivo descargado a traves de ', server_name[server_index]
                else:
                    server_index += 1
                    if serve_index >= 5:
                        downloaded = True
                        print "Error, ningun servidor funciona"

            capitulo -= 1

class mango:
    def __init__(self):
        pass

    def check(self, url, browser, capitulo, name):
        self.name = name #esta linea solo ingresa el nombre del anime, para tenerlo dentro de la class mango
        self.cap_number = capitulo #esta linea da el numero del capitulo, para tenerlo en cuenta dentro de la class mango
        # esta funcion sera como el get_mango_link
        print 'Accediendo a ' + url
        self.available = check_url(browser, url, 5, '//*[@id="XpndCn"]/div[2]/div[1]/span[3]')
        if not self.available:
            return False
        #Expandir tabla
        print 'expandiendo click en tabla'
        browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
        self.link =  revisar_tabla("Mango", browser)
        self.available = True
        if self.link == "Fail":
            self.available = False
            return self.available
        print 'Buscando link mp4'
        if not check_url(browser, self.link, 5, '//*[@id="mgvideo_html5_api"]'):
            return False
        href = browser.find_element_by_xpath('//*[@id="mgvideo_html5_api"]')
        link = href.get_attribute('src').encode('ascii','ignore')
        print "link mp4: " + link
        link = link.replace('https','http')
        self.link_mp4 = link

    def download(self):#metodo de descarga de mango
        #crear carpeta
        path = mother_path + '/' + self.name

        downloaded = False
        url = self.link_mp4
        print '\ndescargando capitulo ' + str(self.cap_number)
        print 'link = ' + url
        name_path = path + "/" + self.name + "-" + str(self.cap_number) + ".mp4"
        print 'Guardando en ' + name_path
        #primero revisa a ver si el archivo ya esta Descargado
        downloaded = os.path.isfile(name_path)
        if downloaded:
            print "Archivo ya descargado\nPor favor verifique el archivo"
        attemps = 1
        while not downloaded:#mientras no este descargado el archivo haga esto
            try:
                r = requests.get(url)
                with open(name_path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    command = "echo -ne '\007'"
                    os.system(command)
                    downloaded = True
                print "Descargado " + name_path
            except Exception as e:
                attemps += 1
                print 'error'
                print e
                print 'descargando el archivo nuevamente'
                if attemps >= 5:
                    print 'Maximo de intentos alcanzado'
                    downloaded = True

'''
class zippy: # Agregarle los xpath

    def check(self, url, browser):
        # esta funcion sera como el get_mango_link
        print 'Accediendo a ' + url
        self.available = check_url(browser, url, 5, '//*[@id="XpndCn"]/div[2]/div[1]/span[3]')
        if not self.available:
            return False
        #Expandir tabla
        print 'expandiendo click en tabla'
        browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
        self.link =  revisar_tabla("Zippyshare", browser)
        self.available = True
        if self.link == "Fail":
            self.available = False
            return self.available
        print 'Buscando link mp4'
        if not check_url(browser, self.link, 5, '//*[@id="mgvideo_html5_api"]'):#boton de descarga, cambiarlo
            return False
        href = browser.find_element_by_xpath('//*[@id="mgvideo_html5_api"]')#boton de descarga, cambiarlo
        link = href.get_attribute('src').encode('ascii','ignore')
        print "link mp4: " + link
        link = link.replace('https','http')
        self.link_mp4 = link


    def download(self):#metodo de descarga de mango
        print 'descargando ', self.link_mp4

class Openload: # Agregarle los xpath

    def check(self, url, browser):
        # esta funcion sera como el get_mango_link
        print 'Accediendo a ' + url
        self.available = check_url(browser, url, 5, '//*[@id="XpndCn"]/div[2]/div[1]/span[3]')
        if not self.available:
            return False
        #Expandir tabla
        print 'expandiendo click en tabla'
        browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
        self.link =  revisar_tabla("Zippyshare", browser)
        self.available = True
        if self.link == "Fail":
            self.available = False
            return self.available
        print 'Buscando link mp4'
        if not check_url(browser, self.link, 5, '//*[@id="mgvideo_html5_api"]'):#boton de descarga, cambiarlo
            return False
        href = browser.find_element_by_xpath('//*[@id="mgvideo_html5_api"]')#boton de descarga, cambiarlo
        link = href.get_attribute('src').encode('ascii','ignore')
        print "link mp4: " + link
        link = link.replace('https','http')
        self.link_mp4 = link


    def download(self):#metodo de descarga de mango
        print 'descargando ', self.link_mp4

class mega: # Cambiarle todo

    def check(self, url, browser):
        # esta funcion sera como el get_mango_link
        print 'Accediendo a ' + url
        self.available = check_url(browser, url, 5, '//*[@id="XpndCn"]/div[2]/div[1]/span[3]')
        if not self.available:
            return False
        #Expandir tabla
        print 'expandiendo click en tabla'
        browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
        self.link =  revisar_tabla("Zippyshare", browser)
        self.available = True
        if self.link == "Fail":
            self.available = False
            return self.available
        print 'Buscando link mp4'
        if not check_url(browser, self.link, 5, '//*[@id="mgvideo_html5_api"]'):#boton de descarga, cambiarlo
            return False
        href = browser.find_element_by_xpath('//*[@id="mgvideo_html5_api"]')#boton de descarga, cambiarlo
        link = href.get_attribute('src').encode('ascii','ignore')
        print "link mp4: " + link
        link = link.replace('https','http')
        self.link_mp4 = link


    def download(self):#metodo de descarga de mango
        print 'descargando ', self.link_mp4

'''
#***********************Funciones que usan todos los servidores************************

def check_url(browser, url, max_attemps, xpath):# solo devuelve valores de verdad, pero igual se puede ejecutar sin guardar el valor
        #esta funcion revisa la pagina, si funciona devuelve un valor de verdad, pero no es necesario guardarlo siempre
        attemps = 0
        timeout = 5
        print 'Esperando pagina'
        fail = 'ok'
        while attemps < max_attemps:
            try:
                browser.get(url)
                element_present = EC.presence_of_element_located((By.XPATH, xpath))
                WebDriverWait(browser, timeout).until(element_present)
                return True
                break
            except TimeoutException:
                attemps +=1
                print "Timed out waiting for page to load"
                fail = 'Fail'
        if attemps == max_attemps:
            return False
                #return "Fail"

def trim_link(new_link):
    new = new_link.replace("%2F","/")
	#print(new)
    new = new.replace("%3A",":")
    new = new.replace('%23','#')
    new = new.replace('%21','!')
	#print(new)
    link = new.partition('s=')
	#print(link[2])
    url = link[2]
    return url # quita los simbolos raros de los links

def revisar_tabla(server_name, browser):
    '''si la encuentra
    return "download_link"
    #si no la encuentra
    return "Fail"
    '''
    xpath_index = 1
    find = False #me da el valor de verdad si ya encontro el link de mango
    while not find: #mientras NO lo encuentre seguira probando
        print 'revisando tabla'
        xpath = '//*[@id="DwsldCn"]/div/table/tbody/tr[' + str(xpath_index) + ']/td[1]'
        link = browser.find_element_by_xpath(xpath).text
        print 'nombre encontrado ' + link
        if(xpath_index >= 4):
            return "Fail"
        if(str(link) == server_name):
            print 'link = ' + str(link)
            print server_name, " encontrado!"
            find = True
        else:
            xpath_index += 1
        pass
    print "tomando link"
    xpath = xpath.replace('td[1]','td[4]/a')
    link = browser.find_element_by_xpath(xpath)
    print 'link encontrado: '
    d_link = str(link.get_attribute('href'))
    print d_link
    print 'recortando link'
    d_link = trim_link(d_link)
    return d_link

switcher = {
    0: mango(),
    #1: zippy(),
    #2: openload(),
    #3: Mega()
    }

def main():

    #animes = anime('https://animeflv.net/anime/5480/ulysses-jehanne-darc-to-renkin-no-kishi')
    link = raw_input('Por favor coloque el link del anime a descargar\n')
    if( link == 'exit'):
        sys.exit()
    animes = anime(link)
    print "preparando descarga"
    os.system("echo -ne '\007'")
    os.system('pause')
    try:
        print "Nombre  = ", animes.name
        anime.info_file()
        print "\nEstado = ", animes.state
        print "\nSinopsis = ", animes.sinopsis
        print '\nCapitulos = ', animes.capitulos
        print '\nDescargando ', animes.download()
        animes.driver.quit()
    except Exception as er:
        print "Error inesperado\n"
        print er
        animes.driver.quit()
        sys.exit()

if __name__== "__main__":
    main()
