# Basic structure for a text-based RPG

# --- Game World ---
world = {
    "station_entrance": {
        "description": "You are at the entrance of a dimly lit metro station. Stairs lead down into the darkness. The air is stale and a faint metallic scent hangs in the air. An old man in greasy overalls, Engineer Elias, tinkers with a flickering lamp nearby.",
        "exits": {"down": "platform", "east": "security_checkpoint"},
        "items": ["rusty_pipe"],
        "details": {
            "stairs": "The stairs are made of cracked concrete, disappearing into the gloom below.",
            "lamp": "The lamp sputters, casting dancing shadows. Elias seems focused on fixing it."
        },
        "npcs": {
            "elias": { 
                "name": "Engineer Elias",
                "description": "Engineer Elias is an old but sturdy man. He looks weary but his eyes show a spark of determination.",
                "dialogue": {
                    "greeting": "Hmph. Another wanderer. Most just scavenge these days. Are you looking for something more?",
                    "offer_main_quest": "This old station... it's dying. But there's a communication array in the old Control Room, deep in the tunnels. If someone could reach it, maybe... just maybe, we could send a signal, find out if there's anyone else out there. The way is through the old Engine Room, south of the main platform. Will you try to reach the Control Room?",
                    "quest_accepted": "Good. Be careful. The tunnels are treacherous. Find the Engine Room, which has a door to the Control Room.", # Changed this line
                    "quest_reminder": "You need to get to the Control Room. It should be accessible from the Engine Room.",
                    "quest_completed_already": "You've done well with the array. There's nothing more I can ask of you for that.",
                    "default": "Keep your wits about you in those tunnels."
                },
                "quest_id": "main_comms_array" 
            }
        }
    },
    "platform": {
        "description": "You are on a dusty platform. An old, stationary train rests here. Faint echoes of dripping water can be heard.",
        "exits": {"up": "station_entrance", "train": "train_car", "south": "flooded_tunnel", "west": "market_station"},
        "items": ["old_ticket"]
    },
    "train_car": {
        "description": "You are inside a graffiti-covered train car. The seats are torn and the floor is littered with debris. The doors are jammed open to the platform.",
        "exits": {"platform": "platform"},
        "items": ["newspaper", "empty_bottle"]
    },
    "market_station": {
        "description": "This section of the tunnels has been converted into a makeshift market. Stalls made of scrap metal line the walls, dimly lit by flickering lanterns. A gruff-looking Vendor eyes you from behind a counter.",
        "exits": {"east": "platform", "north": "abandoned_depot"},
        "items": ["ration_pack", "rope"],
        "npcs": {
            "vendor": { # Changed to new NPC structure
                "name": "Vendor",
                "description": "The Vendor is a burly figure with a scarred face. He doesn't say much, just watches your every move.",
                "dialogue": {
                    "greeting": "Need something or just browsing?",
                    "default": "Don't cause any trouble."
                }
                # No quest_id for the vendor for now
            }
        }
    },
    "flooded_tunnel": {
        "description": "Water pools ankle-deep in this tunnel, and the air is damp and cold. Strange fungi glow faintly on the walls. A narrow, slippery walkway skirts the edge of the deeper water. You hear a faint skittering sound.",
        "exits": {"north": "platform", "south": "engine_room"},
        "items": ["glowing_fungus", "scrap_metal"],
        "enemies": [
            {"name": "Giant Rat", "health": 8, "attack_power": 3, "agility": 2, "loot": "rat_tail"}
        ]
    },
    "abandoned_depot": {
        "description": "An old train depot, filled with rusting hulks of metro cars. Cobwebs hang thick as curtains, and the silence is unnerving. A faint scurrying sound comes from the shadows.",
        "exits": {"south": "market_station"},
        "items": ["crowbar", "old_map_fragment", "antique_glasses"] # Quest item for Librarian Agnes
    },
    "security_checkpoint": {
        "description": "A deserted security checkpoint. Barricades are pushed aside, and a guard booth stands empty, its window cracked. Warning posters about mutants are peeling from the walls.",
        "exits": {"west": "station_entrance", "east": "makeshift_library"},
        "items": ["ammo_clip", "first_aid_kit"]
    },
    "engine_room": {
        "description": "The air hums with the sound of ancient generators. The room is hot and filled with the smell of oil and ozone. Catwalks crisscross above massive, chugging machinery. A reinforced door is set into the far wall, marked 'CONTROL ROOM'.",
        "exits": {"north": "flooded_tunnel", "south": "control_room"}, # New exit to control_room
        "items": ["battery", "copper_wire"]
    },
    "makeshift_library": {
        "description": "Someone has turned this quiet alcove into a small library. Shelves made of crates hold a surprisingly large collection of pre-war books. Librarian Agnes, an elderly woman, is meticulously organizing scrolls.",
        "exits": {"west": "security_checkpoint"},
        "items": ["old_book", "reading_glasses"], 
        "npcs": {
            "agnes": { 
                "name": "Librarian Agnes", 
                "description": "Librarian Agnes is a thin, elderly woman with kind eyes. She seems worried about something.",
                "dialogue": {
                    "greeting": "Oh, hello dear. Welcome to our little sanctuary of knowledge.",
                    "offer_side_quest": "I seem to have misplaced my antique reading glasses. They're not very good for reading anymore, but they have... sentimental value. I think I might have left them in the old Abandoned Depot when I was looking for salvage. Could you possibly keep an eye out for them if you're heading that way?",
                    "quest_accepted": "Oh, thank you, dear! That would be wonderful. They are a pair of simple, wire-rimmed glasses.",
                    "quest_reminder": "Have you found my antique glasses? I believe they might be in the Abandoned Depot.",
                    "quest_item_not_found": "Oh, you don't seem to have them with you. Well, do keep looking if you can. I'd be ever so grateful.",
                    "completion": "My glasses! Oh, thank you, thank you! I know they're just old things, but they meant a lot to me. Please, take this valuable book as a token of my gratitude. It's a rare pre-war edition.",
                    "quest_completed_already": "Thank you again for finding my glasses, dear. That book I gave you is quite special."
                },
                "quest_id": "side_librarian_glasses",
                "quest_item_needed": "antique_glasses", # Item player needs to have
                "reward_item": "valuable_book"        # Item player receives
            }
        },
        "details": {
            "shelves": "The shelves are crammed with books of all kinds, from technical manuals to tattered novels."
        }
    },
    "control_room": {
        "description": "This must be the Control Room Elias mentioned. Dust-covered consoles line the walls, their screens dark. A large central terminal hums faintly. There's a panel here that looks like it could be activated.",
        "exits": {"north": "engine_room"},
        "items": ["circuit_board", "log_entry_1"], # Added a log entry for flavor
        "details": {
            "consoles": "Most consoles are dead, but a few flicker with residual power. One displays a garbled message: '...SYSTEM OFFLINE...AUX_POWER_LOW...MAIN_ARRAY_STATUS: UNKNOWN...'",
            "terminal": "The main terminal seems to be drawing power. A small maintenance hatch is open on its side.",
            "panel": "A large, inviting button on the panel glows faintly green. It's labeled 'COMM_ARRAY_ACTIVATION'."
        },
        "on_enter_event": "main_quest_control_room_entry" # For main quest completion logic in handle_go
    }
}

# --- Player ---
player_inventory = []
player_stats = {
    "name": "Survivor",
    "max_health": 20,
    "current_health": 20,
    "strength": 5, 
    "agility": 3   
}
player_quests = {
    "main_comms_array": "inactive", # Was main_polis_message
    "side_librarian_glasses": "inactive"
}
current_location = "station_entrance"

# --- Enemy Definitions (can be expanded) ---
# Enemies will be placed directly in the location data.
# Example structure for an enemy in a location's 'enemies' list:
# {'name': 'Mutant Rat', 'health': 5, 'attack_power': 2, 'agility': 1, 'loot': 'rat_tail'}


# --- Command Handlers ---
def handle_stats(args):
    """Handles the 'stats' command."""
    print(f"\n--- {player_stats['name']}'s Stats ---")
    print(f"Health: {player_stats['current_health']}/{player_stats['max_health']}")
    print(f"Strength: {player_stats['strength']}")
    print(f"Agility: {player_stats['agility']}")
    print("--------------------")

def handle_help(args):
    """Handles the 'help' command."""
    print("\n--- Available Commands ---")
    print("  look              - Describe your current location, including items, NPCs, and enemies.")
    print("  look at [thing]   - Describe a specific item, NPC, or detail in your location.")
    print("  go [direction]    - Move in the specified direction (e.g., 'go north').")
    print("  take [item]       - Pick up an item from your location and add it to your inventory.")
    print("  inventory / inv   - Show the items you are currently carrying.")
    print("  stats             - Display your character's current health and attributes.")
    print("  attack [target]   - Attack an enemy in your current location (e.g., 'attack rat').")
    print("  fight [target]    - Alias for 'attack'.")
    print("  talk to [npc]     - Speak with an NPC in your current location (e.g., 'talk to elias').")
    print("  quests / journal  - View the status of your current quests.")
    print("  help              - Show this list of commands.")
    print("  quit / exit       - Exit the game.")
    print("--------------------")

def handle_quests(args):
    """Handles the 'quests' or 'journal' command."""
    global player_quests
    print("\n--- Your Quests ---")
    active_quests_found = False
    completed_quests_found = False

    # Main Quest: Comms Array
    if player_quests.get("main_comms_array") == "active":
        print("- (Active) The Signal: Reach the Control Room to investigate the old communication array. Elias mentioned it's accessible via the Engine Room.")
        active_quests_found = True
    elif player_quests.get("main_comms_array") == "completed":
        print("- (Completed) The Signal: You reached the Control Room and activated the communication array panel.")
        completed_quests_found = True
    
    # Side Quest: Librarian's Glasses
    if player_quests.get("side_librarian_glasses") == "active":
        print("- (Active) Lost & Found: Find Librarian Agnes's antique_glasses. She thinks they are in the Abandoned Depot.")
        active_quests_found = True
    elif player_quests.get("side_librarian_glasses") == "completed":
        print("- (Completed) Lost & Found: You returned the antique_glasses to Librarian Agnes and received a valuable_book.")
        completed_quests_found = True

    if not active_quests_found and not completed_quests_found:
        # Check if there are any quests at all, even if all are inactive
        if any(status == "inactive" for status in player_quests.values()):
             print("You have potential quests available. Try talking to people in the stations.")
        else: # This case should ideally not be hit if quests are defined
            print("You have no quests at this time.")
    elif not active_quests_found and completed_quests_found:
        print("You have no active quests, only completed ones.")
    elif active_quests_found and not completed_quests_found:
        pass # Already printed active quests
    # If both are true, both sections are printed.
    print("--------------------")

def handle_look(args):
    """Handles the 'look' command."""
    global current_location
    global player_quests
    location_data = world.get(current_location)
    if not location_data:
        print("Error: Unknown location!")
        return

    print(location_data["description"])

    if location_data.get("npcs"):
        for npc_id, npc_data_val in location_data["npcs"].items():
            if isinstance(npc_data_val, dict): # New NPC structure
                npc_name_display = npc_data_val.get("name", npc_id.capitalize())
                base_desc = npc_data_val.get("description", f"You see {npc_name_display}.")
                
                quest_hint = ""
                npc_quest_id = npc_data_val.get("quest_id")
                # Only show "wants to talk" hint if there's an actual quest to offer
                if npc_quest_id and player_quests.get(npc_quest_id) == "inactive" and \
                   (npc_data_val.get("dialogue", {}).get("offer_main_quest") or \
                    npc_data_val.get("dialogue", {}).get("offer_side_quest")):
                    quest_hint = f" {npc_name_display} looks like they might want to talk. (Try 'talk to {npc_id}')"
                print(base_desc + quest_hint)
            else: # Old format NPC description (just a string for simple NPCs like Vendor initially was)
                print(f"You see {npc_id.capitalize()}. {npc_data_val}") # Should be less common now

    if location_data.get("enemies"):
        print("Enemies present:")
        for enemy in location_data["enemies"]:
            enemy_name = enemy.get('name', 'Unknown Enemy')
            enemy_health = enemy.get('health', 'N/A')
            print(f"- {enemy_name} (Health: {enemy_health})")

    if location_data.get("items"):
        print("Items here: " + ", ".join(location_data["items"]))
    else:
        print("You see no items here.")

    available_exits = ", ".join(location_data["exits"].keys())
    if available_exits:
        print(f"Exits: {available_exits}")
    else:
        print("There are no obvious exits.")

    # Placeholder for looking at specific details
    if len(args) > 0 and args[0] == "at":
        if len(args) > 1:
            detail_name = args[1].lower() # e.g. "elias" or "stairs"
            if "details" in location_data and detail_name in location_data["details"]:
                print(location_data["details"][detail_name])
            # Looking AT an NPC
            elif "npcs" in location_data and detail_name in location_data["npcs"]:
                npc_data_val = location_data["npcs"][detail_name]
                if isinstance(npc_data_val, dict):
                    npc_name_display = npc_data_val.get("name", detail_name.capitalize())
                    desc = npc_data_val.get("description", f"You see {npc_name_display}.")
                    
                    quest_hint = ""
                    npc_quest_id = npc_data_val.get("quest_id")
                    if npc_quest_id: # Check if NPC is related to any quest
                        quest_status = player_quests.get(npc_quest_id, "unavailable")
                        if quest_status == "inactive":
                            quest_hint = f" They seem to want to discuss something. (Try 'talk to {detail_name}')"
                        elif quest_status == "active":
                            quest_hint = f" You have an ongoing task for them."
                        elif quest_status == "completed":
                            quest_hint = f" You've already helped them."
                    print(desc + quest_hint)
                else: # Old format
                    print(npc_data_val) # Show original string desc
            elif "items" in location_data and detail_name in location_data["items"]:
                 print(f"It's a {detail_name}.") 
            else:
                print(f"You don't see any specific details about '{detail_name}' here.")
        else:
            print("Look at what?")


