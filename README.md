# Fossil-Fighters-Randomizer
This is a digsite, starter, and (not now but hopefully in the future) teams randomizer for FF1.

Features:
- This mod uses event-editing shenanigans to make it so you cannot go to the Trial Dig Site,
  and you can go to Greenhorn right away. As a result of this, however, if you try to back out
  of the digsite selection menu during Chapter 1, the game will freeze
- You can only dig up the main 100
- Vivos are matched 1-to-1, so nothing is impossible to get
- Your random starter cannot be Spinax or water-type, nor someone from Post-Game Vivos
- The Starter in GP button force-swaps Spinax fossils and your starter's
- The Custom Starter box must contain a single vivo Number, from 1 to 100, or it will do
  nothing. It also ignores the usual restrictions on DP vivos, Tryma, and Post-Game Vivos,
  so it is possible to make 100% completion impossible
- The three vivosaurs listed in the box Post-Game Vivos, naturally, only appear post-game.
  These are Lambeo, Guan, and T-Rex. All you need to do to change this is edit the text input,
  making sure to use the vivosaurs' Numbers, and separating each by a comma and any number of
  spaces. Also, all entries after the 17th will be ignored
- You will never be able to dig up Tryma or the DP vivosaurs. This is because I cannot find
  where it says what they are, and I want to ensure all 100 vivosaurs can always be revived
- To make the Holt fight beatable, you can always find V-Raptor in the Keymonite room in the
  Digadigamid. IMPORTANT: For technical reasons, these fossils will ONLY appear if you have
  neither fossil chip
- No text is altered. The thing saying you got a "Spinax dino medal" at the beginning should
  be the only oddity, but who knows
- Changing enemies' levels does not change how many moves they have. The code for this, like
  the ability to randomize teams, is here but dummied out, due to problems with the very
  hardcoded AI files
- Captain Travers' team is unaffected (because raising his level would be unfair), as are the
  underground fighters of Bottomsum Bay and the Pirate Ship (because they are known to crashes,
  presumably due to the data being in a different spot)


Also, you download this by pressing the green "Code" button and choosing "Download ZIP," and
you run it by dragging and dropping an FF1 ROM onto randomize.exe. You MUST put the ROM in
the same folder as the exe, or it won't work.

Finally, this normally only works on Windows. For Mac and Linux, I can only point you to
WINE: https://www.winehq.org

# Source Codes
- NitroPaint:  https://github.com/Garhoogin/NitroPaint/releases
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl

