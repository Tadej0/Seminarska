import sys
import time
import winsound
import os

def zvok():
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

def izpis(n):
    print()
    for x in range(0,n):
        sys.stdout.write(".")
    print()

def uvod():
    print()
    print("Skripta za 2. seminarsko nalogo")
    print()
    print('Predmet: Analiza racunalniskih besedil\nAvtor: Tadej Bogataj\n')

def datum():
    trenutno = time.localtime(time.time())
    print("Datum:  {}.{}.{}".format(trenutno[0],trenutno[1],trenutno[2]))
    print("Ura:    {}:{}".format(trenutno[3],trenutno[4]))

def lokacijaDatoteke(besedilo):
    print()
    st = 0
    lokacija = input(besedilo)
    while (st==0):
        if(os.path.isfile(lokacija)):
            st = 1
            print("Datoteka najdena...")
        else:
            print("\tDatoteka ne obstaja...\n")
            lokacija=input(besedilo)
    return lokacija

def najdiLokacijoMape(naslov):
    i = len(naslov) - 1
    while (i>=0):
        if(naslov[i] == "/"):
            break
        else:
            i = i-1
    naslov = naslov[0:(i+1)]
    return (naslov)

def ustvariNovoMapo(koren):
    st = 0
    print()
    while(st==0):
        ime=input("Ustvari mapo za rezultate: ")
        naslov=koren+ime
        if(os.path.exists(naslov)):
            print("Mapa ze obstaja!")
        else:
            print("Mapa ustvarjena...")
            os.mkdir(naslov)
            st=1
    return naslov

def koren(lokacija,dolzina_imena):
    dolzina_niza = len(lokacija) - dolzina_imena
    nov_niz = lokacija[0:dolzina_niza]
    return nov_niz


def oskubiBesedilo(besedilo, brisiNiz):
    konec=0
    for x in besedilo:
        if (x==":"):
            break
        else:
            konec += 1
    konec += 1
    novNiz=besedilo[0:konec]
    konec = 0

    for x in besedilo:
        if(x=="."):
            konec+=1
            break
        else:
            konec+=1
    dolzinaNiza=len(besedilo)
    novNiz=novNiz+besedilo[konec:dolzinaNiza]
    konec = 0

    for x in novNiz:
        if(x=="'"):
            break
        else:
            konec+=1
    novNiz=novNiz[0:konec]+"\n"
    return (novNiz)



def obdelavaNiza(niz):
    st = 0
    while (st<len(niz)):
        if(niz[st]<='z' and niz[st]>='a'):
            break
        st=st+1
    if(st!=0):st=st-1
    niz=niz[st:len(niz)]
    return niz

def izlusciPosameznaDela(niz):
    st = 0
    dolzinaNiza = len(niz)
    while st<dolzinaNiza:
        if ((niz[st]==" ") and (niz[st+1]==" ")):
            break
        st +=1
    if(st!=0):st=st-1
    niz1 = niz[0:st]
    niz2 = niz[(st+3):dolzinaNiza]
    return (niz1,niz2)

def infoObdelava(niz):
    zbirka = []
    i=0
    zac = 0
    kon = 0
    while (niz[i] != "!"):
        i+=1
    i-=1
    stevilo = niz[0:i]
    while (i<len(niz)):
        if(niz[i] == "!"):
            zac = i
        if((niz[i] == " ") and (zac != 0) and (zac!=kon)):
            kon=i
            oznaka = niz[zac:kon]
            zbirka.append(oznaka)
            zac=i
        i+=1
    return (zbirka,stevilo)

def dodajOznakoVBazo(oznake,tmp):
    if(len(oznake)==0):
        oznake.append(tmp)
    else:
        bool = 1
        for x in oznake:
            if(x.ime == tmp.ime):
                x.steviloPojavitev +=1
                x.pojavitevVclanku.append(tmp.pojavitevVclanku)
                bool = 0
                break
        if (bool == 1):
            oznake.append(tmp)
    return (oznake)

#   Mal prevec kode :D enostaven swap bi delou :)
def zamenjaj(seznam,k,l):
    tmp_ime=seznam[k].ime
    tmp_steviloPojavitev=seznam[k].steviloPojavitev
    tmp_pojavitevVclanku = seznam[k].pojavitevVclanku

    seznam[k].ime = seznam[l].ime
    seznam[k].steviloPojavitev = seznam[l].steviloPojavitev
    seznam[k].pojavitevVclanku = seznam[l].pojavitevVclanku

    seznam[l].ime = tmp_ime
    seznam[l].steviloPojavitev = tmp_steviloPojavitev
    seznam[l].pojavitevVclanku = tmp_pojavitevVclanku


def sortiranje(seznam):
    for i in range(len(seznam)):
        for k in range(len(seznam)-1, i, -1):
            if (seznam[k].steviloPojavitev < seznam[k - 1].steviloPojavitev):
                zamenjaj(seznam, k, k-1)
    return (seznam)


def statistikaOznak(seznam):
    izpis(50)
    print("Ime oznake \t Stevilo pojavitev")
    for x in seznam:
        print(x.ime,"\t\t\t", x.steviloPojavitev)


def shraniStatistiko(oznake, lokacija, ime):
    lokacija = lokacija + "/"+ ime +".txt"
    file = open(lokacija, "w+")
    file.write("Avtor: Tadej Bogataj\n\n\n")
    file.write("Statisticne informacije:\n\n")
    file.write("Oznaka \t\tStevilo pojavitev \t\tVsebovano v clanku\n")
    file.write("-------------------------------------------------------------------------------------\n")
    for x in reversed(oznake):
        vrstica = x.ime + ":\t\t" + str(x.steviloPojavitev) + "\t\t\t\t\t" +str(x.pojavitevVclanku) + "\n"
        file.write(vrstica)
    file.close()
    os.system(lokacija)


def shraniPosamezenClanek(stevilkaClanka,clanek,lokacija, info):
    if (info == 0):
        lokacija = lokacija+"/"+stevilkaClanka+".txt"
    else:
        lokacija = lokacija+"/"+stevilkaClanka+"_i.txt"
    datoteka = open (lokacija,"w+")
    datoteka.write(clanek)
    datoteka.close()


def aliNizVsebujeNiz(niz, podniz):
    if ((podniz in niz) == True):
        return 1
    else:
        return 0

def dodajTabulator(string):
    stevec = 0
    for x in string:
        if (x==':'):
            break
        else:
            stevec +=1
    novNiz = string[0:stevec] + "\t" + string[(stevec+1):len(string)]
    return (novNiz)

def pikaVejica(string):
    string = string.replace('.',',')
    return string