def handle_talk(args):
    """Handles the 'talk to [npc]' command."""
    global current_location
    global player_quests
    global player_inventory # Needed for quest item checks & rewards

    if not args:
        print("Talk to whom?")
        return

    npc_target_name_part = args[0].lower()
    location_data = world.get(current_location)

    if not location_data.get("npcs"):
        print("There's no one to talk to here.")
        return

    found_npc_id = None
    npc_data_to_use = None 

    for current_npc_id, current_npc_data_val in location_data["npcs"].items():
        if npc_target_name_part in current_npc_id.lower(): # e.g. "elias" in "elias"
            if isinstance(current_npc_data_val, dict): # Make sure we're dealing with new NPC structure
                found_npc_id = current_npc_id
                npc_data_to_use = current_npc_data_val
                break
            else: # Should not happen if all NPCs are converted
                print(f"DEBUG: NPC {current_npc_id} is not in the new format.") 
                return
    
    if not npc_data_to_use:
        print(f"You don't see anyone called '{npc_target_name_part}' here to talk to like that.")
        return

    npc_display_name = npc_data_to_use.get("name", found_npc_id.capitalize())
    dialogue = npc_data_to_use.get("dialogue", {})
    quest_id = npc_data_to_use.get("quest_id")
    
    print(f"\nYou approach {npc_display_name}.")

    if quest_id: # NPC is related to a quest
        quest_status = player_quests.get(quest_id, "unavailable") 

        if quest_status == "inactive":
            offer_dialogue_key = None
            if quest_id == "main_comms_array" and "offer_main_quest" in dialogue:
                offer_dialogue_key = "offer_main_quest"
            elif quest_id == "side_librarian_glasses" and "offer_side_quest" in dialogue:
                offer_dialogue_key = "offer_side_quest"
            
            if offer_dialogue_key:
                print(f"{npc_display_name}: \"{dialogue[offer_dialogue_key]}\"")
                accept_input = input(f"Help {npc_display_name}? (yes/no): ").strip().lower()
                if accept_input == "yes" or accept_input == "y":
                    player_quests[quest_id] = "active"
                    print(f"{npc_display_name}: \"{dialogue.get('quest_accepted', 'Thank you! Your help is appreciated.')}\"")
                else:
                    print(f"{npc_display_name}: \"{dialogue.get('quest_declined', 'Oh, alright then. Let me know if you change your mind.')}\"")
            else: # NPC has a quest_id but no specific offer dialogue for inactive state
                 print(f"{npc_display_name}: \"{dialogue.get('greeting', 'They look at you but say little.')}\"")
        
        elif quest_status == "active":
            if quest_id == "side_librarian_glasses" and npc_data_to_use.get("quest_item_needed"):
                item_needed = npc_data_to_use["quest_item_needed"]
                if item_needed in player_inventory:
                    print(f"{npc_display_name}: \"{dialogue.get('completion', 'You found it! Amazing!')}\"")
                    player_inventory.remove(item_needed)
                    print(f"(You hand over the {item_needed}.)")
                    reward = npc_data_to_use.get("reward_item")
                    if reward:
                        player_inventory.append(reward)
                        print(f"You received a {reward} as a reward!")
                    player_quests[quest_id] = "completed"
                else:
                    print(f"{npc_display_name}: \"{dialogue.get('quest_item_not_found', 'Still looking for it? I believe it was in the Abandoned Depot.')}\"")
            elif quest_id == "main_comms_array":
                 print(f"{npc_display_name}: \"{dialogue.get('quest_reminder', 'Any progress on reaching the Control Room?')}\"")
            else: 
                print(f"{npc_display_name}: \"{dialogue.get('quest_reminder', 'How is that task coming along?')}\"")
        
        elif quest_status == "completed":
            print(f"{npc_display_name}: \"{dialogue.get('quest_completed_already', 'Thanks again for your help!')}\"")
        
        else: # Should not happen if quests are initialized correctly
            print(f"{npc_display_name}: \"{dialogue.get('default', 'Nothing more to say right now.')}\"")
    else: # NPC has no quest_id
        print(f"{npc_display_name}: \"{dialogue.get('greeting', dialogue.get('default', 'They nod at you.'))}\"")


