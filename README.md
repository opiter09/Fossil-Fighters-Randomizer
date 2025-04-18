# Fossil-Fighters-Randomizer
This is a digsite, starter, and (not now but hopefully in the future) teams randomizer for FF1.

You download this by pressing the green "Code" button and choosing "Download ZIP", and
you run it by dragging and dropping an FF1 ROM onto randomize.exe. Note that you MUST put
the ROM in the same folder as the exe, or it won't work.

Furthermore, this is only designed for Windows. For Mac and Linux, I can only point you to
WINE: https://www.winehq.org. When running this through WINE, please use the command
``wine randomize.exe "ROMNAME.NDS"``, not ``wine randomize.exe`` alone.

After running the randomizer, you should receive the output ROM "out.nds". If this does not
occur, try dragging your ROM onto "DRAG_HERE_TO_SEE_ERRORS.bat" instead of "randomize.exe",
and running the randomizer again. If this yields an error message that includes a line
beginning with "PermissionError", try removing the folder "NDS_UNPACK", then drag your
ROM onto "DRAG_HERE_TO_SEE_ERRORS.bat" and try again. If this still yields a "PermissionError",
try moving the randomizer folder into your Downloads folder (if it is not there already),
removing the folder "NDS_UNPACK", and dragging your ROM onto "DRAG_HERE_TO_SEE_ERRORS.bat"
again. If you receive an error message even after that (or receive a non-"PermissionError"
message after the prior attempt), please take a screenshot of it and either post it into
the #secret-lab channel of the Fossil Fighters Discord
(https://disboard.org/server/213792669569253376), or create an Issue here on GitHub.

Features:
- This mod uses event-editing shenanigans to make it so you cannot go to the Trial Dig Site,
  and you can go to Greenhorn right away. As a result of this, however, if you try to back out
  of the digsite selection menu during Chapter 1, the game will freeze
- You can only dig up the main 100
- Vivos are matched 1-to-1, so nothing is impossible to get
- "Team Level Change:" raises or lowers (you can use negatives with a "-") the levels of all
  vivosaurs in all enemy teams. If you set "TLC on Nameless?" to "No", this will not affect
  random fighters (i.e. the ones named "Fossil Fighter")
- Your random starter cannot be Spinax or water-type, nor someone from Post-Game Vivos
- The Custom Starter box must contain a single vivo Number, from 1 to 116, or it will do
  nothing. It also ignores the usual restrictions on Post-Game Vivos, so it is possible to
  make 100% completion impossible
- FF1 is much easier than FFC in terms of IDs: the only oddity is that choosing 105 or 106
  will get you the OP Frigi and Igno, while the normal ones are 115 and 116
- If the custom starter is over 100 and not a Chicken, it will appear to revive Chelon.
  This is purely cosmetic, however
- The Starter in GP button force-swaps Spinax fossils and your starter's. If the starter is
  custom and has a number over 100, it will force-swap Spinax and Chelon instead
- The seven vivosaurs listed in the box Post-Game Vivos, naturally, only appear post-game.
  These are T-Rex, Guan, Compso, V-Raptor, Zino, Lambeo, and Centro. All you need to do to
  change this is edit the text input, making sure to use the vivosaurs' Numbers, and separating
  each by a comma and any number of spaces. Also, all entries after the 17th will be ignored
- To make the Holt fight beatable, you can always find (the first two parts of) V-Raptor in the
  Keymonite room in the Digadigamid. IMPORTANT: For technical reasons, these fossils will ONLY
  appear if you have neither fossil chip
- Mono-Spawn Mode makes it so each map [1] only spawns one vivo (along with jewels, dropping
  fossils, etc.). The exception is non-PTD Greenhorn Plains (along with the Keymonite Room and
  the Trial Dig Site), so you have a good foundation and aren't completely at the mercy of RNG
- Said vivo is the first found in the file, so some related maps will have the same one, and
  others won't. Also, to be clear, with this on you will not be able to get every vivosaur
- Due to how text replacing works, you may see multiple DP vivos listed as the same one in
  the rare case where one vanilla DP vivosaur turns into another one that comes after it.
  If that happens, you can consult the file "newDPVivos.txt" to see which is which
- Because I don't speak Japanese, the text editing part is ignored when randomizing Japanese
  ROMs. Therefore, in that case you will also have to consult the file "newDPVivos.txt" (which
  also shows what Tryma turned into). I was, however, able to make the names in there be Japanese
  if your ROM is, so that's nice
- Changing enemies' levels does not change how many moves they have. The code for this, like
  the ability to randomize teams, is here but dummied out, due to problems with the very
  hardcoded AI files

Finally, if you would like to see the table of new spawns, see the file "newDigsiteSpawns.txt"
that the randomizer generates.

[1]: I mean this in the more internal sense of "a continuous area with no loading zones in
between", not a whole digsite.

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl

