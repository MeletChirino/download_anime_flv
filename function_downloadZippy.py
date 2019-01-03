"""
Funciones utiles para decargar animes desde animeflv
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
# ------------------ Hacer funciones de Mega que dejen el archivo listo para descargar

# ------------------ Funciones de openload
'''
def get_mango_mp4(url, browser):
    print 'accediendo a la pag...'
    #iniciando intentos de carga de pagina
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'esperando boton de descarga'
    while attemps < 5:
        try:
            browser.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="mgvideo_html5_api"]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            if attemps >= 5:
                print 'Maximo de intentos alcanzado'
                return 'Fail'

    href = browser.find_element_by_xpath('//*[@id="mgvideo_html5_api"]')
    link = href.get_attribute('src').encode('ascii','ignore')
    print "link mp4: " + link
    #link =
    link = link.replace('https','http')
    return link


def get_zippy_link(url, browser):
    """
    primero hay que darle click a la tabla //*[@id="XpndCn"]/div[2]/div[1]/span[3]/span
    """
    print 'accediendo a la pagina'
    xpath_index = 1
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'esperando tabla'
    while attemps < 5:
        try:
            browser.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="DwsldCn"]/div/table/tbody/tr[1]/td[1]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            if attemps >= 5:
                print 'Maximo de intentos alcanzado'
                return 'Fail'
    print 'expandiendo click en tabla'
    browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
    find = False #me da el valor de verdad si ya encontro el link de zipy
    while not find:#mientras NO lo encuentre seguira probando
        print 'revisando tabla'
        try:
            xpath = '//*[@id="DwsldCn"]/div/table/tbody/tr[' + str(xpath_index) + ']/td[1]'
            link = browser.find_element_by_xpath(xpath).text
            print 'nombre encontrado ' + link
        except NoSuchElementException:
            print "Zippy no encontrado"
            return "Fail"
        if(xpath_index >= 4):
            return "Fail"
        if(str(link) == 'Zippyshare'):
            print "Zippyshare encontrado!"
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
'''
# ------------------
def download_zippy(url, browser):
    print 'accediendo a la pag...'
    browser.get(url)
    #iniciando intentos de carga de pagina
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'esperando boton de descarga'
    while attemps < 3:
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//a[@id="dlbutton"]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            if attemps >= 5:
                print 'Maximo de intentos alcanzado'
                return 'Fail'

    href = browser.find_element_by_xpath('//a[@id="dlbutton"]')
    link = href.get_attribute('href').encode('ascii','ignore')
    link = link.replace('https','http')
    command = 'wget ' + link
    print "Ejecutando " + command
    os.system(command)
    pass

def get_zippy_link(url, browser):
    """
    primero hay que darle click a la tabla //*[@id="XpndCn"]/div[2]/div[1]/span[3]/span
    """
    print 'accediendo a la pagina'
    xpath_index = 1
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'esperando tabla'
    while attemps < 5:
        try:
            browser.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="DwsldCn"]/div/table/tbody/tr[1]/td[1]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            if attemps >= 5:
                print 'Maximo de intentos alcanzado'
                return 'Fail'
    print 'expandiendo click en tabla'
    browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
    find = False #me da el valor de verdad si ya encontro el link de zipy
    while not find:#mientras NO lo encuentre seguira probando
        print 'revisando tabla'
        try:
            xpath = '//*[@id="DwsldCn"]/div/table/tbody/tr[' + str(xpath_index) + ']/td[1]'
            link = browser.find_element_by_xpath(xpath).text
            print 'nombre encontrado ' + link
        except NoSuchElementException:
            print "Zippy no encontrado"
            return "Fail"
        if(xpath_index >= 4):
            return "Fail"
        if(str(link) == 'Zippyshare'):
            print "Zippyshare encontrado!"
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

def get_zippy_mp4(url, browser):
        print 'accediendo a la pag...'
        #iniciando intentos de carga de pagina
        attemps = 0 #intentos para que la pag cargue
        timeout = 5
        print 'esperando boton de descarga'
        while attemps < 5:
            try:
                browser.get(url)
                element_present = EC.presence_of_element_located((By.XPATH, '//a[@id="dlbutton"]'))
                WebDriverWait(browser, timeout).until(element_present)
                break
            except TimeoutException:
                attemps +=1
                print "Timed out waiting for page to load"
                if attemps >= 5:
                    print 'Maximo de intentos alcanzado'
                    return 'Fail'

        href = browser.find_element_by_xpath('//a[@id="dlbutton"]')
        link = href.get_attribute('href').encode('ascii','ignore')
        link = link.replace('https','http')
        print 'link encontrado: ' + link
        return link

def get_mango_link(url, browser):
    """
    primero hay que darle click a la tabla //*[@id="XpndCn"]/div[2]/div[1]/span[3]/span
    """
    print 'accediendo a la pagina'
    xpath_index = 1
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'esperando tabla'
    while attemps < 5:
        try:
            browser.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="DwsldCn"]/div/table/tbody/tr[1]/td[1]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            if attemps >= 5:
                print 'Maximo de intentos alcanzado'
                return 'Fail'
    print 'expandiendo click en tabla'
    browser.find_element_by_xpath('//*[@id="XpndCn"]/div[2]/div[1]/span[3]/span').click()# hay qye hacer click para que se abra la tabla
    find = False #me da el valor de verdad si ya encontro el link de zipy
    while not find:#mientras NO lo encuentre seguira probando
        print 'revisando tabla'
        xpath = '//*[@id="DwsldCn"]/div/table/tbody/tr[' + str(xpath_index) + ']/td[1]'
        link = browser.find_element_by_xpath(xpath).text
        print 'nombre encontrado ' + link
        if(xpath_index >= 4):
            break
        if(str(link) == 'Mango'):
            print 'link = ' + str(link)
            print "Mango encontrado!"
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

def get_mango_mp4(url, browser):
    print 'accediendo a la pag...'
    #iniciando intentos de carga de pagina
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'esperando boton de descarga'
    while attemps < 5:
        try:
            browser.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="mgvideo_html5_api"]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            if attemps >= 5:
                print 'Maximo de intentos alcanzado'
                return 'Fail'

    href = browser.find_element_by_xpath('//*[@id="mgvideo_html5_api"]')
    link = href.get_attribute('src').encode('ascii','ignore')
    print "link mp4: " + link
    #link =
    link = link.replace('https','http')
    return link

def create_info_file(lists):
    '''
    state = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/aside/p/span')
    sinopsis = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/main/section[1]/div[2]')
    '''
    name = lists[0]
    global new_path
    new_path = "/home/melet/Videos/" + name
    new_path = new_path.replace(' ','\ ')
    new_path = new_path.replace('(','\(')
    new_path = new_path.replace(')','\)')
    try:
        print 'creando carpeta ' + name + ' en ' + new_path
        command = 'mkdir ' + new_path
        print command
        os.system(command)
        series = open("series.txt", "a+")
        series.write(new_path + '\n')
        series.close()
    except FileExist:
        print 'La carpeta ya existe'
    except Exception as ex:
        message = template.format(type(ex).__name__, ex.args)
        print message
        #print "\nError"

    sinopsis = lists[2]
    state = lists[1]
    f = open(name + '.txt', 'w+')
    f.write(name.encode('utf-8') + '\n')
    f.write(state.encode('utf-8') + '\n')
    f.write(sinopsis.encode('utf-8') + '\n')
    f.write('Episodios:\n')
    caps = len(lists)
    i = caps - 1
    while i > 2:
        f.write(lists[i] + '\n')
        i -= 1
    f.close()
    command = name
    command = command.replace(' ','\ ')
    command = command.replace('(','\(')
    command = command.replace(')','\)')
    command = 'mv ' + command + '.txt '
    command = command + new_path
    print command
    os.system(command)


    pass

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
    return url

def get_episodes_list(url, browser):
    print 'accediendo a la pag...'
    #iniciando intentos de carga de pagina
    attemps = 0 #intentos para que la pag cargue
    timeout = 5
    print 'Esperando pagina'
    fail = 'ok'
    while attemps < 3:
        try:
            browser.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="episodeList"]'))
            WebDriverWait(browser, timeout).until(element_present)
            break
        except TimeoutException:
            attemps +=1
            print "Timed out waiting for page to load"
            fail = 'Fail'
            #return "Fail"
    if(fail == 'Fail'):
        pass
    episode_list = []
    #Busca el nombre del anime y lo coloca de primero en la lista resultante
    episode_list.append(str(browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/h2').text))
    #Busca el estado del anime y lo coloca en la lista resultante
    episode_list.append(browser.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/aside/p/span').text)
    #Busca la sinopsis del anime y lo coloca en la lista resultante
    episode_list.append(browser.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/main/section[1]/div[2]').text)
    print 'Nombre del anime: ' + episode_list[0]

    epis = True
    xpath_index = 1
    while epis:
        try:
            #//*[@id="episodeList"]/li[1]
            xpath = '//*[@id="episodeList"]/li[' + str(xpath_index) + ']/a'
            links = str(browser.find_element_by_xpath(xpath).get_attribute('href'))
            if (links != '#'):
                print links
                episode_list.append(links)
                xpath_index += 1
        except NoSuchElementException:
            try:
                xpath = '//*[@id="episodeList"]/li/a'
                links = str(browser.find_element_by_xpath(xpath).get_attribute('href'))
                print links
                episode_list.append(links)
                epis = False
            except NoSuchElementException:
                epis = False
                print "No hay capitulos disponibles"
            epis = False
            print "Capitulo"
        except Exception as e:
            epis = False
            print "error: "
            print e

    return episode_list

def printing(zip):
    print zip
    pass

def main():
    print 'Bienvenidos\n'
    link_1 = raw_input('Que anime deseas descargar?\n')
    print link_1 + '\n'
    global driver
    options = Options()
    options.headless = True
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
        #zippy_link.append(get_zippy_link(cap_list[i], driver))
        #zippy_link[i - 3] = get_zippy_link(cap_list[i], driver)
        linky = get_zippy_mp4(linky, driver)
        if(linky == "Fail"):
            #Try download thru mango
            print "Zippy fallo, intentando con mango"
            linky = get_mango_link(cap_list[i], driver)
            print "Obteniendo link mp4"
            linky = get_mango_mp4(linky, driver)
            #zippy_link.append(get_mango_link(cap_list[i], driver))
            #zippy_link[i - 3] = get_mango_mp4(zippy_link[i - 3], driver)
        zippy_link.append(linky)
        i+=1
    # i = len(zippy_link) - 1
    # # while i >= 0:
    # #     zippy_link[i] = get_zippy_mp4(zippy_link[i], driver)
    # #     i -= 1
    # #download_zippy(link_1, driver)
    driver.quit()
    printing(zippy_link)
    print "Zippy link con " + str(len(zippy_link))
    i = caps - ajuste - 1
    print zippy_link
    print "\ni = " + str(i)
    while i >= 0:
        command = 'wget ' + zippy_link[i] + ' -P ' + new_path
        #command = 'wget ' + zippy_link[i]
        print "\nEjecutando " + command
        os.system(command)
        i = i - 1
    command = "echo -ne '\007'"
    print link_1

if __name__== "__main__":
    main()
'''
  try:
      main()
  except Exception as e:
      print e# -*- coding: utf-8 -*-
      driver.quit()
'''