def handle_go(args):
    """Handles the 'go' command."""
    global current_location
    global player_quests # Needed for quest events on room entry
    if not args:
        print("Go where?")
        return

    direction = args[0].lower()
    current_room_data = world.get(current_location) # Data of the room we are IN

    if current_room_data and direction in current_room_data["exits"]:
        next_location_id = current_room_data["exits"][direction]
        if next_location_id in world:
            current_location = next_location_id
            print(f"\nYou go {direction}...") # Added newline for better spacing
            
            # --- Main Quest Completion Check ---
            new_location_data = world.get(current_location) # Data for the new room player entered
            if new_location_data and new_location_data.get("on_enter_event") == "main_quest_control_room_entry":
                if player_quests.get("main_comms_array") == "active":
                    print("\n[QUEST COMPLETED] As you step into the Control Room, a panel on the main terminal flickers to life with a soft green glow. You've successfully activated the communication array panel!")
                    print("Elias will be pleased to hear the station's core systems are responsive again.")
                    player_quests["main_comms_array"] = "completed"
                    # To prevent re-triggering, we rely on the quest status check.
            
            handle_look([]) # Automatically look around after moving
        else:
            print(f"Error: The path {direction} leads to an unknown place.")
    else:
        print(f"You can't go {direction}.")


def handle_attack(args):
    """Handles the 'attack' command."""
    global current_location
    global player_stats
    # No need to pass 'world' as global, it's already accessible

    location_data = world.get(current_location)
    if not location_data or not location_data.get("enemies"):
        print("There's nothing to attack here.")
        return

    if not args:
        print("Attack what? (e.g., 'attack rat')")
        return

    target_name_part = args[0].lower()
    target_enemy = None
    enemy_index = -1

    # Find the enemy
    for i, enemy in enumerate(location_data["enemies"]):
        if target_name_part in enemy["name"].lower():
            target_enemy = enemy
            enemy_index = i
            break
    
    if not target_enemy:
        print(f"You don't see a '{target_name_part}' to attack here.")
        return

    # --- Combat Round ---
    print(f"\n--- Combat with {target_enemy['name']} ---")

    # Player's attack
    player_damage = player_stats["strength"] 
    target_enemy["health"] -= player_damage
    print(f"You strike the {target_enemy['name']} for {player_damage} damage.")

    if target_enemy["health"] <= 0:
        print(f"You defeated the {target_enemy['name']}!")
        # Add loot to room 
        if target_enemy.get("loot"):
            # Ensure items list exists
            if "items" not in location_data:
                location_data["items"] = []
            location_data["items"].append(target_enemy["loot"])
            print(f"The {target_enemy['name']} dropped a {target_enemy['loot']}.")
        
        location_data["enemies"].pop(enemy_index) # Remove defeated enemy
        
        # If no more enemies, clear the enemies list to be sure
        if not location_data["enemies"]:
            del location_data["enemies"]
        return # Combat ends

    # Enemy's attack (if still alive)
    # Basic hit chance (optional, can be expanded)
    # For now, enemy always hits if player didn't defeat it.
    enemy_damage = target_enemy["attack_power"]
    player_stats["current_health"] -= enemy_damage
    print(f"The {target_enemy['name']} retaliates, hitting you for {enemy_damage} damage.")

    if player_stats["current_health"] <= 0:
        player_stats["current_health"] = 0 # Prevent negative health display
        print(f"Your health: {player_stats['current_health']}/{player_stats['max_health']}.")
        print("\nYou have succumbed to your wounds. Your adventure ends here.")
        print("Game Over.")
        # The main game loop will catch the zero health and exit.
    else:
        print(f"Your health: {player_stats['current_health']}/{player_stats['max_health']}.")
    print("--------------------")


