import os
import shutil
import subprocess
import random
import sys
import FreeSimpleGUI as psg

def digsiteOutput():
    text = open("newDigsiteSpawns.txt", "wt")
    text.close()
    text = open("newDigsiteSpawns.txt", "at")
    vivoNames = ["NONE"] + list(open("ff1_vivoNames.txt", "rt").read().split("\n"))
    vivoNamesJ = [("NONE").encode("UTF-8", errors = "ignore")] + list(open("ff1_vivoNames_j.txt", "rb").read().split((0x0A).to_bytes(1, "little")))
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                point = int.from_bytes(r[0x54:0x58], "little")
                mapN = os.path.join(root, file).split("\\")[-2]
                mf = open("Map IDs.txt", "rt")
                lines = list(mf.read().split("\n")).copy()
                for t in lines:
                    if (t != ""):
                        nums = list(t.split(":")[0].replace(", ", ",").split(",")).copy()
                        for n in nums:
                            if (int(mapN.split(" [")[0]) == int(n)):
                                mapN = mapN + " [" + t.split(": ")[1] + "]"
                realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
                loc = point + 4
                while (realP[-1] > 0):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP = realP[0:-1]
                check = 0
                for val in realP:
                    index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (check == 0):
                            check = 1
                            text.write(mapN + ":\n")
                    text.write("\tZone " + str(index).zfill(2) + ":\n")
                    chip = int.from_bytes(r[(val + 8):(val + 12)], "little")
                    if (chip in [0x6F, 0x70, 0x71]):
                        chip = str(chip - 0x6F)
                    else:
                        chip = "?"
                    maxFos = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    text.write("\t\tFossil Chips Needed: " + chip + "\n")
                    text.write("\t\tMax Spawns: " + str(maxFos) + "\n")
                    numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                    point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                    for i in range(numSpawns):
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                        chance = int.from_bytes(r[(val + point4 + 4):(val + point4 + 8)], "little")
                        parts = [
                            int.from_bytes(r[(val + point4 + 16):(val + point4 + 20)], "little"),
                            int.from_bytes(r[(val + point4 + 20):(val + point4 + 24)], "little"),
                            int.from_bytes(r[(val + point4 + 24):(val + point4 + 28)], "little"),
                            int.from_bytes(r[(val + point4 + 28):(val + point4 + 32)], "little")
                        ]
                        s = "\t\t" + "[0x" + hex(val + point4).upper()[2:] + "] " + vivoNames[vivoNum] + ": " + str(chance) + "% "
                        s = s + "(Part 1: " + str(parts[0]) + "%, Part 2: " + str(parts[1]) + "%, Part 3: " + str(parts[2])
                        s = s + "%, Part 4: " + str(parts[3]) + "%)\n"
                        text.write(s)
                if (check == 1):
                    text.write("\n")
    text.close()
    if (japan == True):
        f = open("newDigsiteSpawns.txt", "rb")
        r = f.read()
        f.close()
        for i in range(116):
            r = r.replace(("] " + vivoNames[i] + ": ").encode("UTF-8", errors = "ignore"),
                ("] ").encode("UTF-8", errors = "ignore") + vivoNamesJ[i] + (": ").encode("UTF-8", errors = "ignore"))
        f = open("newDigsiteSpawns.txt", "wb")
        f.write(r)
        f.close()

def messageReplace(fileNum, oldList, newList):
    if (japan == True):
        return

    byteList = []
    subprocess.run([ "fftool.exe", "./NDS_UNPACK/data/msg/msg_" + fileNum ])
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "rb")
    r = f.read()
    f.close()
    numStrings = int.from_bytes(r[4:8], "little")
    for i in range(12, 12 + (numStrings * 4), 4):
        loc = int.from_bytes(r[i:(i + 4)], "little")
        nextLoc = int.from_bytes(r[(i + 4):(i + 8)], "little")
        if ((i + 4) >= (12 + (numStrings * 4))):
            nextLoc = os.stat("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin").st_size
        temp = (r[(loc + 8):nextLoc]).decode("UTF-8", errors = "ignore")
        for j in range(min(len(oldList), len(newList))):
            temp = temp.replace(oldList[j], newList[j])
        temp = temp.encode("UTF-8", errors = "ignore")
        align = 4 - (len(r[loc:(loc + 8)] + temp) % 4)
        if (align < 4):
            byteList.append(r[loc:(loc + 8)] + temp + bytes(align))
        else:
            byteList.append(r[loc:(loc + 8)] + temp)
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "wb")
    f.close()
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "ab")
    f.write(r[0:16])
    writeLoc = int.from_bytes(r[12:16], "little")
    for i in range(len(byteList) - 1):
        writeLoc = writeLoc + len(byteList[i])
        f.write(writeLoc.to_bytes(4, "little"))
    for i in range(len(byteList)):
        f.write(byteList[i])
    f.close()
    subprocess.run([ "fftool.exe", "compress", "./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/", "-c", "None", "-c", "None",
        "-i", "0.bin", "-o", "./NDS_UNPACK/data/msg/msg_" + fileNum ])
    shutil.rmtree("NDS_UNPACK/data/msg/bin/")
        
layout = [
    [ psg.Text("Randomize Fossils?", size = 17), psg.Button("Yes", key = "dig", size = 5) ],
    [ psg.Text("Randomize Starter?", size = 17), psg.Button("Yes", key = "start", size = 5) ],
    # [ psg.Text("Randomize Teams?", size = 17), psg.Button("No", key = "team", size = 5) ],
    [ psg.Text("Mono-Spawn Mode?", size = 17), psg.Button("No", key = "mono", size = 5) ],
    [ psg.Text("GP Starter Fossils?", size = 17), psg.Button("Yes", key = "green", size = 5) ],
    [ psg.Text("Custom Starter:", size = 17), psg.Input(default_text = "", key = "custom", size = 5, enable_events = True) ],
    [ psg.Text("Post-Game Vivos:", size = 17), psg.Input(default_text = "1, 8, 22, 29, 43, 65, 76", key = "broken", size = 20, enable_events = True) ],
    [ psg.Text("Team Level Change:", size = 17), psg.Input(default_text = "0", key = "level", size = 5, enable_events = True) ],
    [ psg.Text("TLC on Nameless?", size = 17), psg.Button("Yes", key = "jewel", size = 5) ],
    [ psg.Button("Run") ]
]
window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")
good = 0
res = { "dig": "Yes", "start": "Yes", "team": "No", "mono": "No", "green": "Yes", "jewel": "Yes" }
brokenR = ""
levelR = 0
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        good = 0
        break
    elif (event in res.keys()):
        x = ["No", "Yes"]
        new = x[int(not x.index(window[event].get_text()))]
        window[event].update(new)
        res[event] = new
    elif (event == "Run"):
        good = 1
        brokenR = values["broken"]
        levelR = values["level"]
        customR = values["custom"]
        try:
            levelR = int(levelR)
        except:
            levelR = 0
        break
    
