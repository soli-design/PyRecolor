import os
from halo import Halo

spinner = Halo(text='Dolgozok...', spinner='dots')

_FROM = "svg"
_TO = "txt"
_TARGETCOLOR = "currentColor"

# Ebben az array-ben gyűjtjük a hibák üzeneteit
hibajegyzek = []

def gatherErrors(erMsg, exc):
    """hibaüznetek lekezelése. Kírás és gyűjtés.\n
    erMsg : string -> dev által definiált hibaüzenet\n
    exc : error object -> python hibaüzenet"""
    hibajegyzek.append(erMsg)
    print(exc)

def getFileList(uri):
    """A kapott URI alapján betöltjük az összes SVG-t!\n
    uri : string -> A megadott mappa összes .SVG file-ját betölti egy listába.\n
    return : fileList"""
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

    return fileList

def fileRenamer(FileName, formatFrom, formatTo):
    """Átalakítjuk a file kiterjesztését\n
    FileName : string -> A teljes elérési útvonal\n
    formatFrom : string -> forrás file formátum\n
    formatTo : string -> kimeneti kiterjesztés\n
    return : string"""
    file = FileName.split(".") 

    file[1] = formatTo
    done = ".".join(file)
    return done

def svgRecolor(textFileName):
    """Megnyitjuk a file-t, megkeressük a HEX kódokat és átírjuk _TARGETCOLOR-ra\n
    textFileName : string -> A teljes file elérési útvonalat kell megadni."""
    
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

        
        if "<style>" in svgcontent:
            replaceTo = svgcontent.index(";",replaceFrom)
        else:
            replaceTo = svgcontent.index("\"",replaceFrom)

        startCountAt = replaceTo

        # itt megy a színcsere
        svgcontent = svgcontent[:replaceFrom] + _TARGETCOLOR + svgcontent[replaceTo:]

        try:
            fixed = fixHeader(svgcontent)
            if fixed != False:
                svgcontent = fixed
            else:
                gatherErrors(f'több osztály a file-ban: {textFileName}','')
        except Exception as error:
            gatherErrors(f'hiba a file ({textFileName}) fejlécének javítása közben', error)

    try:
        f = open(textFileName, "w")
    except Exception as error:
        gatherErrors(f'hiba a file ({textFileName}) újramegnyitása közben', error)

    # print(f'{textFileName} visszanyitva')

    f.write(svgcontent)
    # print(f'{textFileName} megírva')

    f.close()
    # print(f'{textFileName} bezárva')

def fixHeader(svgcontent):
    firstIndexOfDefsStyle = ""
    lastIndexOfDefsStyle = ""
    strokeWidth = ""
    strokeLineJoin = ""
    strokeLineCaps = ""
    stroke = ""
    fill = ""
    fillRule = ""
    numberOfClasses = ""

    ## remove ID-s to avoid bullshit HTML errors
    if "id=" in svgcontent:
        fi = svgcontent.index("id=")
        li = svgcontent.index("\"",fi+4)
        svgcontent = svgcontent[:fi] + svgcontent[li+1:]

    if "<defs><style>." in svgcontent:
        firstIndexOfDefsStyle = svgcontent.index("<defs><style>.")
        lastIndexOfDefsStyle = svgcontent.index("</style></defs>")
        
        styles = svgcontent[firstIndexOfDefsStyle:lastIndexOfDefsStyle]

        ## h több mint 1 class van benne, akkor nem csinálunk semmit.
        numberOfClasses = styles.count('{')
        if numberOfClasses > 1:
            print("Több, mint 1 osztály definiálva. Átugorjuk...")
            return False
        
        if "stroke-width:" in styles:
            strokeWidth = returnClassValue(styles,"stroke-width")
        if "stroke-linecap:" in styles:
            strokeLineCaps = returnClassValue(styles,"stroke-linecap")
        if "stroke-linejoin:" in styles:
            strokeLineJoin = returnClassValue(styles,"stroke-linejoin")
        if "stroke:" in styles:
            stroke = returnClassValue(styles,"stroke")
        if "fill:" in styles:
            fill = returnClassValue(styles, "fill")
        if "fill-rule:" in styles:
            fillRule = returnClassValue(styles, "fill-rule")

        ## clear styles
        source = svgcontent[:firstIndexOfDefsStyle]
        source += svgcontent[lastIndexOfDefsStyle+len("</style></defs>"):]

        ## Add to header
        headerAddition = f" stroke=\"{stroke}\" stroke-width=\"{strokeWidth}\" stroke-linecap=\"{strokeLineCaps}\" stroke-linejoin=\"{strokeLineJoin}\" fill=\"{fill}\" fill-rule=\"{fillRule}\" "
        fixFrom = source.index(">",source.index("<svg"))
        firsthalf = source[:fixFrom]
        lasthalf = source[fixFrom:]
        done = firsthalf + headerAddition + lasthalf
        return done
    else:
        return False

def returnClassValue(source,param):
    cursor = source.index(f"{param}:")
    valueStart = source.index(":",cursor)
    cursor = valueStart
    valueEnd = source.index(";",cursor)
    value = source[valueStart+1:valueEnd]
    return value

#####################################################
    
# START #

print(f"\n\nA megadott mappából betöltjük az össes SVG file-t\nmajd kicseréljük a szinezéseit '{_TARGETCOLOR}'-ra.\n")

uri = input("Add meg a mappa elérési útját!\npl.: c://mappa/mappa/\n>>")

# az inputban esélyes, hogy záró / vagy \ nélkül kapjuk az elérési utat. Hozzáadjuk, ha nincs ott.
if uri[-1] != "/" and "/" in uri:
    uri += "/"
elif uri[-1] != "\\" and "\\" in uri:
    uri += "\\"

print(f"Add meg a cél színt, amire minden SVG-t átszínezünk.\nAlapértelmezett: {_TARGETCOLOR}")
color = input("\nAdd meg a HEX színt vagy szín nevet!\nHa HEX színt adsz meg, írd bele a #-et is!\nAmennyiben az alapértelmezett megfelel, csak nyomj entert!\n>> ")

if len(color) > 0 and color != _TARGETCOLOR:
    _TARGETCOLOR = color

process = getFileList(uri) # a mappában lévő eredeti SVG filenevek

process2 = [] # TXT filenevek

process3 = [] # visszanevezett SVG filenevek

try:
    spinner.start()
    # feldolgozáshoz mindet átnevezzük SVG-ről TXT-re
    for file in process:
        newname = fileRenamer(uri + file, _FROM, _TO)
        os.rename(uri + file, newname)
        process2.append(newname)
    spinner.stop()
    print("#2 - [ átnevezés ] sikeres")

except Exception as e:
    gatherErrors("valami baj van az [ ÁTALAKÍTÁSSAL ], szidd a programozót!", e)
    print(hibajegyzek)
    raise SystemExit

finally:
    try:
        # minden file-t feldolgozunk egyesével
        print("#3 - [ feldolgozás ] megkezdve")
        spinner.start()
        for file in process2:
            svgRecolor(file)
        spinner.stop()
        print("#3 - [ feldolgozás ] sikeres")

    except Exception as error:
        gatherErrors("valami baj van a [FELDOLGOZÁSSAL], szidd a programozót!", error)
        raise SystemExit
    
    finally:
        try:
            print("#4 - [ lezárás ] megkezdése")
            spinner.start()
            # manipuláció után visszarakjuk SVG-re mindet
            for file in process2:
                newname = fileRenamer(file, _TO, _FROM) # visszafelé átnevezzük.
                os.rename(file, newname)
            spinner.start()
            print("#5 - [ visszanevezés ] sikeresen végbement.")
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