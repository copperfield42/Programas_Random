"""
Modulo dedicado a los juegos descritos en el canal de youtube Mathologer
www.youtube.com/channel/UC1_uAIS3r8Vu6JjXWvastJg

Juego NIM como se explica en el video de youtube:
www.youtube.com/watch?v=niMjxNtiuu8

       H
      HHH
     HHHHH
    HHHHHHH

    Hay 2 versiones del juego, que varian solo en la condición de victoria:
    las reglas son:
    0)es un juego de 2 personas (e inicia el jugador 1)
    1)Se eligen la cantidad de filas y la cantidad de cartas por fila
      (por defecto 4 y 1,3,5,7 respectivamente)
    2)cada jugador puede tomar 1 o más cartas de una fila por turno
    Versión 1
        3)pierde el jugador que toma la última carta
    Versión 2:
        3)gana el jugador que toma la última carta

Juego PickUp:
https://www.youtube.com/watch?v=W8_qAjR3AGE

    FFFFFFFFFFFFFFFFFFFFF

    Reglas:
    0)Es un juego de 2 personas (e inicia el jugador 1)
    1)Se elijen la cantidad de banderas y la maxima cantidad de que se puede tomar
      de las mismas
    2)Cada jugador, en su turno, puede tomar x banderas tal que 1<x<=maxima cantidad tomable
    3)Gana el jugador que tome la última bandera





"""
from collections import Counter,abc
from numbers import Integral
try:
    from my_object import MyObject
except:
    class MyObject(object):
        def __representar__(self,*v,**k):
            return super().__repr__()

