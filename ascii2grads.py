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

import struct # per scrivere file binari
import getopt
space = re.compile(r'\s+')
multiSpace = re.compile(r"\s\s+")

# debug
# 0 = only short message (Quiet mode) 
# 1 = a lot of print message (Verbose mode) 
debug=0


def checkpathfile(time_steps,path,title_file,data_read,utc,file_format,interval):
    i=0
    data_check=data_read
    if debug==1:
        print("Start checking {0}_ files existing".format(title_file))
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
    nomefile1 = ''
    time_steps= ''
    interval= ''
    variables=''
    title_output=''
    output_path=''
    output_variables=''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "mi:t:h:v:o:p:z:", ["help", "ifile=", "time_steps=", "interval=","vars"])
    except getopt.GetoptError:
        manual= 'ascii2grids.py -i <nomefile1> -t <TDEF number of time to consider> -h <TDEF interval in hours> -z < output_var, [var,..] [-v <var,[var,..]> -o <output_title_file> -p <ouput_path_file>'
        if debug==1:
            print(manual)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-m':
            print(manual)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            nomefile1 = arg
        elif opt in ("-t", "--time_steps"):
            time_steps = arg
        elif opt in ("-h", "--interval"):
            interval = arg
        elif opt in ("-v", "--interval"):
            variables = arg
        elif opt in ("-z", "--interval"):
            output_variables = arg   
        elif opt in ("-o", "--interval"):
            title_output = arg    
        elif opt in ("-p", "--interval"):
            output_path = arg     
    if nomefile1=='':
        print('ERROR: specify an input file')
        sys.exit()
    if time_steps=='':
        print('ERROR: specify a time step (also 1 is allowed)')
        sys.exit()
    if interval=='':
        print('ERROR: specify the time interval (e.g hours=1)')
        sys.exit()
    if output_variables=='':
        print('ERROR: specify the name of the output variable(s) in the ctl file')
        sys.exit()  
    if debug==1:
        print('Input file is ', nomefile1)
        print('Time step: ', time_steps)
        print('Hour Interval: ', interval)    
    # output variables name
    vars_array_o=output_variables.split(',')
    n_vars_o=len(vars_array_o)
    # input additional variables prefix 
    # WK: (the first variable is requested and is given using the -i option)
    if variables!='':
        vars_array=variables.split(',')
        n_vars=len(vars_array)
        if debug==1:
            print('Variables={0} n_vars={1}'.format(variables,n_vars))
    else:
        n_vars=0
    if (n_vars>n_vars_o-1):
        print('ERROR: you have {0} variables  ha'.format((n_vars+1),_n_vars_o))
        sys.exit()
    
    #print 'Output file is "', outputfile

    #exit()



    
    file_name_temp= nomefile1.split('/')
    k=len(file_name_temp)
    i=1
    path=file_name_temp[0]   
    while i<k-1:
        path="{0}/{1}".format(path,file_name_temp[i])
        i+=1
    if output_path =='': # check if title output file name is given or not, if not initilize to input title_file
        output_path="{0}".format(path)
        if debug==1:
            print(output_path)
    if debug==1:
        print("Path: ",path)
        print("Output path: ",output_path)
    file_name=file_name_temp[k-1]    
    
    file_time= file_name.split('_')
    if debug==1:
        print(file_time)
    title_file=file_time[0]
    if title_output=='': # check if title output file name is given or not, if not initilize to input title_file
        title_output=title_file
    data_file=file_time[1].split('.')
    file_format=data_file[1]
    data_temp=data_file[0].split('UTC')
    
    
    
    data_file=data_temp[0]
    if debug==1:
        print(data_file)
    #data_read=time.strptime(data_file,"%Y%m%d%H")
    #print data_read
    data_read=datetime.datetime.strptime(data_file,"%Y%m%d%H")
    if debug==1:
        print(data_read)
    
    #strptime("30 Nov 00", "%d %b %y")
    #data_read=data_file.strftime("%Y%m%d%H")
    #print data_read
    
    
    
 
            
    # gestione time zone
    #print len(data_temp[1])
    utc=data_temp[1]
    sign_temp=utc.split('s')
    sign_check=len(sign_temp[0])
    if debug==1:
        print(data_temp[1].split('s'))
        print(sign_temp[1])
    if (sign_check==3):
        utc_zone=int(sign_temp[1])
    elif (sign_check==4):
        utc_zone=int(sign_temp[1])*-1
    else:
        print('ERROR: invalid UTC time')
        sys.exit()     
 
    # calcolo data_write (sbagliato.. interpretato male i dati e scrivevamo come data_write quella finale, invece nel file ctl ci vuole la data iniziale)
    #data_read_z=data_read+datetime.timedelta(hours=int(utc_zone))
    #calcolo la data correttamemnte usando time_steps
     
    data_read_z=data_read-datetime.timedelta(hours=int(time_steps)-1)
    data_write=data_read_z.strftime("%H:%Mz%d%b%Y").lower() # lower è per rendere minuscolo l'output di %b che in realtà sarebbe maiuscolo (vd. libreria python-time)
    if debug ==1:
        print(data_write)
    #exit()
    
    
    if int(time_steps)>1:
        checkpathfile(time_steps,path,title_file,data_read,utc,file_format,interval)
        j=0
        while j<n_vars:
            checkpathfile(time_steps,'',vars_array[j],data_read,utc,file_format,interval)
            j+=1
    else:
        j=0
        while j<n_vars:
            data_file_new=data_read.strftime("%Y%m%d%H")
            namefile_check="{0}_{1}UTC{2}.{3}".format(vars_array[j],data_file_new,utc,file_format)
            j+=1
            if debug==1:
                print(namefile_check)
            if os.path.isfile(namefile_check)==False:
                print "ERROR: file {0} doesn't exist".format(namefile_check)
                sys.exit() 
    
    #UTC_zone=
        
    ########################################################
    # scrivere file .ctl
    ########################################################
    if debug==1:
        print("Inizio a leggere il file {0} (solo intestazione) per scrivere file ctl".format(nomefile1))
    f = open(nomefile1, 'r') # 'r' = read
    if debug==1:
        print(nomefile1)
    i=0
    while i<6:
        for riga in file(nomefile1): 
            line = riga
            #print i
            a = line.split()
            if i==0:
                ncols=int(a[1])
            if i==1:
                nrows=int(a[1])
            if i==2:
                xllcorner=float(a[1])           
            if i==3:
                yllcorner=float(a[1])
            if i==4:
                cellsize=float(a[1])
            if i==5:
                NODATA_value=float(a[1]) 
            i+=1
    f.seek(0)
    f.close()
    #scriviamo file .ctl
    #DSET /home/meteo/programmi/interpolazione_statistica/oi_fwi/temp/20180916plzln_g.dat 
    #TITLE  TITOLO
    #UNDEF  -9999.000
    #XDEF  177 LINEAR 1436301.37500000 1500.00000000000
    #YDEF  174 LINEAR 4916704.50000000 1500.00000000000
    #ZDEF  1 LINEAR 1.000000 1.000000
    #TDEF 24 LINEAR 13:00Z16sep2018 1HR
    #VARS  3
    #xpa  0  99  prec analysis
    #xidiw  0  99  idi wet
    #xidid  0  99  idi dry
    #ENDVARS
    
    ########################################################
    #l'output_path andrebbe reso assoluto anzichè relativo?
    ########################################################
    #controllo il titolo e nel caso cambio quello del ctl
    if title_output=='tdrh_g':
        title_output_ctl='rhtd_g'
    elif title_output=='plzln_g':
        title_output_ctl='raintana11_g'
    elif title_output=='CUMplzln_g':
        title_output_ctl='CUMraintana11_g'
    else:
        title_output_ctl=title_output

    nomefile_ctl="{0}/{1}.ctl".format(output_path,title_output_ctl)
    if debug==1:
        print("Inizio a scrivere il file {0}".format(nomefile_ctl))
    data_file_output=data_read_z.strftime("%Y%m%d")
    nomefile_dat="{0}/{1}{2}.dat".format(output_path,data_file_output,title_output)
    #nome_path_milanone="/home/meteo/programmi/interpolazione_statistica/oi_fwi/temp" #marta- mhhh, non ha funzionato... 
    #nomefile_dat="{0}/{1}{2}.dat".format(nome_path_milanone,data_file_output,title_output)   
    nomefile_dat_nopath="^{1}{0}.dat".format(title_output,data_file_output)
    # se volessi creare un file grads effettivamente leggibile sarebbe da sostituire a nomefile_milanone
    ####################################################################################
    # PARTE CHE RENDE I FILE CONGRUENTI CON LA STRUTTURA DI MILANONE
    # (rende leggibile il file solo da MILANONE)
    nome_path_milanone="/home/meteo/programmi/interpolazione_statistica/oi_fwi/temp"
    nomefile_milanone="{0}/{1}{2}.dat".format(nome_path_milanone,data_file_output,title_output)
    ####################################################################################
    ctl = open(nomefile_ctl, 'w') # 'r' = read 
    #ctl.write("DSET {0}".format(nomefile_dat_nopath))
    ctl.write("DSET {0}".format(nomefile_milanone))
    ctl.write("\nTITLE {0}".format(title_output))
    ctl.write("\nUNDEF {0}".format(NODATA_value))
    ctl.write("\nXDEF {0} LINEAR {1} {2}".format(ncols,xllcorner,cellsize))
    ctl.write("\nYDEF {0} LINEAR {1} {2}".format(nrows,yllcorner,cellsize))
    ctl.write("\nZDEF  1 LINEAR 1.000000 1.000000") #!! per ora funziona solo per file grads 2D senza dimensione Z
    ctl.write("\nTDEF {0} LINEAR {1} {2}HR".format(time_steps,data_write,interval))
    ctl.write("\nVARS {0}".format(n_vars+1))
    ctl.write("\n{0}  0  99  {1}".format (vars_array_o[0],title_output))
    j=0
    while j<n_vars:
        ctl.write("\n{0}  0  99  {1}".format (vars_array_o[j+1],vars_array[j]))
        j+=1
    ctl.write("\nENDVARS")
    if debug==1:
        print("ncols={0}, nrows={1}, xllcorner={2}, yllcorner={3},cellsize={4},NODATA_value={5}".format(ncols,nrows,xllcorner,yllcorner,cellsize,NODATA_value))
    ctl.close()
    #lines = f.read()
    #print lines
    #f.close()
    
    
    ########################################################
    # scrivere file .dat
    ########################################################
    
    # ciclo sui tempi 
    # ciclo sulle variabil
    
    # con questi apriamo il file giusto, poi lo leggiamo riga per riga dall'alto verso il basso
    # lo riscriviamo con la regola seguente
    # scrive per ciascuna variabile la matrice riga per riga dal basso verso l'alto
    t=1
    data_zero=data_read-datetime.timedelta(hours=int(time_steps))
    while t <= int(time_steps):
        avanti=t*int(interval)
        if debug==1:
            print("Time {0}".format(avanti))
        data_check=data_zero + datetime.timedelta(hours=avanti)
        #print data_check
        data_file_new=data_check.strftime("%Y%m%d%H")
        if debug==1:
            print(data_file_new)
            print("Read variable {0}".format(title_file))
        nomefile="{0}/{1}_{2}UTC{3}.{4}".format(path, title_file,data_file_new,utc,file_format)
        if t==1:
            legge_e_stampa(nomefile, nomefile_dat, 'FALSE' )
        else:
            legge_e_stampa(nomefile, nomefile_dat, 'TRUE' )
        #exit()
        v=0
        while v<n_vars:
            vars_tmp=vars_array[v].split('/')
            if debug==1:
                print("Read variable {0}".format(vars_array[v]))
            nomefile="{0}_{1}UTC{2}.{3}".format(vars_array[v],data_file_new,utc,file_format)
            legge_e_stampa(nomefile, nomefile_dat, 'TRUE' )
            v+=1
        t=t+int(interval)
            
        
        
    #exit()
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
