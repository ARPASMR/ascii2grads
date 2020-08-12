#! /usr/bin/env python
# -*- coding: utf-8 -*-
#   Gter Copyleft 2018
#   Roberto Marzocchi, Lorenzo Benvenuto
#   Script for Python 2.7


import os,sys,re #,shutil,glob
import commands
import time
#import urllib
import datetime
import subprocess

#check if script is already running
def stop_if_already_running():
    script_name = os.path.basename(__file__)
    l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}' | awk '{print $2}'" % script_name)
    if l[1]:
        print('Script {0} is already running. Please check crontab or zombie process')
        # questa parte non funziona su mediano perchè credo ci sia una vecchia versione di logger
        #command_logger='logger -i -p user.error -s -t PREVISORE-T -P514 -n 10.10.0.15 "Errore script {0} sta già girando per qualche ragione. Controllare processi attivi su mediano"'.format(script_name)
        #os.system(command_logger)
        sys.exit(0);

stop_if_already_running()


# debug
# 0 = only short message (Quiet mode) 
# 1 = a lot of print message (Verbose mode) 
debug=0

# absolute path mediano
path="/home/meteo/programmi/interpolazione_statistica/oi_ascii/archivio_ascii"
path_d="{0}/ascii2grads".format(path)


#rimozione vecchi file dat
output_dir="{0}/grads_file".format(path)
rm_old_files="rm {0}/*.dat".format(output_dir)
p1=subprocess.Popen(rm_old_files, stdout=subprocess.PIPE, shell=True)
out1, err1 = p1.communicate() 
result = out1.split('\n')
# modifica per parametro della data:
# se passo una data come parametro nel formato AAAAMMGG allora il giorno di partenza diventa quello
if len(sys.argv)>1:
   dummy_start_data=datetime.datetime.strptime(sys.argv[1],"%Y%m%d")
   yd=dummy_start_data.strftime("%Y%m%d")
   print yd
else:
   yesterday = datetime.date.today()-datetime.timedelta(hours=int(24))
   print yesterday
   yd=yesterday.strftime("%Y%m%d")


data_start="{0}12UTCplus1.txt".format(yd)

print('run ascii2grads for {0}'.format(data_start))

crea_dummy="python {1}/crea_dummy.py  -s {0} -t 24 -h 1 -p dummy".format(data_start,path_d)

p2=subprocess.Popen(crea_dummy, stdout=subprocess.PIPE, shell=True)
out2, err2 = p2.communicate() 
result2 = out2.split('\n')
for lin in result2:
    if not lin.startswith('#'):
        print(lin)


#temperatura
#t2m_g.dat 
#t2m_g.ctl 
#con variabili 
#DUMMY: xb 0 99 T background field 
#DA ASCII: xa 0 99 T analysis field 
#DA ASCII: xidi 0 99 integral data influence 



#dummy version
#temperatura="python {0}/ascii2grads.py  -i {0}/dummy_{1} -t 24 -h 1 -v {2}/temperatura/TEMP2m,{2}/temperatura_IDI/T2mIDI -z xb,xa,xidi -o t2m_g -p {2}/grads_file".format(path_d,data_start,path)

#versione pulita
temperatura="python {0}/ascii2grads.py  -i {1}/temperatura/TEMP2m_{2} -t 24 -h 1 -v {1}/temperatura_IDI/T2mIDI -z xa,xidi -o t2m_g -p {1}/grads_file".format(path_d,path,data_start)

if debug==1:
    print temperatura

p3=subprocess.Popen(temperatura, stdout=subprocess.PIPE, shell=True)
out3, err3 = p3.communicate() 
result3 = out3.split('\n')
for lin in result3:
    if not lin.startswith('#'):
        print(lin)

#print "Fin qua OK"


#wind 

#dummy version
#wind="python {0}/ascii2grads.py  -i {0}/dummy_{1} -t 24 -h 1 -v {0}/dummy,{0}/dummy,{0}/dummy,{0}/dummy,{0}/dummy,{0}/dummy,{2}/vento/VU,{2}/vento/VV,{0}/dummy,{0}/dummy,{0}/dummy,{2}/vento_IDI/VVIDI -z dummy,dummy,dummy,dummy,dummy,dummy,dummy,ahu,ahv,dummy,dummy,dummy,xidi -o wind -p {2}/grads_file".format(path_d,data_start,path)


#versione pulita
wind="python {0}/ascii2grads.py  -i {1}/vento/VU_{2} -t 24 -h 1 -v {1}/vento/VV,{1}/vento_IDI/VVIDI -z ahu,ahv,xidi -o wind_g -p {1}/grads_file".format(path_d,path,data_start)


if debug==1:
    print wind

p4=subprocess.Popen(wind, stdout=subprocess.PIPE, shell=True)
out4, err4 = p4.communicate() 
result4 = out4.split('\n')
for lin in result4:
    if not lin.startswith('#'):
        print(lin)



#rh
#dummy version
#rh="python {0}/ascii2grads.py  -i {0}/dummy_{1} -t 24 -h 1 -v {0}/dummy,{0}/dummy,{2}/umiditarelativa/RH,{2}/umiditarelativa_IDI/RHIDI,{0}/dummy -z dummy,dummy,dummy,rha,xidi,dummy -o rhtd -p {2}/grads_file".format(path_d,data_start,path)

#versione pulita 
rh="python {0}/ascii2grads.py  -i {1}/umiditarelativa/RH_{2} -t 24 -h 1 -v {1}/umiditarelativa_IDI/RHIDI -z rha,xidi -o tdrh_g -p {1}/grads_file".format(path_d,path,data_start)


if debug==1:
    print rh

p5=subprocess.Popen(rh, stdout=subprocess.PIPE, shell=True)
#p5=subprocess.call(rh, stdout=subprocess.PIPE, shell=True)
#print(p5)
out5, err5 = p5.communicate(input=None, timeout=None)
#This makes the wait possible
#p_status5 = p5.wait()
#print(p_status5) 
result5 = out5.split('\n')
for lin in result5:
    if not lin.startswith('#'):
        print(lin)




#rain
rain="python {2}/ascii2grads.py  -i {0}/precipitazione/PR_{1} -t 24 -h 1 -v {0}/precipitazione_IDI/PRIDIW,{0}/precipitazione_IDI/PRIDID -z xpa,xidiw,xidid -o plzln_g -p {0}/grads_file".format(path,data_start,path_d)

if debug==1:
    print(rain)


p6=subprocess.Popen(rain, stdout=subprocess.PIPE, shell=True)
out6, err6 = p6.communicate(input=None, timeout=None)
#This makes the wait possible
#p_status6 = p6.wait() 
#print(p_status6)
result6 = out6.split('\n')
for lin in result6:
    if not lin.startswith('#'):
        print(lin)




#rain_cumulata
rain_cum="python {2}/ascii2grads_cumulata.py  -i {0}/precipitazione/PR_{1} -t 24 -h 1 -z rain -o CUMplzln_g -p {0}/grads_file".format(path,data_start,path_d)

if debug==1:
    print rain_cum


p7=subprocess.Popen(rain_cum, stdout=subprocess.PIPE, shell=True)
out7, err7= p7.communicate(input=None, timeout=None) 
#This makes the wait possible
#p_status7 = p7.wait()
#print(p_status7)
result7 = out7.split('\n')
for lin in result7:
    if not lin.startswith('#'):
        print(lin)






if debug==1:
    print("\n\n################################")
    print("Remove dummy")
# remove dummy
rm_dummy="python {0}/rm_dummy.py".format(path_d)

ret=os.system(rm_dummy)
if ret!=0:
    print(ret)
#p=subprocess.Popen(rm_dummy, stdout=subprocess.PIPE, shell=True)
#out, err = p.communicate() 
#result = out.split('\n')
#for lin in result:
#    if not lin.startswith('#'):
#        print(lin)

        
print("Fine script run_ascii2grads per la data {0}".format(yd))