class NIM(MyObject):
    """Juego de cartas NIM.
       Para jugar solo basta con hacer
       >>> NIM().jugar("yo")
       abre una simple interacción de juego con la
       configuración basica del mismo contra la computadora"""

    def __init__(self,filas=4,char="H"):
        """Inicialisa este juego de NIM.
           Si filas es un número, el juego se inicializa con tantas filas como se requiere
           con primera fila teniendo 1 carta y las siguente teniendo 2 más que la anterior.
           Si filas es una lista/tupla de números, tendra tantas filas como elementos haya
           y las filas tendran tantas cartas como se indique en cada posición del mismo.
           Para imprimir el NIM se utilisa el caracter dado como representación de las
           cartas en el tablero (en caso de ser más de uno se usa el valor por defecto)"""
        if isinstance(char,str):
            self.char=char if len(char)==1 else "H"
        else:
            raise TypeError("El caracter debe ser un str")
        self.filas=[]
        if isinstance(filas,Integral) and filas>0:
            i=1
            for x in range(filas):
                self.filas.append(i)
                i+=2
        elif isinstance(filas,abc.Sequence) and len(filas)>0:
            if all(map(lambda x: isinstance(x,Integral) and x>=0,filas)):
                self.filas=list(filas)
            else:
                raise ValueError("La secuencia debe ser de números positivos")
        else:
            raise TypeError("Las filas debe ser o un número positivo o una secuencia de uno o más números no negativos")

    def __str__(self):
        n=max(self.filas)+2
        tem="{:^n}".replace("n",str(n))
        lin=[ tem.format(self.char*x) for x in self.filas ]
        return "\n".join(map(lambda p,x:str(p)+x,range(len(lin)),lin))

    def __repr__(self):
        return super().__representar__(dict(filas=self.filas,char=self.char))

    def tomar_carta(self,fila,cantidad):
        """Toma una o más cartas de una fila del tablero.
           La cantidad a tomar debe ser mayor o igual a 1, de una fila no vacia
           Si si intenta tomar más de las que hay, se toman todas en su lugar"""
        if cantidad<1:
            raise ValueError("La cantidad a tomar deebe ser >=1")
        if fila>=0:
            if self.filas[fila]:
                self.filas[fila]-=cantidad
                if self.filas[fila]<0:
                    self.filas[fila]=0
            else:
                raise ValueError("Fila vacia")
        else:
            raise IndexError("No hay filas negativas")
        
    def termino(self):
        """Dice si el juego termino"""
        return not any(self.filas)

    def balance(self):
        """Dice si el tablero está equilibrado.
           EL tablero está equilibrado si en la representación binaria
           de la cantidad de cartas por fila, hay una cantidad par
           de 1 en la misma posición para todas las posiciones"""
        contar=Counter()
        for fila in self.filas:
            if fila:
                elems=reversed(bin(fila)[2:])
                tem=filter(bool,map(lambda ele,pos: pos if ele!="0" else 0,elems,range(1,fila+1)))
                contar.update(tem)
        for pos,cue in contar.items():
            if cue%2 !=0 :
                return False
        return True

    def mayor_unbalance(self):
        """Dice cúal es la fila más larga que procude desequilibrio, si está
           desequilibrado, sino regresa -1"""
        if not self.balance() and not self.termino():
            contar=Counter()
            distri=dict()
            i=0
            for fila in self.filas:
                if fila:
                    elems=list(reversed(bin(fila)[2:]))
                    tem=list(filter(bool,map(lambda ele,pos: pos if ele!="0" else 0,elems,range(1,fila+1))))
                    contar.update(tem)
                    distri[i]=elems
                i+=1
            des_pos=set()
            for pos,cue in contar.items():
                if cue%2 !=0 :
                    des_pos.add(pos-1)
            n=max(des_pos)+1
            candidatos=dict(filter(lambda par:len(par[1])>=n,distri.items()))
            if len(candidatos)==1:
                return tuple(candidatos.keys())[0]
            res=dict()
            for fila in candidatos:
                todo=True
                for p in des_pos:
                    if candidatos[fila][p] != "1":
                        todo=False
                        break
                if todo:
                    res[fila]=len(candidatos[fila])
            return max(res.items(),key=lambda a:a[1] )[0]
        return -1

    def fila_larga(self):
        """Dice cual es la fila más larga, en caso de empate la primera más larga"""
        return self.filas.index(max(self.filas))

    def filas_largas(self):
        """Dice cuantas filas tienen más de una carta"""
        return sum( map(lambda x: 1 if x>1 else 0,self.filas) )

    def las_filas_largas(self):
        """Retorna una lista con el número de la(s) fila(s) con más de una carta"""
        r=map(lambda pos,elem: pos if elem>1 else -1,range(len(self.filas)),self.filas)
        return list(filter(lambda x:x>-1,r))  
    
    def computador(self,version=1):
        """jugador virtual, realiza una jugada
           Regresa una tupla con la fila y la cantidad de cartas tomadas"""
        ##funciones axuiliares
        def jugar_balanciado():
            f=self.fila_larga()
            self.tomar_carta(f,1)
            return f,1
        def jugar_desbalanciado():
            f=self.mayor_unbalance()
            c=0
            while not self.balance() and not self.termino():
                self.tomar_carta(f,1)
                c+=1
            return f,c
        ##### 
        if not self.termino():
            if version==2:
                if self.balance():
                    return jugar_balanciado()
                else:
                    return jugar_desbalanciado()
            elif version==1:
                if self.filas_largas()>1:
                    if self.balance():
                        return jugar_balanciado()
                    else:
                        return jugar_desbalanciado()
                elif self.filas_largas()==1:
                    f=self.las_filas_largas()[0]
                    c=self.filas[f] - sum(map(lambda x: 1 if x else 0,self.filas))%2
                    self.tomar_carta(f,c)
                    return f,c
                else:
                    return jugar_balanciado()
                    
            else:
                raise ValueError("No existe la versión "+str(version)+" de este juego") 
        else:
            print("El juego termino")

    def jugada_valida(self,fila,cantidad):
        """Dice si la jugada es válida"""
        if fila<0 or cantidad<1:
            return False
        try:
            if not self.filas[fila]:
                return False
        except:
            return False
        return True
        
    def jugar(self,jug1,jug2="computador",version=1,lang="es"):
        """Juega un juego de NIM a partir del estado actual de este objeto.
           jug1 y jug2 son los nombres de los jugadores, si alguno de
           ellos se llama "computador" o "computadora" jugara la inteligencia
           artificial de este juego.
           version: la versión de este juego que se desee jugar
           """
        dict_mensajes={
            "es":{
                "Turno":"Turno",
                "jugador":"  Jugador",
                "compu play":"Listo tome {c} cartas de la fila {f}",
                "elegir fila":"    Fila: ",
                "elegir cartas":"    Cartas: ",
                "ganador":"Gana el jugador {n}: {name}",
                "mala jugada":"-->Error: jugada imposible, elija otra vez",
                "rendirse":"fin",
                "jugada":"  Elija la fila y cantidad de cartas a tomar,\n  o escriba 'fin' para abandonar el juego:",
                "error":"-->Error: Debe introducir números",
                "fin":"Juego abandonado."
                },
            "en":{
                "Turno":"Turn",
                "jugador":"  player",
                "compu play":"Ready, I take {c} card from row {f}",
                "elegir fila":"    Select a row: ",
                "elegir cartas":"    Select a number of cards to take: ",
                "ganador":"Win the player {n}: {name}",
                "mala jugada":"-->Error: Imposible play, try again",
                "rendirse":"end",
                "jugada":"  Select a row and a number of cards to take,\n  or write 'end' to leave the game:",
                "error":"-->Error: You must introduce a number",
                "fin":"Leaving game."
                },
            }
        def acabar_juego(x,mensajes,n,name):
            if x==mensajes["rendirse"]:
                print(mensajes["fin"])
                print(mensajes["ganador"].format(n=n,name=name))
                return True
            return False
        #mensajes=None
        if lang in dict_mensajes:
            mensajes=dict_mensajes[lang]
        else:
            raise ValueError("Lenguaje desconocido: "+str(lang))
        print(self)
        i=0
        while not self.termino():
            print(mensajes["Turno"],i)
            jugador= [jug1,jug2][i%2]
            print(mensajes["jugador"]+str(i%2 + 1)+":",jugador)
            if jugador in {"computador","computadora"}:
                f,c=self.computador(version)
                print(mensajes["compu play"].format(c=c,f=f))
            else:
                f,c=-1,0
                while True:
                    print(mensajes["jugada"])
                    a=input(mensajes["elegir fila"])
                    if acabar_juego(a,mensajes,(i+1)%2+1,[jug1,jug2][(i+1)%2]):
                        return None
                    b=int(input(mensajes["elegir cartas"]))
                    if acabar_juego(b,mensajes,(i+1)%2+1,[jug1,jug2][(i+1)%2]):
                        return None
                    try:
                        f=int(a)
                        c=int(b)
                        if self.jugada_valida(f,c):
                            self.tomar_carta(f,c)
                            break
                        else:
                            print(mensajes["mala jugada"])
                    except:
                        print(mensajes["error"])
            print(self)
            i+=1
        if version==2:
            i+=1
        print(mensajes["ganador"].format(n=i%2+1,name=[jug1,jug2][i%2]))
    

    def game(self,player1,player2="computador",version=1):
        """Play a NIM game starting in the current state of this NIM.
           player1 and player2 are the names of the player, if any of 
           them if is "computador" or "computadora" the AI play instead
           version: is the version of the NIM game to play
           """
        return self.jugar(player1,player2,version,"en")

    @classmethod
    def reglas(cls,lang="es"):
        """Imprime las reglas del juego en el idioma solicitado"""
        if lang=="es":
            print(
                "Hay 2 versiones del juego, que varian solo en la condición de victoria.",
                "Las reglas son:",
                "0)Es un juego de 2 personas (e inicia el jugador 1)",
                "1)Se eligen la cantidad de filas y la cantidad de cartas por fila",
                "  (por defecto 4 y 1,3,5,7 respectivamente)",
                "2)cada jugador puede tomar 1 o más cartas de una fila por turno",
                "Versión 1",
                "    3)pierde el jugador que toma la última carta",
                "Versión 2:",
                "    3)gana el jugador que toma la última carta",
                sep="\n"
                )
        elif lang=="en":
            print(
                "There are 2 versions of the game, that only differ in the win condition.",
                "The rules are:",
                "0)Is a 2 person game (star the player 1)",
                "1)You pick the numbers of rows and the size for row",
                "  (by default is 4 and 1,3,5,7 respectively)",
                "2)Each player must take 1 o more cards form a single row each turn",
                "Version 1",
                "    3)Lose the player tha take the last card",
                "Versión 2:",
                "    3)Win the player tha take the last card",
                sep="\n"
                )
        else:
            print("No hay reglas en el lenguaje",lang)

    @classmethod
    def rules(cls):
        """Show the rules of this game"""
        cls.reglas("en")


