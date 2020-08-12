# ascii2grads
## scopo
Il codice viene eseguito da mediano (in crontab) e produce i file necessaari al funzionamento di FWI.

I file sono parte della procedura di produzione delle mappe AIB. Per maggiori dettagli consultare il repository https://github.com/ARPASMR/AIB/
## uso
```
python run_ascii2grads.py
```
esegue la cumulazione e la copia dei file riferiti alla data di ieri
```
python run_ascii2grads.py AAAAMMGG
```
esegue l'operazione riferita alla data del AAAMMGG
