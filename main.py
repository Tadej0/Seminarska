from razred import oznaka
import knjiznica
import os

N = 50

def uvod():
    knjiznica.izpis(N)
    knjiznica.uvod()
    knjiznica.datum()
    knjiznica.izpis(N)

def lokacijeProgramov():
    global Txt2Bow
    global BowKMeans
    global BowTrainBinSVM
    global BowClassify
    global ucnaZbirkaBesedil
    global zbirkaBesedilPreverjanja
    Txt2Bow = "D:/Txt2Bow.exe"
    BowKMeans = "D:/BowKMeans.exe"
    BowTrainBinSVM = "D:/BowTrainBinSVM.exe"
    BowClassify = "D:/BowClassify.exe"
    ucnaZbirkaBesedil = "D:/1.txt"
    zbirkaBesedilPreverjanja = "D:/2.txt"

    #Txt2Bow = knjiznica.lokacijaDatoteke("Lokacija programa Txt2Bow: ")
    #BowKMeans = knjiznica.lokacijaDatoteke("Lokacija programa BowKMeans: ")
    #BowTrainBinSVM = knjiznica.lokacijaDatoteke("Lokacija programa BowTrainBinSVM: ")
    #BowClassify = knjiznica.lokacijaDatoteke("Lokacija programa BowClassify: ")
    #ucnaZbirkaBesedil = knjiznica.lokacijaDatoteke("Lokacija besedilne datoteke za ucenje: ")
    #zbirkaBesedilPreverjanja = knjiznica.lokacijaDatoteke("Lokacija besedilne datoteke za prevejanje: ")


def izgradnjaDatotecneStrukture():
    global korenskaMapa
    global statistikaMapa
    global razbitiClanki
    global tmpRezultati
    global kcah
    global konkretniClanki
    korenskaMapa = knjiznica.najdiLokacijoMape(ucnaZbirkaBesedil)
    korenskaMapa = knjiznica.ustvariNovoMapo(korenskaMapa)
    korenskaMapa+="/"
    statistikaMapa = korenskaMapa + "Statistika/"
    razbitiClanki = korenskaMapa + "Razbiti_Clanki/"
    tmpRezultati = korenskaMapa + "tmpFolder/"
    kcah = korenskaMapa + "kcah/"
    konkretniClanki = korenskaMapa + "konkretniClanki/"
    os.mkdir(kcah)
    os.mkdir(konkretniClanki)
    os.mkdir(statistikaMapa)
    os.mkdir(razbitiClanki)
    os.mkdir(tmpRezultati)

def prviDel():
    try:
        ukaz = Txt2Bow + " -inlndoc:"+ucnaZbirkaBesedil+ " -o:"+statistikaMapa+"prvo.bow -stopword:none -stemmer:none -ngramlen:1"
        os.system(ukaz)
        print("\n\n Pretvorba v BOW uspesna.")
    except:
        print("\nUkaz se ni uspesno izvedel!")


def obdelavaPrvegaBesedila():
    trenutniSeznamOznak = []
    oznake = []
    print("Obdelava dokumenta v postopku....\nLahko traja nekaj sekund...")
    ucnoBesedilo = open(ucnaZbirkaBesedil,"r")
    for vrsta in iter(ucnoBesedilo):
        #   Bedarija da posebej shranjujem oba dela... zna pridit kasneje prav
        info, clanek = knjiznica.izlusciPosameznaDela(vrsta)
        trenutniSeznamOznak, stevilkaClanka = knjiznica.infoObdelava(info)
        #   Prehod skozi oznake, še vedno ista vrstica
        for oz in trenutniSeznamOznak:
            tmp = oznaka(oz,stevilkaClanka)
            #   Zacnem polniti ali pa preverjam ali je ze notri nek element in inkrementiram njegovo vrednost
            oznake = knjiznica.dodajOznakoVBazo(oznake,tmp)
    ucnoBesedilo.close()
    oznake = knjiznica.sortiranje(oznake)
    knjiznica.shraniStatistiko(oznake, statistikaMapa,"Statistika_Oznak_1")
    knjiznica.izpis(N)

def drugiDel():
    vpr = 1
    print()
    while (vpr == 1):
        clust = input("Na koliko clustrov zelis razdeliti dokument: ")
        #   Ustvari datoteko za vsako število...
        try:
            tmpLokacija = statistikaMapa+clust+"_clustrov/"
            os.mkdir(tmpLokacija)
            os.chdir(tmpLokacija)
            ukaz = BowKMeans + " -i:"+statistikaMapa+"prvo.bow -clusts:"+clust
            os.system(ukaz)
        except:
            print("Na toliko clustrov se je ze razdelilo...")
        odg = int(input("Zelis ponoviti razdelitev? \n0 == Ne\n1 == Da\nIzbira:"))
        if (odg != 1):
            break
    knjiznica.izpis(N)
    print("Clustriranje koncano...")



