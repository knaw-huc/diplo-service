# CHANGELOG

## 30-11-2022

Er is een applicatie die een .vtt formaat aanlevert dat enigszins verschilt van de standaard.
Verzoek:
sprekers worden niet volgens het VTT-format weergegeven (“<v [speakername]>”), maar als een aparte regel

Probleem:
- dat nieuwe formaat rendert niet goed in Able Player
Verschillen, met een eerdere .vtt versie 

- in dit formaat lijkt voor de timestamp altijd een volgnummer te staan, maar dat behoort ook tot de standaard (cue identifier), dat is geen probleem
- een spreker staat altijd vlak na een TimeStamp met aan het eind van de regel een dubbele punt.


Verzoek:
sprekers worden niet volgens het VTT-format weergegeven (“<v [speakername]>”), maar als een aparte regel

Werkwijze:
 
    python3 vttconvert.py filenaam.vtt
 
levert 

    conv_filenaam.vtt 
 


## 28-11-2022

- added from - too subtree

## 25-11-2022

- adapted detail webservice with 'stationering'
- added fileexist test detail


## 24-11-2019

- browse endpoint investigation
- troubleshooting titles
- script for renaming cmdi files
- reindexing ES