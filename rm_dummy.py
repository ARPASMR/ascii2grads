#! /usr/bin/env python
# -*- coding: utf-8 -*-
#   Gter Copyleft 2018
#   Roberto Marzocchi, Lorenzo Benvenuto

import glob, os
for f in glob.glob("/home/meteo/programmi/interpolazione_statistica/oi_ascii/archivio_ascii/ascii2grads/dummy*.txt"):
    os.remove(f)
