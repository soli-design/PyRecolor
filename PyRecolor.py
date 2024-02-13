import os
_FROM = "svg"
_TO = "txt"
_TARGETCOLOR = "currentColor"

hibajegyzek = []

def gatherErrors(erMsg, exc):
    hibajegyzek.append(erMsg)
    print(exc)

def getFileList(uri):
    """A kapott URI alapján betöltjük az összes SVG-t!\nuri : string -> A megadott mappa összes .SVG file-ját betölti egy listába.\nreturn : fileList"""
    fileList = list()
    try:
        oslist = os.listdir(uri)
        if len(oslist) == 0:
            gatherErrors("Nem volt beolvasott file.", 0)
            SystemExit
        
        print("#1 - [ betölés sikeres ]")

    except RuntimeError as error:
        gatherErrors("valami baj van a [ BETÖLTÉSSEL ] futás közben, szidd a programozót!", error)
        raise SystemExit
    
    except Exception as error:
        gatherErrors("valami szar volt a [ betöltésnél ]...", error)
        raise SystemExit

    for name in oslist:
        if ".svg" in name:
            fileList.append(name)
            # print(">> " + name + " hozzáadva a listához")

    return fileList

def fileRenamer(FileName, formatFrom, formatTo):
    """Átalakítjuk a file kiterjesztését\nFileName : string -> A teljes elérési útvonal\nformaFrom : string -> forrás file formátum\nformatTo : strong -> kimeneti kiterjesztés"""
    file = FileName.split(".") 
    print(f"{formatFrom} -> {formatTo} -- {file[0]}")
    file[1] = formatTo
    done = ".".join(file)
    return done

def svgRecolor(textFileName):
    f"""Megnyitjuk a file-t, megkeressük a HEX kódokat és átírjuk '{_TARGETCOLOR}'-ra\ntextFileName : string -> A teljes file elérési útvonalat kell megadni."""
    try:
        f = open(textFileName, "rt")
        svgcontent = f.read()
    except Exception as error:
        gatherErrors(f'nem tudom megnyitni olvasásra a {textFileName} file-t.', error)
        raise SystemExit
    f.close()

    # itt megy a szín keresése
    startCountAt = 0
    while startCountAt <= len(svgcontent):
        try:
            replaceFrom = svgcontent.index("#", startCountAt)
        except:
            break
        replaceTo = replaceFrom + 7 # mert csak HEX-et nézünk, HEXA-t nem!
        startCountAt = replaceFrom
        # print(svgcontent[replaceFrom:replaceTo])
        # itt megy a színcsere
        svgcontent = svgcontent[:replaceFrom] + _TARGETCOLOR + svgcontent[replaceTo:]

    try:
        f = open(textFileName, "w")
    except Exception as error:
        gatherErrors(f'hiba a file ({textFileName}) újramegnyitása közben', error)

    # print(f'{textFileName} visszanyitva')

    f.write(svgcontent)
    # print(f'{textFileName} megírva')

    f.close()
    # print(f'{textFileName} bezárva')

#####################################################
    
# START #

print(f"\n\nA megadott mappából betöltjük az össes SVG file-t\nmajd kicseréljük a szinezéseit '{_TARGETCOLOR}'-ra.\n")

uri = input("Add meg a mappa elérési útját!\npl.: c://mappa/mappa/\n")

# az inputban esélyes, hogy záró / vagy \ nélkül kapjuk az elérési utat. Hozzáadjuk, ha nincs ott.
if uri[-1] != "/" and "/" in uri:
    uri += "/"
elif uri[-1] != "\\" and "\\" in uri:
    uri += "\\"


process = getFileList(uri) # a mappában lévő eredeti SVG filenevek

process2 = [] # TXT filenevek

process3 = [] # visszanevezett SVG filenevek

try:
    # feldolgozáshoz mindet átnevezzük SVG-ről TXT-re
    for file in process:
        newname = fileRenamer(uri + file, _FROM, _TO)
        os.rename(uri + file, newname)
        process2.append(newname)
    print("#2 - [ átnevezés siekres ]")

except Exception as e:
    gatherErrors("valami baj van az [ ÁTALAKÍTÁSSAL ], szidd a programozót!", e)
    print(hibajegyzek)
    raise SystemExit

finally:
    try:
        # minden file-t feldolgozunk egyesével
        for file in process2:
            print(file + " [ feldolgozása ] megkezdve")
            svgRecolor(file)
        print("#3 - [ feldolgozás sikeres ]")

    except Exception as error:
        gatherErrors("valami baj van a [FELDOLGOZÁSSAL], szidd a programozót!", error)
        raise SystemExit
    
    finally:
        try:
            print("#4 - [lezárás megkezdése]")
            # manipuláció után visszarakjuk SVG-re mindet
            for file in process2:
                newname = fileRenamer(file, _TO, _FROM) # visszafelé átnevezzük.
                os.rename(file, newname)
            print("#5 - [A file visszanevezés folyamata sikeresen végbement]")
            if len(hibajegyzek) != 0:
                print(f"Hibás műveletek száma: {len(hibajegyzek)}")
                print(hibajegyzek,sep="\n")

        except Exception as error:
            gatherErrors("valami baj van a [ LEZÁRÁSSAL ], szidd a programozót!", error)
            print(hibajegyzek,sep="\n")
            raise SystemExit


if len(hibajegyzek) != 0:
    print("hiba történt az alábbi file-ok feldolgozása során:")
    print(hibajegyzek, sep="\n", end="\nEzek manuális javítást igényelnek!")