if (good == 1):
    if (os.path.exists("NDS_UNPACK/y7.bin") == True):
        shutil.rmtree("./NDS_UNPACK/")
    if (os.path.exists("out.nds") == True):
        os.remove("out.nds")
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    
    f = open(sys.argv[1], "rb")
    r = f.read()
    f.close()
    if (r[0x0F] == 0x4A): # "J"
        japan = True
    else:
        japan = False
    
    if (japan == False):
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/data/episode/e0102", "output_e0102.xdelta",
            "NDS_UNPACK/data/episode/e0102x" ])
        if (os.path.exists("NDS_UNPACK/data/episode/e0102x") == True):
            os.remove("NDS_UNPACK/data/episode/e0102")
            os.rename("NDS_UNPACK/data/episode/e0102x", "NDS_UNPACK/data/episode/e0102")
    else:
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/data/episode/e0102", "output_e0102_j.xdelta",
            "NDS_UNPACK/data/episode/e0102x" ])
        if (os.path.exists("NDS_UNPACK/data/episode/e0102x") == True):
            os.remove("NDS_UNPACK/data/episode/e0102")
            os.rename("NDS_UNPACK/data/episode/e0102x", "NDS_UNPACK/data/episode/e0102")

    
    subprocess.run([ "fftool.exe", "NDS_UNPACK/data/battle" ])
    subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode" ])
    subprocess.run([ "fftool.exe", "NDS_UNPACK/data/etc/creature_defs" ])
    subprocess.run([ "fftool.exe", "NDS_UNPACK/data/map/m" ])
    
    vivoNames = ["NONE"] + list(open("ff1_vivoNames.txt", "rt").read().split("\n"))
    vivoNamesJ = [("NONE").encode("UTF-8", errors = "ignore")] + list(open("ff1_vivoNames_j.txt", "rb").read().split((0x0A).to_bytes(1, "little")))

    shift = []
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                mapN = os.path.join(root, file).split("\\")[-2]
                numTables = int.from_bytes(r[0x50:0x54], "little")
                point = int.from_bytes(r[0x54:0x58], "little")
                realP = []
                loc = point
                for i in range(numTables):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP.append(len(r))
                for val in realP[0:-1]:
                    index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                    if (index == 0):
                        continue
                    else:
                        numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                        point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                        for i in range(numSpawns):
                            point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                            vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                            if (mapN in ["0049", "0063"]):
                                shift.append(vivoNum)
    shift = list(set(shift))
    shift.sort()
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                mapN = os.path.join(root, file).split("\\")[-2]
                numTables = int.from_bytes(r[0x50:0x54], "little")
                point = int.from_bytes(r[0x54:0x58], "little")
                realP = []
                loc = point
                for i in range(numTables):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP.append(len(r))
                for val in realP[0:-1]:
                    index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                    if (index == 0):
                        continue
                    else:
                        numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                        point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                        for i in range(numSpawns):
                            point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                            vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                            if (mapN not in ["0049", "0063"]):
                                if (vivoNum in shift):
                                    shift.remove(vivoNum)
    # print(shift)
    
    water = []
    f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "rb")
    r = f.read()
    f.close()
    for i in range(116):
        oldOffset = int.from_bytes(r[(48 + (i * 4)):(52 + (i * 4))], "little")
        newOffset = int.from_bytes(r[(52 + (i * 4)):(56 + (i * 4))], "little")
        if (i == 115):
            newOffset = len(r)
        e = r[oldOffset + 0x0D]
        if ((e == 4) and (i <= 99)):
            water.append(i + 1)
    water.sort()
    # print(water)

    f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "rb")
    r = f.read()
    f.close()
    oldStarter = min(100, int.from_bytes(r[0x9D0:0x9D2], "little"))
    # print(oldStarter)

    f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "rb")
    r = f.read()
    f.close()
    donors = []
    places = [0x10160, 0x10224, 0x102E8, 0x103AC, 0x10540, 0x10604, 0x106C8, 0x1078C, 0x10920, 0x109E4, 0x10AA8, 0x10B6C,
    0x10D00, 0x10DC4, 0x10E88, 0x10F4C]
    if (japan == True):
        for i in range(len(places)):
            places[i] = places[i] + 0x110
    for i in range(0, len(places), 4):
        head = int.from_bytes(r[places[i]:(places[i] + 2)], "little")
        vivoNum = ((head - 1) // 4) + 1
        donors.append(vivoNum)
    # print(donors)
    
    f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "rb")
    r = f.read()
    f.close()
    head = int.from_bytes(r[0x0F63C:0x0F63E], "little")
    trymaNum = ((head - 1) // 4) + 1
    # print(trymaNum)
    
    vivos = list(range(1, 101))
    random.shuffle(vivos)
    vivos = [0] + vivos
    donate = [] # too much work to take this out entirely
    for d in donate:
        x = vivos.index(d)
        vivos[x] = vivos[d]
        vivos[d] = d

    broken = list(brokenR.replace(" ", "").replace("\n", "").split(","))
    broken = list(set(broken))
    try:
        broken = [ max(1, min(100, int(x))) for x in broken ]
    except:
        broken = []
    for d in donate:
        try:
            broken.remove(d)
        except:
            pass

    for b in broken:
        try:
            shift.remove(b)
        except:
            pass
    for i in shift:
        if (vivos[i] in broken):
            x = vivos[i]
            y = vivos[vivos[i]]
            vivos[i] = y
            vivos[x] = x
    for i in range(min(len(broken), len(shift))):
        ind = vivos.index(broken[i])
        x = vivos[ind]
        y = vivos[shift[i]]
        vivos[ind] = y
        vivos[shift[i]] = x

    if (res["team"] == "Yes"):
        water = []
    starter = list(range(1, 101))
    combined = list(set(donate + broken + water + [oldStarter]))
    for i in combined:
        starter.remove(i)
    starterRes = random.choice(starter)
    
    try:
        custom = max(1, min(116, int(customR)))
    except:
        custom = ""
    if (custom != ""):
        starterRes = custom
        
    if ((custom == "") and (res["start"] == "No")):
        starterRes = oldStarter

    if (res["dig"] == "No"):
        vivos = list(range(101))
    if (res["green"] == "Yes"):
        x = vivos.index(min(100, starterRes))
        y = vivos[oldStarter]
        vivos[x] = y
        vivos[oldStarter] = min(100, starterRes)
        
    if ((res["dig"] == "Yes") or (res["green"] == "Yes")):
        for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    f = open(os.path.join(root, file), "wb")
                    f.close()
                    f = open(os.path.join(root, file), "ab")
                    first = 0
                    mapN = os.path.join(root, file).split("\\")[-2]
                    numTables = int.from_bytes(r[0x50:0x54], "little")
                    point = int.from_bytes(r[0x54:0x58], "little")
                    realP = []
                    loc = point
                    for i in range(numTables):
                        realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                        loc = loc + 4
                    realP.append(len(r))
                    f.write(r[0:realP[0]])
                    for val in realP[0:-1]:
                        index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                        if (index == 0):
                            f.write(r[val:realP[realP.index(val) + 1]])
                            continue
                        else:
                            f.write(r[val:(val + 8)])
                            if (mapN == "0037"):
                                f.write((0x6F).to_bytes(4, "little"))
                                f.write((4).to_bytes(4, "little"))
                            else:
                                f.write(r[(val + 8):(val + 16)])
                            f.write(r[(val + 16):(val + 0x2C)])
                            numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                            point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                            f.write(r[(val + 0x2C):(val + point3 + (numSpawns * 4))])
                            for i in range(numSpawns):
                                point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                                vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                                if (mapN == "0037"):
                                    f.write((29).to_bytes(4, "little")) # V-Raptor
                                else:
                                    if ((res["mono"] == "Yes") and ((mapN not in ["0033", "0121"]) or (index in [7, 8]))):
                                        if (first == 0):
                                            first = vivos[vivoNum]
                                        f.write(first.to_bytes(4, "little"))
                                    else:
                                        f.write(vivos[vivoNum].to_bytes(4, "little"))
                                f.write(r[(val + point4 + 4):(val + point4 + 16)])
                                if (mapN == "0037"):
                                    f.write((50).to_bytes(4, "little"))
                                    f.write((50).to_bytes(4, "little"))
                                    f.write(bytes(8))
                                else:
                                    f.write(r[(val + point4 + 16):(val + point4 + 32)])
                                if (i == (numSpawns - 1)) and ((val + point4 + 32) < realP[realP.index(val) + 1]):
                                    f.write(r[(val + point4 + 32):realP[realP.index(val) + 1]])
                    f.close()
                    subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + mapN, "-c", "None", "-c", "None",
                        "-i", "0.bin", "-o", "NDS_UNPACK/data/map/m/" + mapN ])
        digsiteOutput()
        
    if ((res["dig"] == "Yes") or ((res["green"] == "Yes") and (starterRes in (donors + [trymaNum])))):
        f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "ab")
        parts = []
        for n in donors:
            head = ((vivos[n] - 1) * 4) + 1
            parts = parts + [head, head + 1, head + 2, head + 3]
        places = [0x10160, 0x10224, 0x102E8, 0x103AC, 0x10540, 0x10604, 0x106C8, 0x1078C, 0x10920, 0x109E4, 0x10AA8, 0x10B6C,
            0x10D00, 0x10DC4, 0x10E88, 0x10F4C, len(r)]
        if (japan == True):
            for i in range(len(places) - 1):
                places[i] = places[i] + 0x110
        f.write(r[0:places[0]])
        for i in range(16):
            f.write(parts[i].to_bytes(2, "little"))
            f.write(r[(places[i] + 2):places[i + 1]])
        f.close()

        if (japan == False):
            oldNames = [vivoNames[x] for x in (donors + [trymaNum])]
            newNames = [vivoNames[vivos[x]] for x in (donors + [trymaNum])]
            new = open("newDPVivos.txt", "wt")
            new.close()
            new = open("newDPVivos.txt", "at")
            for i in range(5):
                new.write(oldNames[i] + " --> " + newNames[i] + "\n")
            new.close()
        else:
            oldNames = [vivoNamesJ[x] for x in (donors + [trymaNum])]
            newNames = [vivoNamesJ[vivos[x]] for x in (donors + [trymaNum])]
            new = open("newDPVivos.txt", "wb")
            new.close()
            new = open("newDPVivos.txt", "ab")
            for i in range(5):
                new.write(oldNames[i] + (" --> ").encode("UTF-8", errors = "ignore") + newNames[i] + (0x0A).to_bytes(1, "little"))
            new.close()
        
        f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "ab")
        head = ((vivos[trymaNum] - 1) * 4) + 1
        parts = [head, head + 1, head + 2, head + 3]
        places = [0x0F63C, 0x0F98C, 0x0FAC8, 0x0FC04, len(r)]
        f.write(r[0:places[0]])
        for i in range(4):
            f.write(parts[i].to_bytes(2, "little"))
            f.write(r[(places[i] + 2):places[i + 1]])
        f.close()        

        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0899/",  "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e0899" ])
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e1155/",  "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e1155" ])
        
        oldDPList = []
        newDPList = []
        articleDict = {}
        for n in (donors + [trymaNum]):
            if (vivoNames[vivos[n]][0] in ["A", "E", "I", "O", "U"]):
                if (vivoNames[vivos[n]] != "U-Raptor"):
                    articleDict[str(n)] = "an"
            elif (vivoNames[vivos[n]] in ["F-Raptor", "M-Raptor", "S-Raptor"]):
                articleDict[str(n)] = "an"
            else:
                articleDict[str(n)] = "a"
        for n in donors:
            for p in ["(Head)", "(Body)", "(Arms)", "(Legs)", "head", "body", "arms", "legs"]:
                oldDPList.append(vivoNames[n] + " " + p)
                newDPList.append(vivoNames[vivos[n]] + " " + p)
                oldDPList.append("a " + vivoNames[n] + "-" + p)
                newDPList.append(articleDict[str(n)] + " " + vivoNames[vivos[n]] + "-" + p)
                oldDPList.append("an " + vivoNames[n] + "-" + p)
                newDPList.append(articleDict[str(n)] + " " + vivoNames[vivos[n]] + "-" + p)
        oldTrList = []
        newTrList = []
        for p in ["(Head)", "(Body)", "(Arms)", "(Legs)", "head", "body", "arms", "legs"]:
            oldTrList.append(vivoNames[trymaNum] + " " + p)
            newTrList.append(vivoNames[vivos[trymaNum]] + " " + p)     
            oldTrList.append("a " + vivoNames[trymaNum] + "-" + p)
            newTrList.append(articleDict[str(trymaNum)] + " " + vivoNames[vivos[trymaNum]] + "-" + p)
            oldTrList.append("an " + vivoNames[trymaNum] + "-" + p)
            newTrList.append(articleDict[str(trymaNum)] + " " + vivoNames[vivos[trymaNum]] + "-" + p)           
        messageReplace("0398", oldDPList, newDPList)
        messageReplace("1191", oldTrList, newTrList)
        
    if ((res["start"] == "Yes") or (custom != "")):
        f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "ab")
        f.write(r[0:0x8B4])
        fossil = ((starterRes - 1) * 4) + 1
        f.write(fossil.to_bytes(2, "little"))
        revi = 100
        if ((starterRes <= 100) or (starterRes in [107, 108, 109, 110, 111])): # chickens
            revi = starterRes
        f.write(r[0x8B6:0x9D0])
        f.write((revi).to_bytes(2, "little"))
        f.write(r[0x9D2:0xB18])
        f.write((revi).to_bytes(2, "little"))
        f.write(r[0xB1A:])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0047/", "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e0047" ])
        
        oldArticle = "a"
        if (vivoNames[oldStarter][0] in ["A", "E", "I", "O", "U"]):
            if (vivoNames[oldStarter] != "U-Raptor"):
                oldArticle = "an"
        elif (vivoNames[oldStarter] in ["F-Raptor", "M-Raptor", "S-Raptor"]):
            oldArticle = "an"        
        article = "a"
        if (vivoNames[starterRes][0] in ["A", "E", "I", "O", "U"]):
            if (vivoNames[starterRes] != "U-Raptor"):
                article = "an"
        elif (vivoNames[starterRes] in ["F-Raptor", "M-Raptor", "S-Raptor"]):
            article = "an"
        messageReplace("0075", [oldArticle + " $c2" + vivoNames[oldStarter]], [article + " $c2" + vivoNames[starterRes]])
    
    if ((res["team"] == "Yes") or (levelR != 0)):
        f = open("ff1_enemyNames.txt", "rt")
        eNames = list(f.read().split("\n"))
        f.close()

        for root, dirs, files in os.walk("NDS_UNPACK/data/battle/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    shift = int.from_bytes(r[8:12], "little") - 0x5C
                    teamN = eNames[int.from_bytes(r[(0x64 + shift):(0x66 + shift)], "little") - 3362]
                    if ((len(r) > 0x94) and (r[4] == 0) and ((res["jewel"] == "Yes") or (teamN != "Fossil Fighter"))):
                        f = open(os.path.join(root, file), "wb")
                        f.close()
                        f = open(os.path.join(root, file), "ab")
                        mapN = os.path.join(root, file).split("\\")[-2]
                        bpShift = int.from_bytes(r[4:8], "little")
                        numVivos = r[0x5C + shift]
                        f.write(r[0:(0x94 + shift)])
                        for i in range(numVivos):
                            vivoNum = int.from_bytes(r[(0x94 + shift + (i * 12)):(0x94 + shift + (i * 12) + 4)], "little")
                            if ((vivoNum in list(range(1, 101))) and (res["team"] == "Yes")):
                                f.write(random.randint(1, 100).to_bytes(4, "little"))
                            else:
                                f.write(r[(0x94 + shift + (i * 12)):(0x94 + shift + (i * 12) + 4)])
                            if ((levelR != 0) and (mapN != "0023")):
                                oldLevel = int.from_bytes(r[(0x94 + shift + (i * 12) + 4):(0x94 + shift + (i * 12) + 8)], "little")
                                newLevel = max(1, min(oldLevel + levelR, 12))
                                f.write(newLevel.to_bytes(4, "little"))
                            else:
                                f.write(r[(0x94 + shift + (i * 12) + 4):(0x94 + shift + (i * 12) + 8)])
                            f.write(r[(0x94 + shift + (i * 12) + 8):(0x94 + shift + (i * 12) + 12)])
                        f.write(r[(0x94 + shift + (numVivos * 12)):(0x94 + shift + (numVivos * 12) + (numVivos * 8))])
                        if False: # ((levelR != 0) and (mapN != "0023")):
                            moveMap = [ 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4 ]
                            for i in range(numVivos):
                                oldLevel = int.from_bytes(r[(0x94 + shift + (i * 12) + 4):(0x94 + shift + (i * 12) + 8)], "little")
                                newLevel = max(1, min(oldLevel + levelR, 12))
                                f.write(moveMap[newLevel].to_bytes(4, "little"))
                        else:
                            f.write(r[(0x94 + shift + (numVivos * 12) + (numVivos * 8)):(0x94 + shift + (numVivos * 12) + (numVivos * 12))])
                        f.write(r[(0x94 + shift + (numVivos * 12) + (numVivos * 12)):])
                        f.close()
                        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle/bin/" + mapN, "-c", "None", "-c",
                        "None", "-i", "0.bin", "-o", "NDS_UNPACK/data/battle/" + mapN ])

    shutil.rmtree("NDS_UNPACK/data/battle/bin")
    shutil.rmtree("NDS_UNPACK/data/episode/bin")
    shutil.rmtree("NDS_UNPACK/data/etc/bin")
    shutil.rmtree("NDS_UNPACK/data/map/m/bin")
    
    subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
    psg.popup("You can now play out.nds!", font = "-size 12") 