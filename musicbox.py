# -*- coding: utf-8 -*-
#Code by monsunalb

import os, urllib2, youtube_dl, datetime, shutil, time, sys


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    if count == total:
        print
    sys.stdout.flush()



def busca(text):
    lst = []
    cnt = 1
    print "Obtenint informació..."
    for grup in text:
        
        response = urllib2.urlopen("https://www.youtube.com/results?search_query="+grup)
        html = response.read()
        llista = html.split("/watch?")
        llista2 = []
        for vid in llista:
            llista2.append("/watch?" + vid[0:13])
        lst.append(llista2[1:2])
        progress(cnt,len(text))
        cnt +=1
    return lst

def entrainfo(tipus,prompt,error):
    entrada = raw_input(str(prompt)+"\n>>")
    if tipus == "int":
        try:
            entrada = int(entrada)
        except:
            print "Tipus invalid\n"+str(error)
            return entrainfo(tipus,prompt,error)
    return entrada

def estructurainfo(canco,artista):
    data = (canco + " " + artista).replace(" ","+")
    return data

def readfile(filename):
    lst = []
    lst2 = []
    lst3 = []
    fitxer = open(filename,"r")
    lines = fitxer.readlines()
    for line in lines:
        canco,artista= line.split("%%")
        lst.append(estructurainfo(canco,artista[:-1]))
        lst2.append(canco)
        lst3.append(artista)
    return lst,lst2,lst3

def readuser():
    lst = []
    lst2 = []
    lst3 = []
    seguir = 0
    while seguir != "N":
        canco = entrainfo("text","Canço","")
        artista = entrainfo("text","Artista","")
        seguir = entrainfo("text","Vols seguir afegint cançons?\n[S]/N","").upper()
        lst.append(estructurainfo(canco,artista))
        lst2.append(canco)
        lst3.append(artista)
    return lst,lst2,lst3

def download(item,artista,canco):
    conjunt = artista +"@" +canco
    a = 'youtube-dl --extract-audio --audio-format mp3 --output "'+conjunt+'.%(ext)s" http://www.youtube.com'+item
    os.system(a)




def main():
    count = 0
    source = entrainfo("text","Origen de la informació\n[0]Terminal/(1)Fitxer","Ha de ser un 0 o un 1")
    if source == "1":
    	print "Recorda que el format és CANÇÓ%%ARTISTA per linia"
        lectura = readfile(entrainfo("text","Fitxer",""))
    else:
        lectura = readuser()
    result = busca(lectura[0])
    cancons = lectura[1]
    artistes = lectura[2]


    try:
        time = datetime.datetime.now().strftime("music download %m-%d %H:%M")
        file = time 
        os.mkdir(file)
    except:
        file = entrainfo("text","La carpeta de destí " + str(time) + " ja existeix, Especifica el nom de la carpeta","")
        os.mkdir(file)
    for item in result:
        download(str(item[0]),artistes[count],cancons[count])
        filename = artistes[count]+"@"+cancons[count]+".mp3"
        shutil.move(filename,file)  
        count += 1
    os.system("clear")
    if count > 1:
        msgend = "Trobaras les %s cançons a /%s"%(count,file)
    else:
        msgend = "Trobaras la cançó a "+file
    print msgend
    os.system("notify-send \'Fet!!\' \'"+msgend+"\'")

main()
