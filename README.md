# Manual Archipelago implementation for Touhou 9 ~ Phantasmagoria of Flower View
This is a [Manual Archipelago](https://discord.gg/T5bcsVHByx) implementation for the game _Touhou Kaeizuka ~ Phantasmagoria of Flower View_.

Setup guide can be viewed [here](manual_touhoupofv_uni/docs/setup_en.md)
## How does this work?
There are 2 modes to play: Story Mode and Match Mode

### Story Mode:
- Played in story mode
- Start with 1 random character to play
  - The rest are unlocked through AP items
- Stage Clears are AP locations
- Lives are AP items
  - If you die more times than you have life items for the character you played in that run, you'll have to exit out of that run
  - If you run out of in-game lives before life items, a continue may be used
- Clearing stage 9 gives an ending item
  - Collect them with a configurable amount of characters to goal
- Difficulty mode is up to the player

### Match Mode:
- Played in match mode (vs CPU)
- Start with 1 random character to play
  - The rest are unlocked through AP items
- Each of your characters get 9 opponents to fight
- Defeating opponents are AP locations
  - Opponents are defeated by surviving a specified amount of time against them in 1 round
  - Early game opponents have short survival requirement but it ramps up as you get further
  - Location names will tell you which of your characters fight who, and how long you need to survive them
    - Example: "__[Reimu] VS Youmu - 2 Minutes__" Survive 2 minutes against Youmu as Reimu
- Instead of lives, there are "Reduced Timer" items which reduces the timer for their respective character's opponents by 1 minute
  - Example: If you have 2 "__-1 Minute - Marisa__" items,\
"__[Marisa] VS Sakuya - 5 Minutes__" means you'll have to survive Sakuya as Marisa for <ins>3 Minutes</ins>
  - If a timer goes below 1 Minute, the player can decide what that means for themselves, whether it's bottom capped at 1 Minute or so
- Defeating your characters' last opponent gives an ending item
  - Collect them with a configurable amount of characters to goal
- Lunatic is the intended difficulty for this mode, as it makes opponents never take intentional hits
  - If your opponent dies before you reach your survival time, it counts as a win
  - Alternatively, [thprac](https://github.com/touhouworldcup/thprac) can be used to make opponents invincible for better consistency on difficulty
