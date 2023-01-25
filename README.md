# Sakura-Dungeon-NPC-stat-growth-mod
Mod for Sakura Dungeon to allow non Ceri / Yomi characters to have small stat growths


## Instalation

1. Navigate to the install directory of your Sakura Dungeon `game` folder (eg: if using steam it should look something like `steamapps\common\Sakura Dungeon\game`
2. Make a backup of your game's `rpy` and `tsv` files (Optional but reccomended). If your `game` folder doesn't have any `rpy` or `tsv` files like in this example pic, then you will need to run the [RPA extractor](https://iwanplays.itch.io/rpaex) and [unrpyc scripts](https://github.com/CensoredUsername/unrpyc/releases) (or similar tools).
![](https://github.com/Best-by-feb132024/Sakura-Dungeon-NPC-stat-growth-mod/blob/main/img/non%20extracted%20game%20folder.PNG)
3. Replace


## Changes

* Sylvi: gains `Capacity`
* All other recruitable characters: gain `Capacity-2`

The new `Capicity-2` ability is a weaker version of the pre-existing `Capacity` skill Yomi / Ceri have where you gain only 4 attribute points every 10 levels instead of the weird 5 or 6 capacity gives.
Stat growth is as follows:
* levels ending in 0: +1 AGI
* levels ending in 3: +1 MNT or STR (random)
* levels ending in 5: +1 VIT
* levels ending in 7: +1 DEX or RES (random)



## Compatability
If you have other mods that change the 3 files in this, you will want to manually copy and paste the changes here into your respective `actors.tsv`, `actors.rpy`, and `stats.rpy` files.
