import os
import shutil
import subprocess
import random
import sys
import PySimpleGUI as psg

layout = [
    [ psg.Text("Randomize Fossils?", size = 17), psg.Button("Yes", key = "dig", size = 5) ],
    [ psg.Text("Randomize Starter?", size = 17), psg.Button("Yes", key = "start", size = 5) ],
    # [ psg.Text("Randomize Teams?", size = 17), psg.Button("No", key = "team", size = 5) ],
    [ psg.Text("GP Starter Fossils?", size = 17), psg.Button("Yes", key = "green", size = 5) ],
    [ psg.Text("Custom Starter:", size = 17), psg.Input(default_text = "", key = "custom", size = 5, enable_events = True) ],
    [ psg.Text("Post-Game Vivos:", size = 17), psg.Input(default_text = "1, 8, 65", key = "broken", size = 20, enable_events = True) ],
    [ psg.Text("Team Level Change:", size = 17), psg.Input(default_text = "0", key = "level", size = 5, enable_events = True) ],
    [ psg.Button("Run") ]
]
window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")
good = 0
res = { "dig": "Yes", "start": "Yes", "team": "No", "green": "Yes" }
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
    vivos = list(range(1, 101))
    random.shuffle(vivos)
    vivos = [0] + vivos
    donate = [51, 80, 19, 22, 98]
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

    shift = [1, 3, 10, 31, 40, 47, 79, 90, 96, 16, 34, 49, 57, 84, 91, 95, 97]
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

    water = [ 7, 5, 35, 57, 91, 100, 16, 24, 33, 87, 86, 53, 85, 97, 62, 37, 95, 88, 72, 89, 34, 36, 73 ]
    if (res["team"] == "Yes"):
        water = []
    starter = list(range(1, 101))
    combined = list(set(donate + broken + water + [20]))
    for i in combined:
        starter.remove(i)
    starterRes = random.choice(starter)
    
    try:
        custom = max(1, min(100, int(customR)))
    except:
        custom = ""
    if (custom != ""):
        starterRes = custom

    if (res["green"] == "Yes"):
        if (res["dig"] == "No"):
            vivos = list(range(101))
        x = vivos.index(starterRes)
        y = vivos[20]
        vivos[x] = y
        vivos[20] = starterRes

    try:
        shutil.rmtree("NDS_UNPACK")
    except:
        pass
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    
    if ((res["dig"] == "Yes") or (res["green"] == "Yes")):
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/data/episode/e0102", "output_e0102.xdelta",
            "NDS_UNPACK/data/episode/e0102x" ])
        if (os.path.exists("NDS_UNPACK/data/episode/e0102x") == False):
            subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/data/episode/e0102", "output_e0102_j.xdelta",
                "NDS_UNPACK/data/episode/e0102x" ])
        os.remove("NDS_UNPACK/data/episode/e0102")
        os.rename("NDS_UNPACK/data/episode/e0102x", "NDS_UNPACK/data/episode/e0102")       

        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/map/m" ])
        for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    f = open(os.path.join(root, file), "wb")
                    f.close()
                    f = open(os.path.join(root, file), "ab")
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
                                f.write((9).to_bytes(4, "little"))
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
                                    f.write((29).to_bytes(4, "little"))
                                else:
                                    f.write(vivos[vivoNum].to_bytes(4, "little"))
                                f.write(r[(val + point4 + 4):(val + point4 + 32)])
                                if (i == (numSpawns - 1)) and ((val + point4 + 32) < realP[realP.index(val) + 1]):
                                    f.write(r[(val + point4 + 32):realP[realP.index(val) + 1]])
                    f.close()
                    subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + mapN, "-i", "0.bin", "-o",
                        "NDS_UNPACK/data/map/m/" + mapN ])
        shutil.rmtree("NDS_UNPACK/data/map/m/bin/")
    
    if ((res["start"] == "Yes") or (custom != "")):
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode/e0047" ])
        f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0047/0.bin", "ab")
        f.write(r[0:0x8B4])
        fossil = ((starterRes - 1) * 4) + 1
        f.write(fossil.to_bytes(2, "little"))
        f.write(r[0x8B6:0x9D0])
        f.write(starterRes.to_bytes(2, "little"))
        f.write(r[0x9D2:])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0047/", "-i", "0.bin", "-o",
            "NDS_UNPACK/data/episode/e0047" ])
        shutil.rmtree("NDS_UNPACK/data/episode/bin/")
    
    if ((res["team"] == "Yes") or (levelR != 0)):
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/battle" ])
        for root, dirs, files in os.walk("NDS_UNPACK/data/battle/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    if (len(r) > 0x94):
                        f = open(os.path.join(root, file), "wb")
                        f.close()
                        f = open(os.path.join(root, file), "ab")
                        mapN = os.path.join(root, file).split("\\")[-2]
                        forbid = [ "0023", "0258", "0259", "0260", "0261", "0262", "0263", "0264", "0265", "0266", "0267", "0268",
                             "0269", "0270", "0271", "072", "0273", "0274", "0275" ]
                        numVivos = r[0x5C]
                        f.write(r[0:0x94])
                        for i in range(numVivos):
                            vivoNum = int.from_bytes(r[(0x94 + (i * 12)):(0x94 + (i * 12) + 4)], "little")
                            if ((vivoNum in list(range(1, 101))) and (res["team"] == "Yes") and (mapN not in forbid)):
                                f.write(random.randint(1, 100).to_bytes(4, "little"))
                            else:
                                f.write(r[(0x94 + (i * 12)):(0x94 + (i * 12) + 4)])
                            if ((levelR != 0) and (mapN not in forbid)):
                                oldLevel = int.from_bytes(r[(0x94 + (i * 12) + 4):(0x94 + (i * 12) + 8)], "little")
                                newLevel = max(1, min(oldLevel + levelR, 12))
                                f.write(newLevel.to_bytes(4, "little"))
                            else:
                                f.write(r[(0x94 + (i * 12) + 4):(0x94 + (i * 12) + 8)])
                            f.write(r[(0x94 + (i * 12) + 8):(0x94 + (i * 12) + 12)])
                        f.write(r[(0x94 + (numVivos * 12)):(0x94 + (numVivos * 12) + (numVivos * 8))])
                        if False: # ((levelR != 0) and (mapN not in forbid)):
                            moveMap = [ 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4 ]
                            for i in range(numVivos):
                                oldLevel = int.from_bytes(r[(0x94 + (i * 12) + 4):(0x94 + (i * 12) + 8)], "little")
                                newLevel = max(1, min(oldLevel + levelR, 12))
                                f.write(moveMap[newLevel].to_bytes(4, "little"))
                        else:
                            f.write(r[(0x94 + (numVivos * 12) + (numVivos * 8)):(0x94 + (numVivos * 12) + (numVivos * 12))])
                        f.write(r[(0x94 + (numVivos * 12) + (numVivos * 12)):])
                        f.close()
                        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle/bin/" + mapN, "-i", "0.bin", "-o",
                            "NDS_UNPACK/data/battle/" + mapN ])
        shutil.rmtree("NDS_UNPACK/data/battle/bin/")
        
    subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
    psg.popup("You can now play out.nds!", font = "-size 12")


    