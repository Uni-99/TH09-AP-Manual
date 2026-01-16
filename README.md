# Manual Archipelago implementation for Touhou 9 ~ Phantasmagoria of Flower View
This is a [Manual Archipelago](https://github.com/ManualForArchipelago/Manual) implementation for the game _Touhou Kaeizuka ~ Phantasmagoria of Flower View_.
## How does this work?
A complete save file with all characters unlocked is required.

### Items
- Playable Characters
  - You start with 1 random character to play while the rest must be unlocked through AP items
- Lives (Story Mode) / Reduced Timer (Match Mode)
- Fumos <sub>(There was a single leftover location for a filler item, they do nothing)</sub>

### Locations:
- Stage Clears (Story Mode) / Defeating Opponents (Match Mode)

### Story Mode:
- Played in story mode
- Stage Clears are AP locations
- Lives are AP items
  - If you die more times than you have life items for the character you played in that run, you'll have to restart from stage 1
  - If you run out of in-game lives before life items, a continue may be used
  - Lives you receive in-game should be ignored
- Clearing stage 9 gives an ending item. Collect them with the required number of characters to goal
- Difficulty mode is up to the player

### Match Mode:
- Played in match mode (vs CPU)
- Each of your characters get 9 opponents to fight
- Defeating opponents are AP locations
  - Opponents are defeated by surviving a specified amount of time against them in 1 round
  - Early game opponents have short survival requirement but it ramps up as you get further
  - Location names will tell you which of your characters fight who, and how long you need to survive them
    - Example: "[Reimu] VS Youmu - 2 Minutes" Survive 2 minutes against Youmu as Reimu
- Instead of lives, the progressive items are "Time Reduction" items
  - Reduces the timer for the respective character's opponents by 1 minute
- Surviving the required amount of time against opponents last in the order gives an ending item. Collect them with the required number of characters to goal
- Lunatic is the intended difficulty for this mode, as it makes opponents never take intentional hits
  - If your opponent dies before you reach your survival time, it counts as a win
  - Alternatively, [thprac](https://github.com/touhouworldcup/thprac) can be used to make opponents invincible for better consistency on difficulty