def handle_take(args):
    """Handles the 'take' command."""
    global current_location
    global player_inventory
    if not args:
        print("Take what?")
        return

    item_name = args[0].lower()
    location_data = world.get(current_location)

    if location_data and item_name in location_data["items"]:
        player_inventory.append(item_name)
        location_data["items"].remove(item_name)
        print(f"You take the {item_name}.")
    else:
        print(f"You don't see a {item_name} here.")

def handle_inventory(args):
    """Handles the 'inventory' command."""
    global player_inventory
    if player_inventory:
        print("You are carrying: " + ", ".join(player_inventory))
    else:
        print("Your inventory is empty.")

def handle_quit(args):
    """Handles the 'quit' command."""
    print("Thanks for playing!")
    exit()

# --- Command Parser ---
commands = {
    "look": handle_look,
    "go": handle_go,
    "take": handle_take,
    "inventory": handle_inventory,
    "stats": handle_stats,
    "attack": handle_attack,
    "fight": handle_attack, # Alias for attack
    "quests": handle_quests,
    "journal": handle_quests, # Alias for quests
    "talk": handle_talk,
    "help": handle_help,      # New command
    "quit": handle_quit,
    "exit": handle_quit # Alias for quit
}

# --- Main Game Loop ---
def game_loop():
    """Main loop for the game."""
    global player_stats # Ensure we can modify the global player_stats

    print("Welcome to the Metro Adventure Game!")
    
    # Character Creation
    player_name = input("Enter your character's name (default: Survivor): ").strip()
    if player_name:
        player_stats["name"] = player_name
    
    # Initialize stats (can be more complex later)
    player_stats["max_health"] = 20
    player_stats["current_health"] = player_stats["max_health"] # Start with full health
    player_stats["strength"] = 5
    player_stats["agility"] = 3

    # Initialize Quests
    global player_quests
    player_quests = {
        "main_comms_array": "inactive", # Updated quest key
        "side_librarian_glasses": "inactive"
    }
    
    print(f"\nWelcome, {player_stats['name']}! Your adventure begins.")
    handle_stats([]) # Show initial stats
    # Initial hint for main quest
    print("\nEngineer Elias, in the station entrance, looks like he has something important to tell you. (Try 'talk to elias')") 
    
    handle_look([]) # Initial look around

    while True:
        # Check for game over condition at the start of each loop iteration
        if player_stats["current_health"] <= 0:
            # This check ensures game ends if health drops to 0 outside of direct combat loop
            # (e.g. future traps or poison)
            # Message is printed by handle_attack or other future damage sources
            break # Exit the main game loop

        try:
            # Update prompt to show current health
            prompt = f"\n({player_stats['current_health']}/{player_stats['max_health']} HP) > "
            player_input = input(prompt).strip().lower()
            if not player_input:
                continue

            parts = player_input.split()
            command = parts[0]
            args = parts[1:]

            if command in commands:
                commands[command](args)
            else:
                print("Unknown command. Type 'help' for a list of commands.") # Updated help hint
        except EOFError:
            print("\nQuitting game (EOF detected).")
            break
        except KeyboardInterrupt:
            print("\nQuitting game (interrupt signal).")
            break

if __name__ == "__main__":
    game_loop()
