from classes import *
import json
import csv
import numpy as np
def Tura(liczba_owiec,object_on_map,sheep_move_dist,wolf_move_dist):
    #print("tura")
    # 3.1    Wszystkie zyjące owce wykonuja ruch losowo(randomdirection1-4)(gora dol prawo lewo) sheepmovedist
    eat_flag=-1
    #sheepmove
    for x in range(liczba_owiec):
        temp=int(x)
        if (object_on_map[temp].isAlive == 1):
            x, y = giveRandomDir(sheep_move_dist)
            object_on_map[temp].objectMove(x,y)
    #wolfmove
    # 1.sprawdzanie która owca jest najbliżej
    # a=111100000000
    # for i in range(liczba_owiec):
    #     if(object_on_map[i].isAlive==1):
    #         # print("owca nr",i,"pozycja x y to ",object_on_map[i].xpos,object_on_map[i].ypos)
    #         odl_wilk_od_owc=(calcDistance(object_on_map[-1], object_on_map[i]))
    #         if(odl_wilk_od_owc<a):
    #             a=odl_wilk_od_owc
    #             chasing=i
                
    sheep_distanes =  [calcDistance(sheep, object_on_map[-1]) for sheep in object_on_map[:-1]]           
    chasing = np.argmin(sheep_distanes)
    a = sheep_distanes[chasing]
    # print("2.sprawdzenie czy od niej odległość < wolf_move_dist", a)
    if(a<=wolf_move_dist):
        # print("ZJOD")
        object_on_map[-1].xpos = object_on_map[chasing].xpos
        object_on_map[-1].ypos = object_on_map[chasing].ypos
        object_on_map[chasing].isAlive=0
        eat_flag=1
    #gonienie owcy
    else:
        # print("goni")
        # print("to owca",chasing)
        #degree=calculating_degree(object_on_map[liczba_owiec].xpos,object_on_map[chasing].xpos,object_on_map[liczba_owiec].ypos,object_on_map[chasing].ypos)
        #new_x,new_y=moving_through_object(object_on_map[liczba_owiec].xpos,object_on_map[liczba_owiec].ypos,wolf_move_dist,degree)
        try:
            new_x,new_y = movenew(object_on_map[-1].xpos,object_on_map[chasing].xpos,object_on_map[-1].ypos,object_on_map[chasing].ypos,wolf_move_dist)
        except Exception:
            import pdb;pdb.set_trace()
        #print(new_x)
        object_on_map[liczba_owiec].xpos = new_x
        #print(object_on_map[liczba_owiec].xpos)
        object_on_map[liczba_owiec].ypos = new_y
        eat_flag = 0
    return eat_flag,chasing


# jeśli wilk goni którąś owcę - informację o tym fakcie wraz z określeniem, która to owca (jej numer porządkowy);
# jeżeli któraś z owiec została pożarta - informację o tym fakcie wraz z określeniem, która to była owca (jej numer porządkowy).
def giveInfo(tura_number,object_on_map,chasing,eat_flag,liczba_owiec):

    ilosc_zyjacych_owiec =0
    #Numer tury
    print("Jest to tura: ",tura_number)
    # liczbę żywych owiec;
    print("Ilosc zyjacych:" ,calcAlive(object_on_map))
    # pozycję wilka (z dokładnością do trzeciego miejsca po przecinku każdej współrzędnej);
    print("Pozycje wilka",round(object_on_map[liczba_owiec].xpos,3),round(object_on_map[liczba_owiec].ypos,3))
    if(eat_flag==0):
        print("Goni owce ",chasing)
    if(eat_flag==1):
        print("POzarta ",chasing)
        
        
        
def json_write(object_on_map, liczba_owiec, tura_number):
    with open('pos.json', 'a+') as plik:
        plik.seek(0)
        plik.write("\n" + 'Tura nr: ' + json.dumps(tura_number))
        plik.write("\n" + 'Pozycja wilka: ' + json.dumps(object_on_map[liczba_owiec].xpos) + "\t" + json.dumps(object_on_map[liczba_owiec].ypos) + "\t")
        for i in range(liczba_owiec):
            if (object_on_map[i].isAlive==1):
                plik.write(
                    "\n" + 'Owca nr: ' + json.dumps(i + 1) + "\t" + json.dumps(object_on_map[i].xpos) + "\t" + json.dumps(object_on_map[i].ypos) + "\t")
            else:
                plik.write("\n" + 'Owca nr: ' + json.dumps(i + 1) + "\t" + "Zostala zjedzona")
        plik.write("\n")
    


def csv_write(liczba_owiec, tura_number,object_on_map):
    with open('alive.csv', 'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([tura_number, calcAlive(object_on_map)])



def GameStart():
    object_on_map = []
    liczba_tur = 5000
    liczba_owiec = 15
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    chasing=0
    eaten=0
    #1. Spawning sheeps on the map with random locations
    spawnObjects(object_on_map, liczba_owiec, init_pos_limit)
    #2. spawning wolf on the map
    spawnWolf(object_on_map, liczba_owiec)
    #start tury
    for i in range(liczba_tur):
        if(calcAlive(object_on_map)==0):
            print("przerywamy by nadac specjalny komunikat")
            return 1
        giveInfo(i + 1, object_on_map, chasing, eaten, liczba_owiec)
        eaten,chasing=Tura(liczba_owiec,object_on_map,sheep_move_dist,wolf_move_dist)
        print("--------------------------------------------------")
        json_write(object_on_map,liczba_owiec,i+1)
        csv_write(liczba_owiec,i+1,object_on_map)

# Korzystając z pakietu json z biblioteki standardowej, zaimplementować zapisywanie pozycji każdego zwierzęcia podczas każdej tury do pliku pos.json. Zawartość pliku ma stanowić lista, której elementami będą słowniki, gdzie każdy słownik odpowiadać będzie pojedynczej turze symulacji i zawierać będzie następujące elementy:
# 'round_no' - numer tury (liczba całkowita);
# 'wolf_pos' - pozycja wilka (para liczb zmiennoprzecinkowych);
# 'sheep_pos' - pozycje wszystkich owiec (lista zawierająca pary liczb zmiennoprzecinkowych w przypadku żywych owiec albo wartość None/null w przypadku owiec, które zostały pożarte).
# Byłoby przy tym pożądane, aby zawartość pliku miała postać sformatowaną, to znaczy była zapisana w kolejnych liniach o odpowiednich wcięciach. Jeśli plik pos.json już istnieje, powinien zostać nadpisany.
# Korzystając z pakietu csv z biblioteki standardowej, zaimplementować zapisywanie liczby żywych owiec podczas każdej tury do pliku alive.csv. Plik ten ma się składać z dwóch kolumn przechowujących następujące wartości:
# numer tury (liczba całkowita);
# liczba żywych owiec (liczba całkowita).
# Każdej turze ma w tym pliku odpowiadać jeden wiersz (rekord). Jeśli plik alive.csv już istnieje, powinien zostać nadpisany.