import os

hibajegyzek = []

def getFileList(uri):
    """A kapott URI alapján betöltjük az összes SVG-t!"""
    fileList = list()
    try:
        oslist = os.listdir(uri)
        print("#1 - [betölés sikeres]")
    except RuntimeError as error:
        print("valami baj van a [BETÖLTÉSSEL] futás közben, szidd a programozót!")
        print(error)
        raise SystemExit
    except:
        print("valami szar volt a betöltésnél....")
        raise SystemExit

    for name in oslist:
        if ".svg" in name:
            fileList.append(name)
            print(">> " + name + " hozzáadva a listához")

    return fileList

def fileRenamer(FileName, formatFrom, formatTo):
    """Átalakítjuk a file kiterjesztését"""
    file = FileName.split(".") 
    print(f"{formatFrom} -> {formatTo} -- {file[0]}")
    file[1] = formatTo
    done = ".".join(file)
    return done

def svgRecolor(textFileName):
    """Megnyitjuk a file-t, megkeressük a HEX kódokat és átírjuk "currentColor"-ra"""
    try:
        f = open(textFileName, "rt")
        svgcontent = f.read()
    except:
        print(f'nem tudom megnyitni olvasásra a {textFileName} file-t')
        raise SystemExit
    f.close()

    # itt megy a szín keresése
    startCountAt = 0
    counter = 0
    while True:
        replaceFrom = svgcontent.index("#", startCountAt)
        replaceTo = replaceFrom+7
        startCountAt = replaceFrom
        print(svgcontent[replaceFrom:replaceTo])
        # itt megy a színcsere
        svgcontent = svgcontent[:replaceFrom] + "currentColor" + svgcontent[replaceTo:]
        counter + 1
        print(counter)
        if replaceFrom == -1:
            print('eof')
            break

    try:
        f = open(textFileName, "w")
    except:
        print('hiba a file újramegnyitása közben')
    print('file visszanyitva')
    f.write(svgcontent)
    print('file megírva')
    f.close()
    print('file bezárva')

#####################################################



print("A megadott mappából betöltjük az össes SVG file-t\nmajd kicseréljük a szinezéseit [currentColor]-ra.\n")

uri = input("Add meg a mappa elérési útját!\npl.: c://mappa/mappa/\n")
# az inputban esélyes, hogy záró / vagy \ nélkül kapjuk az elérési utat. Hozzáadjuk, ha nincs ott.
if uri[-1] != "/" and "/" in uri:
    uri += "/"
elif uri[-1] != "\\" and "\\" in uri:
    uri += "\\"


process = getFileList(uri) # a mappában lévő eredeti SVG filenevek
print(process)
print('Add meg a forrás kiterjeszését')
formatFrom = input('forrás kiterjesztése (alapérelmezett SVG -> ENTER): ')
print('Add meg a cél kiterjeszését')
formatTo = input('cél kiterjesztése (alapéretelmezett: SVG -> ENTER): ')
process2 = [] # TXT filenevek
process3 = [] # visszanevezett SVG filenevek
try:
    # feldolgozáshoz mindet átnevezzük SVG-ről TXT-re
    for file in process:
        newname = fileRenamer(uri + file, formatFrom="svg", "txt")
        os.rename(uri + file, newname)
        process2.append(newname)
    print("#2 - [átnevezés siekres]")

except Exception as e:
    print("valami baj van az [ÁTALAKÍTÁSSAL], szidd a programozót!")
    print(e)
    raise SystemExit
finally:
    try:
        # minden file-t feldolgozunk egyesével
        for file in process2:
            print(file + " feldolgozása megkezdve")
            svgRecolor(uri + file)
        print("#3 - [feldolgozás sikeres]")
    except:
        print("valami baj van a [FELDOLGOZÁSSAL], szidd a programozót!")
        raise SystemExit
    finally:
        try:
            print("#4 - [lezárás megkezdése]")
            # manipuláció után visszarakjuk SVG-re mindet
            for file in process2:
                newname = fileRenamer(file, "txt", formatTo="svg")
                os.rename(file, newname)
            print("#5 - [A folyamat sikeresen végbement]")
        except:
            print("valami baj van a LEZÁRÁSSAL, szidd a programozót!")
            raise SystemExit


if len(hibajegyzek) != 0:
    print("hiba történt az alábbi file-ok feldolgozása során:")
    print(hibajegyzek, sep="\n", end="\nEzek manuális javítást igényelnek!")