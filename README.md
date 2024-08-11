# Fossil-Fighters-Randomizer
This is a digsite, starter, and (not now but hopefully in the future) teams randomizer for FF1.

You MUST put the ROM in the same folder as the exe, or it won't work.

Features:
- This mod uses event-editing shenanigans to make it so you cannot go to the Trial Dig Site,
  and you can go to Greenhorn right away. As a result of this, however, if you try to back out
  of the digsite selection menu during Chapter 1, the game will freeze
- You can only dig up the main 100
- Vivos are matched 1-to-1, so nothing is impossible to get
- Your random starter cannot be Spinax or water-type, nor someone from Post-Game Vivos
- The Custom Starter box must contain a single vivo Number, from 1 to 114, or it will do
  nothing. It also ignores the usual restrictions on DP vivos, Tryma, and Post-Game Vivos,
  so it is possible to make 100% completion impossible
- If the custom starter is over 100, it will make appear to revive Chelon. This is purely
  cosmetic, though
- The Starter in GP button force-swaps Spinax fossils and your starter's. If the starter is
  custom and has a number over 100, it will force-swap Spinax and Chelon instead
- The three vivosaurs listed in the box Post-Game Vivos, naturally, only appear post-game.
  These are Lambeo, Guan, Compso, and T-Rex. All you need to do to change this is edit the
  text input, making sure to use the vivosaurs' Numbers, and separating each by a comma and
  any number of spaces. Also, all entries after the 17th will be ignored
- To make the Holt fight beatable, you can always find V-Raptor in the Keymonite room in the
  Digadigamid. IMPORTANT: For technical reasons, these fossils will ONLY appear if you have
  neither fossil chip
- The only text which is altered is the stuff saying which DP/Tryma vivos you get, since that
  is obviously required to know. Unfortunately, however, Joe's confirmation lines could not
  be altered (it crashed it for some odd reason), so you'll just have to remember what
  vivosaur it was
- Changing enemies' levels does not change how many moves they have. The code for this, like
  the ability to randomize teams, is here but dummied out, due to problems with the very
  hardcoded AI files

If you would like to see the table of new spawns, see the "ff1_digsiteOutput.txt" the
randomizer generates.

Also, you download this by pressing the green "Code" button and choosing "Download ZIP," and
you run it by dragging and dropping an FF1 ROM onto randomize.exe.

Finally, this normally only works on Windows. For Mac and Linux, I can only point you to
WINE: https://www.winehq.org

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl

