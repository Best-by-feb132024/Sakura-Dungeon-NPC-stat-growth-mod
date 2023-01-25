# Sakura-Dungeon-NPC-stat-growth-mod
Mod for Sakura Dungeon to allow non Ceri / Yomi characters to have small stat growths. Sakura Dungeon is a terribly balanced game when it comes to non main character party members falling off a cliff after a few levels given they just do not gain stats when leveling up. This leads to party members being quickly discarded everytime a new member joins who has straight up better stats usually. This mod aims to slightly balance things by giving everyone mild stat growths.


## Instalation

1. Navigate to the install directory of your Sakura Dungeon `game` folder (eg: if using steam it should look something like `steamapps\common\Sakura Dungeon\game`. You can either download the zip file in releases, or just download the 3 files in the `game` folder.
2. Make a backup of your game's `rpy` and `tsv` files (Optional but reccomended). If your `game` folder doesn't have any `rpy` or `tsv` files like in this example pic, then you will need to run the [RPA extractor](https://iwanplays.itch.io/rpaex) and [unrpyc scripts](https://github.com/CensoredUsername/unrpyc/releases) (or similar tools).
![](https://github.com/Best-by-feb132024/Sakura-Dungeon-NPC-stat-growth-mod/blob/main/img/non%20extracted%20game%20folder.PNG)
3. Replace the `actors.tsv` file in the `game` folder, then navigate to `system` and replace the `actor.rpy` and `stats.rpy` files. (If you see `actors.rpyc` or `stats.rpyc` you can delete them)
4. Start a new game. Because you are adding the abilities via `actors.tsv` it won't retroactively apply to any current saves.

If succesful you should see that all non Ceri/Yomi characters now have either `Capacity` or `Capacity-2` in their abilities.

Example (ignore the debug XP ability):

![example](https://github.com/Best-by-feb132024/Sakura-Dungeon-NPC-stat-growth-mod/blob/main/img/capacity-2%20before.PNG)

## Changes

* Sylvi, Maeve, and Captain Bonny: gains `Capacity`
* All other recruitable characters: gain `Capacity-2`

The new `Capicity-2` ability is a weaker version of the pre-existing `Capacity` skill Yomi / Ceri have where you gain only 4 attribute points every 10 levels instead of the weird 5 or 6 capacity gives.

Stat growth is as follows:
* levels ending in 0: +1 AGI
* levels ending in 3: +1 MNT or STR (random)
* levels ending in 5: +1 VIT
* levels ending in 7: +1 DEX or RES (random)

*Notes*: There's also a `XP-Debug` ability I was using to test this that basically jacks up XP gains to where you gain a level every battle, I left in if you want to have a go at it (You will need to edit `actors.tsv` to assign it to any characters). Lastly in `actors.rpy` there's a leftover `raise_resists(self, point)` method you can toy with calling in dialogue events, but is uneeded and unused by this mod itself.

## Compatability
If you have other mods that change the 3 files in this, you will want to manually copy and paste the changes here into your respective `actors.tsv`, `actors.rpy`, and `stats.rpy` files. Tbh I think the only mods for this game are a birthday suit nude costume patch, and a mod that makes clothes rip more easily, but they do modify `actors.rpy` I think.

## Credits

Modify and use this code however you want without credit. It's a mod for a horribly balanced 6 year old ecchi dungeon crawler that no one plays.If you're interested in modding I have a really incomplete guide document I will upload sometime.
