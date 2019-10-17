#! /usr/bin/env python
# -*- coding: utf-8 -*-
#   Gter Copyleft 2018
#   Roberto Marzocchi, Lorenzo Benvenuto


# lo script è statto sviluppato per trasformare dei file raster ASCII (formato ESRI) --> a file griglia GRADS _g.ctl + relativi .dat
# input necessari:
# -i : nome_file ascii con l'indicazione dell'ora UTC seguita dall'indicazione del fuso di appartenenza  TITLE_YYYYMMDDHHUTCplusX.txt
# input (deve essere il dato finale)
# -t numero di step temporali da importare nel file dat --> integer (es. 24)
# -h intervallo di tempo espresso in ore --> integer (es. 1)
# input opzionali: 
# -v prefisso altre variabili da considerare separate da virgola 
# -o prefisso dei file GRADS di output (se non specificato il codice usa lo stesso prefisso dei file ASCII)
# -p percorso al file di output 

# !! il codice controlla l'esistenza dei file di input necessari secondo i parametri (t, d) specificati. 
# Ad esempio se indichiamo un file di input: TITLE_2018091500UTCplus1.txt , 24 come time step  --> 00:00 UTC del 15-09-2018 andrà a  cercarsi i 24 file corrispondenti agli step temporali precedenti



# -m --> manuale

#library added by GTER
import os,sys,re #,shutil,glob
#import time
#import urllib
import datetime #importo tutta la libreria
#from datetime import datetime, date, timedelta   #importa solo alcune funzioni della libreria datetime


from shutil import copyfile



import struct # per scrivere file binari
import getopt
space = re.compile(r'\s+')
multiSpace = re.compile(r"\s\s+")



def checkpathfile(time_steps,path,title_file,data_read,utc,file_format,interval):
    i=0
    data_check=data_read
    print "Start checking {0}_ files existing".format(title_file)
    while i < int(time_steps):
        if i>0:
            data_check=data_check -datetime.timedelta(hours=int(interval))
        else:
            data_check=data_check
        #print data_check
        data_file_new=data_check.strftime("%Y%m%d%H")
        if path=='':
            namefile_check="{0}_{1}UTC{2}.{3}".format(title_file,data_file_new,utc,file_format)
        else:
            namefile_check="{0}/{1}_{2}UTC{3}.{4}".format(path,title_file,data_file_new,utc,file_format)
        if os.path.isfile(namefile_check)==False:
            print "ERROR: file {0} doesn't exist".format(namefile_check)
            sys.exit() 
            # directory exists
        i+=1
        #print i


def legge_e_stampa(file_i,file_o,append):
    f_i = open(file_i, 'r') # 'r' = read
    #print "Ok 0"
    #print file_i
    righe=[]
    i=0
    #print "Ok 1"
    for riga in file(file_i): 
        line = riga
        #print i
        if i>5:
            colonne = line.split()
            righe.append(colonne)
        i+=1
    #ora devo scrivere su ff partendo dall'ultima riga
    f_i.close()
    #print "Ok 2"
    #print len(righe)
    k=1
    b = bytes()
    if append=='TRUE':
        ff = open(file_o, 'ab') # 'w+' = append to existing file
    else:
        ff = open(file_o, 'wb') # 'w+' = append to existing file
    while k<=len(righe):
        riga_w=len(righe)-k
        j=0
        while j<len(righe[riga_w]):
            #print riga_w,j,float(righe[riga_w][j])
            b=struct.pack('f',float(float(righe[riga_w][j])))
            ff.write(b)
            ff.flush()
            #b=b.join(struct.pack('<f',float(righe[riga_w][j])))
            j+=1
            #print b
            
            
            
        #b=b.join(struct.pack('f', float(val)) for val in righe)
        #print b 
        #print riga_w, righe[riga_w][176]
        
        k+=1
    #exit()
    f_i.close()
    ff.close




def main():
    path_mediano="/home/meteo/programmi/interpolazione_statistica/oi_ascii/archivio_ascii/ascii2grads"
    start_time = ''
    time_steps= ''
    interval= ''
    prefix=''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ms:t:h:p:", ["help", "start_time=", "time_steps=", "interval=","prefix"])
    except getopt.GetoptError:
        manual= 'ascii2grids.py -s <start time wirth the format of ascii file> -t <TDEF number of time to consider> -h <TDEF interval in hours> -p <prefix of file>'
        print manual
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-m':
            print 'manual'
            sys.exit()
        elif opt in ("-s", "--start time"):
            start_time = arg
        elif opt in ("-t", "--time_steps"):
            time_steps = arg
        elif opt in ("-h", "--interval"):
            interval = arg
        elif opt in ("-p", "--interval"):
            prefix = arg
    if start_time=='':
        print 'ERROR: specify a start time'
        sys.exit()
    if time_steps=='':
        print 'ERROR: specify a time step (also 1 is allowed)'
        sys.exit()
    if interval=='':
        print 'ERROR: specify the time interval (e.g hours=1)'
        sys.exit()
    if prefix=='':
        print 'ERROR: specify a prefix for dummy file '
        sys.exit()        
            
    print 'Time start is ', start_time
    print 'Time step: ', time_steps
    print 'Hour Interval: ', interval    
    file_time= start_time
    print file_time
    data_file=file_time.split('.')
    file_format=data_file[1]
    data_temp=data_file[0].split('UTC')
    
    
    
    data_file=data_temp[0]
    
    print data_file
    #data_read=time.strptime(data_file,"%Y%m%d%H")
    #print data_read
    data_read=datetime.datetime.strptime(data_file,"%Y%m%d%H")
    print data_read
    
    #strptime("30 Nov 00", "%d %b %y")
    #data_read=data_file.strftime("%Y%m%d%H")
    #print data_read
    
    
    
 
            
    # gestione time zone
    #print len(data_temp[1])
    utc=data_temp[1]
    sign_temp=utc.split('s')
    sign_check=len(sign_temp[0])
    print data_temp[1].split('s')
    print sign_temp[1]
    if (sign_check==3):
        utc_zone=int(sign_temp[1])
    elif (sign_check==4):
        utc_zone=int(sign_temp[1])*-1
    else:
        print 'ERROR: invalid UTC time'
        sys.exit()     
 
    # calcolo data_write (sbagliato.. interpretato male i dati e scrivevamo come data_write quella finale, invece nel file ctl ci vuole la data iniziale)
    #data_read_z=data_read+datetime.timedelta(hours=int(utc_zone))
    #calcolo la data correttamemnte usando time_steps
     
    data_read_z=data_read-datetime.timedelta(hours=int(time_steps)-1)
    data_write=data_read_z.strftime("%H:%Mz%d%b%Y").lower() # lower è per rendere minuscolo l'output di %b che in realtà sarebbe maiuscolo (vd. libreria python-time)
    
    
    
    i=0
    data_check=data_read
    print "Start creating files".format(prefix)
    while i < int(time_steps):
        if i>0:
            data_check=data_check -datetime.timedelta(hours=int(interval))
        else:
            data_check=data_check
        #print data_check
        data_file_new=data_check.strftime("%Y%m%d%H")
        namefile_check="{4}/{0}_{1}UTC{2}.{3}".format(prefix,data_file_new,utc,file_format,path_mediano)
        print namefile_check
        # deve sempre esserci il file con tutti i nulli con nome prefissato dummy_null.txt
        copyfile('{0}/DUMMY_NOT_REMOVE.txt'.format(path_mediano), namefile_check)
        i+=1
    #print data_write
    exit()
    
    
    
        
    #exit()
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