def bowClassifyUporaba(lokacijaUcenega, kategorija, jedro):
    naslovRezultati = statistikaMapa + "Rezultati_" + kategorija + "_" + jedro + ".txt"
    rezultati = open(naslovRezultati, "a+")
    tmpNaslov = tmpRezultati + kategorija + "_" + jedro+"/"
    os.mkdir(tmpNaslov)
    prviBow = statistikaMapa+"prvo.bow"

#   Istocasno ko obdelujem z BowC berem rezultate in jih shranjujem v skupno datoteko
#   istočasno grem skozi datoteke x_i.txt, kjer pogleddam ali je kategorija znotraj niza...


    for dokument in seznamDokumentov:
        infoNaslov = kcah + dokument + "_i.txt"
        infoDatoteka = open(infoNaslov,"r")
        info = infoDatoteka.readline()
    #   Info del o posameznem clanku prebran!
        aliJe = knjiznica.aliNizVsebujeNiz(info, kategorija)
        infoDatoteka.close()
        tmpDatoteka = tmpNaslov + dokument + "/"
        os.mkdir(tmpDatoteka)
        os.chdir(tmpDatoteka)
        ukaz = BowClassify + " -ibow:" + prviBow + " -imd:" + lokacijaUcenega+" -qh:" + razbitiClanki + dokument + ".txt"
        os.system(ukaz)
        tmpInfo = "BowCfy.Txt"
        tmp = open(tmpInfo, "r")
        niz=tmp.readline()
        stringOdg = " "
        if (aliJe == 1):
            stringOdg = "1 \t Vsebuje \t"
        elif (aliJe == 0):
            stringOdg = "0 \t Ne vsebuje \t"
        string = stringOdg + dokument +":\t\t" + niz
        string = knjiznica.oskubiBesedilo(string, kategorija)
        rezultati.write(string)
        tmp.close()
    rezultati.close()
    knjiznica.zvok()



def uporabaKlasifikatorjev():
    vpr = 1
    while(vpr == 1):
        print("BowClassify...")
        kategorija = input("Kategorija: ")
        kategorija = kategorija.upper()
        jedro = input("Jedro [L... linerna   P... polinomska]: ")
        jedro = jedro.upper()
        lokacijaUcenja = statistikaMapa +kategorija+"_"+jedro+"/prvo.bowmd"
        print(lokacijaUcenja)
        if(os.path.isfile(lokacijaUcenja)):
            print("Klasifikator in vrsta jedra sta bila izvedena... BowClassify se lahko zazene")
            bowClassifyUporaba(lokacijaUcenja, kategorija, jedro)


            "TU SEM OSTAL..."



        else:
            print("Specificna klasifikacija ni bila izvedena!")

        odg =input("Zelis ponoviti uporabo BowClassify? \n0 == Ne\n1 == Da\nIzbira:")
        if (odg != "1"):
            break



def obdelavaDrugegaBesedila():
    trenutniSeznamOznak = []

#   Seznam dokumentov drzi imena vseh dokumentov, ki jih mora kasneje BowClassify obdelati...
#   Ko sm tolk butast resno :/ sam se eno dodatno txt datoteko ustvarjej za info shranjevat, pol pa po sami informaciji skač
    global seznamDokumentov
    seznamDokumentov = []
    oznake = []
    print("Obdelava dokumenta v postopku....\nLahko traja nekaj sekund...")
    ucnoBesedilo = open(zbirkaBesedilPreverjanja,"r")
    for vrsta in iter(ucnoBesedilo):
        info, clanek = knjiznica.izlusciPosameznaDela(vrsta)
        trenutniSeznamOznak, stevilkaClanka = knjiznica.infoObdelava(info)
        seznamDokumentov.append(stevilkaClanka)
        #   Prehod skozi oznake, še vedno ista vrstica
        for oz in trenutniSeznamOznak:
            tmp = oznaka(oz,stevilkaClanka)
            #   Zacnem polniti ali pa preverjam ali je ze notri nek element in inkrementiram njegovo vrednost
            oznake = knjiznica.dodajOznakoVBazo(oznake,tmp)
        # hashtag:PonosnNaIdejo :P
        knjiznica.shraniPosamezenClanek(stevilkaClanka,clanek,razbitiClanki,0)
        knjiznica.shraniPosamezenClanek(stevilkaClanka,info,kcah,1)
    ucnoBesedilo.close()
    oznake = knjiznica.sortiranje(oznake)
    knjiznica.shraniStatistiko(oznake, statistikaMapa,"Statistika_Oznak_2")

    global seznamKategorijDrugegaBesedila
    seznamKategorijDrugegaBesedila = oznake
    knjiznica.izpis(N)
    '''
    seznamKategorijDrugegaBesedila je seznam vseh objektov, ki so sestavljeni iz imena,
    pogostosti pojavitve in seznamu dokumentov v katerem se nahajajo.
    To uporabiš kasneje pri preverjanju ali nek dokument res je označen pod neko kategorijo ali ne...
    '''
    uporabaKlasifikatorjev()