class PickUp(MyObject):
    
    def __init__(self,flags=21,max_pickup=3):
        self.flags=flags
        self.max_pickup=max_pickup

    def __repr__(self):
        claves=dict(flags=self.flags,max_pickup=self.max_pickup)
        return super().__representar__(claves)

    def __str__(self):
        return str(self.flags)+" "+"F"*self.flags

    def take(self,num):
        """Toma una cantidad de banderas"""
        if 0<num<=self.max_pickup:
            self.flags-=num
            if self.flags<0:
                self.flags=0
        else:
            raise ValueError("Solo puedes tomar x con x tal que: 0<x<="+str(self.max_pickup))

    def termino(self):
        return not bool(self.flags)

    def computador(self):
        """Jugador virtual, realiza una jugada"""
        if not self.termino():
            bad=self.max_pickup +1
            n=self.flags
            p=0
            for x in range(1,self.max_pickup +1):
                p=x
                if (n-p)%bad==0:
                    break
            self.take(p)
            return p
        else:
            print("El juego termino")

    def jugar(self,jug1,jug2="computador"):
        print(self)
        i=0
        while not self.termino():
            print("Turno:",i)
            jugador= [jug1,jug2][i%2]
            print("  jugador"+str(i%2 + 1)+":",jugador)
            if jugador in {"computador","computadora"}:
                f=self.computador()
                print("  listo tome",f,"banderas")
            else:
                f=int(input("    ¿cuantas banderas tomaras?: "))
                self.take(f)
            print(self)
            i+=1
        i+=1
        print("Gana el jugador",i%2+1,[jug1,jug2][i%2])        
        















