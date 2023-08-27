import os
import shutil
import subprocess
import random
import sys

vivos = list(range(1, 101))
random.shuffle(vivos)
donate = [51, 80, 19, 22, 98]
for d in donate:
    vivos[vivos.index(d)] = vivos[d]
    vivos[d] = d

broken = [1, 8, 65]
shift = [3, 10, 31, 40, 47, 79, 90, 96]
for i in shift:
    if (vivos[i] in broken):
        x = vivos[i]
        y = vivos[vivos[i]]
        vivos[i] = y
        vivos[x] = x
for i in range(len(broken)):
    ind = vivos.index(broken[i])
    x = vivos[ind]
    y = vivos[shift[i]]
    vivos[ind] = y
    vivos[shift[i]] = x

# for b in (donate + broken):
    # print(vivos.index(b))
    # print(vivos.count(b))
   
water = [ 7, 5, 35, 57, 91, 100, 16, 24, 33, 87, 86, 53, 85, 97, 62, 37, 95, 88, 72, 89, 34, 36, 73 ]
starter = list(range(1, 101))
for i in (broken + water + [20]):
    starter.remove(i)
starterRes = random.choice(starter)

subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/data/episode/e0102", "output_e0102.xdelta",
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
            point = int.from_bytes(r[0x54:0x58], "little")
            realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
            loc = point + 4
            while (realP[-1] > 0):
                realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                loc = loc + 4
            realP[-1] = len(r)
            f.write(r[0:realP[0]])
            for val in realP[0:-1]:
                index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                if (index == 0):
                    f.write(r[val:realP[realP.index(val) + 1]])
                    continue
                else:
                    f.write(r[val:(val + 12)])
                    if (mapN == "0037"):
                        f.write((3).to_bytes(4, "little"))
                    else:
                        f.write(r[(val + 12):(val + 16)])
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
                            f.write(vivos[vivoNum - 1].to_bytes(4, "little"))
                        f.write(r[(val + point4 + 4):(val + point4 + 32)])
                        if (i == (numSpawns - 1)) and ((val + point4 + 32) < realP[realP.index(val) + 1]):
                            f.write(r[(val + point4 + 32):realP[realP.index(val) + 1]])
            f.close()
            subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + mapN, "-i", "0.bin", "-o",
                "NDS_UNPACK/data/map/m/" + mapN ])
shutil.rmtree("NDS_UNPACK/data/map/m/bin/")

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
                       
subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])


    