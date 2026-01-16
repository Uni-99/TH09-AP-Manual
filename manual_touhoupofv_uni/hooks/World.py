# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    # Fetching yaml option values
    endings_required = get_option_value(multiworld, player, "endings_required")
    difficulty_mid = get_option_value(multiworld, player, "difficulty_mid")
    difficulty_end = get_option_value(multiworld, player, "difficulty_end")
    difficulty_ayamedi = get_option_value(multiworld, player, "difficulty_ayamedi")

    enable_reimu = get_option_value(multiworld, player, "enable_reimu")
    enable_marisa = get_option_value(multiworld, player, "enable_marisa")
    enable_sakuya = get_option_value(multiworld, player, "enable_sakuya")
    enable_youmu = get_option_value(multiworld, player, "enable_youmu")
    enable_reisen = get_option_value(multiworld, player, "enable_reisen")
    enable_cirno = get_option_value(multiworld, player, "enable_cirno")
    enable_lyrica = get_option_value(multiworld, player, "enable_lyrica")
    enable_mystia = get_option_value(multiworld, player, "enable_mystia")
    enable_tewi = get_option_value(multiworld, player, "enable_tewi")
    enable_aya = get_option_value(multiworld, player, "enable_aya")
    enable_medicine = get_option_value(multiworld, player, "enable_medicine")
    enable_yuuka = get_option_value(multiworld, player, "enable_yuuka")
    enable_komachi = get_option_value(multiworld, player, "enable_komachi")
    enable_shikieiki = get_option_value(multiworld, player, "enable_shikieiki")

    # Goal access rules
    ending = multiworld.get_location("Resolve Incident", player)
    ending.access_rule = lambda state: (state.count_group("Endings", world.player) >= endings_required)

    # Stage access rules
    midaccess = difficulty_mid

    if difficulty_mid >= difficulty_end:
        s9access = difficulty_mid + 1
    else:
        s9access = difficulty_end

    if enable_reimu == True:
        s6reimu = multiworld.get_location("Reimu - Stage 6 Clear", player)
        s7reimu = multiworld.get_location("Reimu - Stage 7 Clear", player)
        s8reimu = multiworld.get_location("Reimu - Stage 8 Clear", player)
        s9reimu = multiworld.get_location("Reimu - Stage 9 Clear", player)
        s6reimu.access_rule = lambda state: (state.count("Progressive Life - Reimu", world.player) >= midaccess - 2)
        s7reimu.access_rule = lambda state: (state.count("Progressive Life - Reimu", world.player) >= midaccess - 1)
        s8reimu.access_rule = lambda state: (state.count("Progressive Life - Reimu", world.player) >= midaccess)
        s9reimu.access_rule = lambda state: (state.count("Progressive Life - Reimu", world.player) >= s9access)
    if enable_marisa == True:
        s6marisa = multiworld.get_location("Marisa - Stage 6 Clear", player)
        s7marisa = multiworld.get_location("Marisa - Stage 7 Clear", player)
        s8marisa = multiworld.get_location("Marisa - Stage 8 Clear", player)
        s9marisa = multiworld.get_location("Marisa - Stage 9 Clear", player)
        s6marisa.access_rule = lambda state: (state.count("Progressive Life - Marisa", world.player) >= midaccess - 2)
        s7marisa.access_rule = lambda state: (state.count("Progressive Life - Marisa", world.player) >= midaccess - 1)
        s8marisa.access_rule = lambda state: (state.count("Progressive Life - Marisa", world.player) >= midaccess)
        s9marisa.access_rule = lambda state: (state.count("Progressive Life - Marisa", world.player) >= s9access)
    if enable_sakuya == True:
        s6sakuya = multiworld.get_location("Sakuya - Stage 6 Clear", player)
        s7sakuya = multiworld.get_location("Sakuya - Stage 7 Clear", player)
        s8sakuya = multiworld.get_location("Sakuya - Stage 8 Clear", player)
        s9sakuya = multiworld.get_location("Sakuya - Stage 9 Clear", player)
        s6sakuya.access_rule = lambda state: (state.count("Progressive Life - Sakuya", world.player) >= midaccess - 2)
        s7sakuya.access_rule = lambda state: (state.count("Progressive Life - Sakuya", world.player) >= midaccess - 1)
        s8sakuya.access_rule = lambda state: (state.count("Progressive Life - Sakuya", world.player) >= midaccess)
        s9sakuya.access_rule = lambda state: (state.count("Progressive Life - Sakuya", world.player) >= s9access)
    if enable_youmu == True:
        s6youmu = multiworld.get_location("Youmu - Stage 6 Clear", player)
        s7youmu = multiworld.get_location("Youmu - Stage 7 Clear", player)
        s8youmu = multiworld.get_location("Youmu - Stage 8 Clear", player)
        s9youmu = multiworld.get_location("Youmu - Stage 9 Clear", player)
        s6youmu.access_rule = lambda state: (state.count("Progressive Life - Youmu", world.player) >= midaccess - 2)
        s7youmu.access_rule = lambda state: (state.count("Progressive Life - Youmu", world.player) >= midaccess - 1)
        s8youmu.access_rule = lambda state: (state.count("Progressive Life - Youmu", world.player) >= midaccess)
        s9youmu.access_rule = lambda state: (state.count("Progressive Life - Youmu", world.player) >= s9access)
    if enable_reisen == True:
        s6reisen = multiworld.get_location("Reisen - Stage 6 Clear", player)
        s7reisen = multiworld.get_location("Reisen - Stage 7 Clear", player)
        s8reisen = multiworld.get_location("Reisen - Stage 8 Clear", player)
        s9reisen = multiworld.get_location("Reisen - Stage 9 Clear", player)
        s6reisen.access_rule = lambda state: (state.count("Progressive Life - Reisen", world.player) >= midaccess - 2)
        s7reisen.access_rule = lambda state: (state.count("Progressive Life - Reisen", world.player) >= midaccess - 1)
        s8reisen.access_rule = lambda state: (state.count("Progressive Life - Reisen", world.player) >= midaccess)
        s9reisen.access_rule = lambda state: (state.count("Progressive Life - Reisen", world.player) >= s9access)
    if enable_cirno == True:
        s6cirno = multiworld.get_location("Cirno - Stage 6 Clear", player)
        s7cirno = multiworld.get_location("Cirno - Stage 7 Clear", player)
        s8cirno = multiworld.get_location("Cirno - Stage 8 Clear", player)
        s9cirno = multiworld.get_location("Cirno - Stage 9 Clear", player)
        s6cirno.access_rule = lambda state: (state.count("Progressive Life - Cirno", world.player) >= midaccess - 2)
        s7cirno.access_rule = lambda state: (state.count("Progressive Life - Cirno", world.player) >= midaccess - 1)
        s8cirno.access_rule = lambda state: (state.count("Progressive Life - Cirno", world.player) >= midaccess)
        s9cirno.access_rule = lambda state: (state.count("Progressive Life - Cirno", world.player) >= s9access)
    if enable_lyrica == True:
        s6lyrica = multiworld.get_location("Lyrica - Stage 6 Clear", player)
        s7lyrica = multiworld.get_location("Lyrica - Stage 7 Clear", player)
        s8lyrica = multiworld.get_location("Lyrica - Stage 8 Clear", player)
        s9lyrica = multiworld.get_location("Lyrica - Stage 9 Clear", player)
        s6lyrica.access_rule = lambda state: (state.count("Progressive Life - Lyrica", world.player) >= midaccess - 2)
        s7lyrica.access_rule = lambda state: (state.count("Progressive Life - Lyrica", world.player) >= midaccess - 1)
        s8lyrica.access_rule = lambda state: (state.count("Progressive Life - Lyrica", world.player) >= midaccess)
        s9lyrica.access_rule = lambda state: (state.count("Progressive Life - Lyrica", world.player) >= s9access)
    if enable_mystia == True:
        s6mystia = multiworld.get_location("Mystia - Stage 6 Clear", player)
        s7mystia = multiworld.get_location("Mystia - Stage 7 Clear", player)
        s8mystia = multiworld.get_location("Mystia - Stage 8 Clear", player)
        s9mystia = multiworld.get_location("Mystia - Stage 9 Clear", player)
        s6mystia.access_rule = lambda state: (state.count("Progressive Life - Mystia", world.player) >= midaccess - 2)
        s7mystia.access_rule = lambda state: (state.count("Progressive Life - Mystia", world.player) >= midaccess - 1)
        s8mystia.access_rule = lambda state: (state.count("Progressive Life - Mystia", world.player) >= midaccess)
        s9mystia.access_rule = lambda state: (state.count("Progressive Life - Mystia", world.player) >= s9access)
    if enable_tewi == True:
        s6tewi = multiworld.get_location("Tewi - Stage 6 Clear", player)
        s7tewi = multiworld.get_location("Tewi - Stage 7 Clear", player)
        s8tewi = multiworld.get_location("Tewi - Stage 8 Clear", player)
        s9tewi = multiworld.get_location("Tewi - Stage 9 Clear", player)
        s6tewi.access_rule = lambda state: (state.count("Progressive Life - Tewi", world.player) >= midaccess - 2)
        s7tewi.access_rule = lambda state: (state.count("Progressive Life - Tewi", world.player) >= midaccess - 1)
        s8tewi.access_rule = lambda state: (state.count("Progressive Life - Tewi", world.player) >= midaccess)
        s9tewi.access_rule = lambda state: (state.count("Progressive Life - Tewi", world.player) >= s9access)
    if enable_yuuka == True:
        s6yuuka = multiworld.get_location("Yuuka - Stage 6 Clear", player)
        s7yuuka = multiworld.get_location("Yuuka - Stage 7 Clear", player)
        s8yuuka = multiworld.get_location("Yuuka - Stage 8 Clear", player)
        s9yuuka = multiworld.get_location("Yuuka - Stage 9 Clear", player)
        s6yuuka.access_rule = lambda state: (state.count("Progressive Life - Yuuka", world.player) >= midaccess - 2)
        s7yuuka.access_rule = lambda state: (state.count("Progressive Life - Yuuka", world.player) >= midaccess - 1)
        s8yuuka.access_rule = lambda state: (state.count("Progressive Life - Yuuka", world.player) >= midaccess)
        s9yuuka.access_rule = lambda state: (state.count("Progressive Life - Yuuka", world.player) >= s9access)
    if enable_komachi == True:
        s6komachi = multiworld.get_location("Komachi - Stage 6 Clear", player)
        s7komachi = multiworld.get_location("Komachi - Stage 7 Clear", player)
        s8komachi = multiworld.get_location("Komachi - Stage 8 Clear", player)
        s9komachi = multiworld.get_location("Komachi - Stage 9 Clear", player)
        s6komachi.access_rule = lambda state: (state.count("Progressive Life - Komachi", world.player) >= midaccess - 2)
        s7komachi.access_rule = lambda state: (state.count("Progressive Life - Komachi", world.player) >= midaccess - 1)
        s8komachi.access_rule = lambda state: (state.count("Progressive Life - Komachi", world.player) >= midaccess)
        s9komachi.access_rule = lambda state: (state.count("Progressive Life - Komachi", world.player) >= s9access)
    if enable_shikieiki == True:
        s6shikieiki = multiworld.get_location("Shikieiki - Stage 6 Clear", player)
        s7shikieiki = multiworld.get_location("Shikieiki - Stage 7 Clear", player)
        s8shikieiki = multiworld.get_location("Shikieiki - Stage 8 Clear", player)
        s9shikieiki = multiworld.get_location("Shikieiki - Stage 9 Clear", player)
        s6shikieiki.access_rule = lambda state: (state.count("Progressive Life - Shikieiki", world.player) >= midaccess - 2)
        s7shikieiki.access_rule = lambda state: (state.count("Progressive Life - Shikieiki", world.player) >= midaccess - 1)
        s8shikieiki.access_rule = lambda state: (state.count("Progressive Life - Shikieiki", world.player) >= midaccess)
        s9shikieiki.access_rule = lambda state: (state.count("Progressive Life - Shikieiki", world.player) >= s9access)

    if enable_aya == True:
        s6aya = multiworld.get_location("Aya - Stage 6 Clear", player)
        s7aya = multiworld.get_location("Aya - Stage 7 Clear", player)
        s8aya = multiworld.get_location("Aya - Stage 8 Clear", player)
        s9aya = multiworld.get_location("Aya - Stage 9 Clear", player)
        if difficulty_ayamedi == False:
            s6aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= 0)
            s7aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= 0)
            s8aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= 0)
            s9aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= 0)
        else:
            s6aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= midaccess - 2)
            s7aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= midaccess - 1)
            s8aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= midaccess)
            s9aya.access_rule = lambda state: (state.count("Progressive Life - Aya", world.player) >= s9access)
    if enable_medicine == True:
        s6medicine = multiworld.get_location("Medicine - Stage 6 Clear", player)
        s7medicine = multiworld.get_location("Medicine - Stage 7 Clear", player)
        s8medicine = multiworld.get_location("Medicine - Stage 8 Clear", player)
        s9medicine = multiworld.get_location("Medicine - Stage 9 Clear", player)
        if difficulty_ayamedi == False:
            s6medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= 0)
            s7medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= 0)
            s8medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= 0)
            s9medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= 0)
        else:
            s6medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= midaccess - 2)
            s7medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= midaccess - 1)
            s8medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= midaccess)
            s9medicine.access_rule = lambda state: (state.count("Progressive Life - Medicine", world.player) >= s9access)

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