def tretjiDel():
    vpr = 1
    while(vpr == 1):
        odg = input("Prikazi podatke o pogostosti klasifikatorjev prvega dokumenta? [Y/N]")
        odg = odg.upper()
        if (odg == "Y"):
            niz = statistikaMapa+"Statistika_Oznak_1.txt"
            os.system(niz)

        kategorija = input("Kategorija za klasifikacijo: ")
        kategorija = kategorija.upper()

        linPol = input("Linearna ali polinomska oblika jedra: [L... linerna   P... polinomska]")
        linPol = linPol.upper()

        __tmpImeDatoteke = kategorija + "_" + linPol + "/"
        tmpLokacija = statistikaMapa + __tmpImeDatoteke

        try:
            os.mkdir(tmpLokacija)
            os.chdir(tmpLokacija)
            if (linPol == "L"):
                ukaz = BowTrainBinSVM + " -i:"+statistikaMapa+"prvo.bow -t:linear -o:"+tmpLokacija+"prvo.bowmd -cat:"+kategorija
            else:
                ukaz = BowTrainBinSVM + " -i:"+statistikaMapa+"prvo.bow -t:polynomial -ker_p:3 -o:"+tmpLokacija+"prvo.bowmd -cat:"+kategorija
            os.system(ukaz)
        except:
            print("Ta klasifikacija je ze bila opravljena...")
        odg =input("Zelis ponoviti klasificiranje? \n0 == Ne\n1 == Da\nIzbira:")
        if (odg != "1"):
            break
    #   Zakljucek ucenja razlicnih klasifikatorjev

    #   preverjanje nad drugim besedilom:
    obdelavaDrugegaBesedila()

def bowClassifyUporabaNadClankom(lokacijaUcenja, kategorija, jedro, imeClanka, lokacijaZunanjiClanek):
    tmpNaslov = konkretniClanki + imeClanka + "_" + kategorija + "_" + jedro + "/"
    os.mkdir(tmpNaslov)
    os.chdir(tmpNaslov)
    ukaz = BowClassify + " -ibow:" + prviBow + " -imd:" + lokacijaUcenega+" -qh:" + lokacijaZunanjiClanek
    os.system(ukaz)



def zunanjiClanek():
    vpr = 1
    knjiznica.izpis(N)
    print("'Za vsako od uporabljenih štirih kategorij poiščite na internetu po eno besedilo, ki ga klasifikator za tisto kategorijo napove kot pozitiven primer.'")
    print("Pregled zunanjih clankov. Ustvarite datoteko[format .txt], ki vsebuje besedilo clanka.")
    print("Nato sledite navodilom...")
    knjiznica.izpis(N)
    while(vpr == 1):
        lokacijaZunanjiClanek = knjiznica.lokacijaDatoteke("Lokacija clanka: ")
        clanek = open(lokacijaZunanjiClanek,"r")
        imeClanka = clanek.name
        kategorija = input("Kategorija: ")
        kategorija = kategorija.upper()
        jedro = input("Jedro [L... linerna   P... polinomska]: ")
        jedro = jedro.upper()
        lokacijaUcenja = statistikaMapa +kategorija+"_"+jedro+"/prvo.bowmd"
        if(os.path.isfile(lokacijaUcenja)):
            print("Klasifikator in vrsta jedra sta bila izvedena... BowClassify se lahko zazene")
            bowClassifyUporabaNadClankom(lokacijaUcenja, kategorija, jedro, imeClanka, lokacijaZunanjiClanek)
        else:
            print("Specificna klasifikacija ni bila izvedena!")

        odg =input("Zelis ponoviti ukaz? \n0 == Ne\n1 == Da\nIzbira:")
        if (odg != "1"):
            break

def main():
    uvod()
    lokacijeProgramov()
    izgradnjaDatotecneStrukture()
    obdelavaPrvegaBesedila()
    prviDel()
    drugiDel()
    tretjiDel()
    zunanjiClanek()

if (__name__ == "__main__"):
    main()
