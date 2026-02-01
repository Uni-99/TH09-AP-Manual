# Archipelago Manual for Touhou 9 ~ Phantasmagoria of Flower View
This is a [Manual Archipelago](https://discord.gg/T5bcsVHByx) implementation for the game _Touhou Kaeizuka ~ Phantasmagoria of Flower View_.

Setup guide can be viewed [here](manual_touhoupofv_uni/docs/setup_en.md).
## How does this work as a manual randomizer?
There are 2 modes to play.
- Story Mode, which is played in story mode
- Match Mode, which is played in match mode against CPU opponents

## Story Mode
### Locations:
- Stage Clears
  - Each stage clear for each character is a check.
  - Stage 1 ~ 8 sends a random item, while Stage 9 gives you an ending item.
### Items:
- Lives/Extends
  - Each of your characters have their own set of life items.  
    If you die more times than you have life items for the character you played in that run, you'll have to exit out of that run.
  - If you run out of in-game lives before life items, a continue may be used.
- Characters
  - Characters are locked behind items.  
    If you don't have a character unlock item for a certain character, then you're not allowed to play that character.
  - You start off with 1 random character to play.
- Endings
  - Obtain enough of them to goal.

<sup>- Fumos (There was a single leftover location for a filler item. They do nothing).</sup>

### Other Notes:
Difficulty mode is up to the player (Not including Extra Mode).

## Match Mode
This is structured similarly to story mode, kind of as a way to play story mode stages individually.
### Locations:
- Defeating Opponents
  - Each of your playable characters have 9 opponents to fight.
  - Opponents are defeated by surviving a specified amount of time against them in 1 round.
  - Early game opponents have short survival requirement but it ramps up as you go through them in order.
  - Location names will tell you which of your characters fight who, and how long you need to survive them.
    - Example: "__[Reimu] VS Youmu - 2 Minutes__" means you need to survive 2 minutes against Youmu as Reimu.
  - The first 8 opponents sends a random item, while the final opponent gives you an ending item.
  
### Items:
Items are basically the same as story mode, except lives are replaced with "Reduced Timer" items.
- Reduced Timer
  - Each of your characters have their own set of reduced timer items.  
    It reduces the amount of time required to survive opponents by 1 minute for their respective character.
    - Example: If you have two "__-1 Minute - Marisa__" items,  
      then "__[Marisa] VS Sakuya - 5 Minutes__" means you'll have to survive Sakuya as Marisa for <ins>3 Minutes</ins>.
  - If a timer goes below 1 Minute, the player can decide what that means for themselves, whether it's bottom capped at 1 minute or so.
- Characters
  - Characters are locked behind items.  
    If you don't have a character unlock item for a certain character, then you're not allowed to play that character.
  - You start off with 1 random character to play.
- Endings
  - Obtain enough of them to goal.

### Other Notes:
Lunatic is the intended difficulty for this mode, as it makes opponents never take intentional hits.  
If your opponent dies before you reach your survival time, it counts as defeating the opponent.  
Alternatively, [thprac](https://github.com/touhouworldcup/thprac) can be used to make opponents invincible for better consistency on difficulty.
