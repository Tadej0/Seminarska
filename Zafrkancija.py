import urllib.request
import xml
import re
import sys

def obdelavaDatoteke(datoteka):
    rezultat = open("rezultati.txt", "a+")
    for vrsta in datoteka:
        if not vrsta.isspace():
            niz = re.sub("<.*?>", "", vrsta)
            print (vrsta)
            rezultat.write(niz)
    rezultat.close()

def main():
    naslov = input("Vnesi polen naslov: ")
    stran = urllib.request.urlopen(naslov)
    biti = stran.read()
    string = biti.decode("utf8")
    stran.close()

# Ne pozabi zbrisati datoteke tml.txt

    datoteka = open("tmp.txt","a+")
    datoteka.write(string)
    datoteka.close()
    datoteka = open("tmp.txt","r")
    obdelavaDatoteke(datoteka)

main()
