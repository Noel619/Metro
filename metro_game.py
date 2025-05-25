# -*- coding: utf-8 -*-
# Basic structure for a text-based RPG
import random
import json # For saving and loading
import copy # For deepcopying game state
import tkinter as tk
from tkinter import Menu, simpledialog, messagebox, filedialog
# Attempt to import Pillow (PIL)
try:
    from PIL import Image, ImageTk
except ImportError:
    # If Pillow is not installed, this subtask should include instructions
    # to the user or attempt to install it if the environment allows.
    # For now, we'll assume the worker can install it.
    # If direct installation within the subtask isn't feasible,
    # the subtask should report back that Pillow needs to be installed.
    messagebox.showerror("Error", "Pillow library is not installed. Please install it to use image features (e.g., pip install Pillow)") # Or parent=None if self is not available
    # Then raise an error or return to prevent further execution of this specific feature
    raise ImportError("Pillow library not found. Please install it.")

# --- Item Display Names (Spanish) ---
ITEM_DISPLAY_NAMES = {
    "rusty_pipe": "tubo oxidado",
    "old_ticket": "billete viejo",
    "newspaper": "periódico",
    "empty_bottle": "botella vacía",
    "ration_pack": "paquete de raciones",
    "rope": "cuerda",
    "glowing_fungus": "hongo brillante",
    "scrap_metal": "chatarra",
    "rat_tail": "cola de rata",
    "ammo_scraps": "restos de munición", 
    "mutant_claws": "garras de mutante", 
    "crowbar": "palanca",
    "old_map_fragment": "fragmento de mapa viejo",
    "antique_glasses": "gafas antiguas", 
    "moldy_bread": "pan mohoso", 
    "ammo_clip": "cargador de munición",
    "first_aid_kit": "botiquín de primeros auxilios",
    "bandage": "venda",
    "battery": "batería",
    "copper_wire": "cable de cobre",
    "old_book": "libro viejo",
    "reading_glasses": "gafas de lectura", 
    "valuable_book": "libro valioso", 
    "circuit_board": "placa de circuito",
    "log_entry_1": "entrada de diario 1",
    "cache_of_military_rounds": "reserva de munición militar"
}

# --- Game World ---
world = {
    "station_entrance": {
        "description": "Estás en la entrada de una estación de metro tenuemente iluminada. Unas escaleras descienden hacia la oscuridad. El aire está viciado y un leve olor metálico flota en el ambiente. Un anciano con mono grasiento, el Ingeniero Elías, juguetea con una lámpara parpadeante cercana.",
        "exits": {"down": "platform", "east": "security_checkpoint"},
        "items": ["rusty_pipe"], 
        "details": {
            "stairs": "Las escaleras son de hormigón agrietado y desaparecen en la penumbra inferior.",
            "lamp": "La lámpara chisporrotea, proyectando sombras danzantes. Elías parece concentrado en arreglarla."
        },
        "npcs": {
            "elias": { 
                "name": "Ingeniero Elías",
                "description": "El Ingeniero Elías es un hombre anciano pero robusto. Parece cansado, pero sus ojos muestran una chispa de determinación.",
                "dialogue": {
                    "greeting": "Mmm. Otro trotamundos. La mayoría solo busca chatarra estos días. ¿Tú buscas algo más?",
                    "offer_main_quest": "Esta vieja estación... se está muriendo. Pero hay una antena de comunicaciones en la antigua Sala de Control, en lo profundo de los túneles. Si alguien pudiera llegar hasta ella, tal vez... solo tal vez, podríamos enviar una señal, averiguar si queda alguien más ahí fuera. El camino es a través de la vieja Sala de Máquinas, al sur del andén principal. ¿Intentarás llegar a la Sala de Control?",
                    "quest_accepted": "Bien. Ten cuidado. Los túneles son traicioneros. Encuentra la Sala de Máquinas, que tiene una puerta a la Sala de Control.",
                    "quest_reminder": "Necesitas llegar a la Sala de Control. Debería ser accesible desde la Sala de Máquinas.",
                    "quest_completed_already": "Has hecho un buen trabajo con la antena. No hay nada más que pueda pedirte al respecto.",
                    "default": "Mantente alerta en esos túneles."
                },
                "quest_id": "main_comms_array" 
            }
        }
    },
    "platform": {
        "description": "Estás en un andén polvoriento. Un viejo tren inmóvil descansa aquí. Se oyen débiles ecos de agua goteando.",
        "exits": {"up": "station_entrance", "train": "train_car", "south": "flooded_tunnel", "west": "market_station"},
        "items": ["old_ticket"]
    },
    "train_car": {
        "description": "Estás dentro de un vagón de tren cubierto de grafitis. Los asientos están rasgados y el suelo lleno de escombros. Las puertas están atascadas, abiertas hacia el andén.",
        "exits": {"platform": "platform"},
        "items": ["newspaper", "empty_bottle"]
    },
    "market_station": {
        "description": "Esta sección de los túneles ha sido convertida en un mercado improvisado. Puestos hechos de chatarra se alinean en las paredes, tenuemente iluminados por farolillos parpadeantes. Un Vendedor de aspecto rudo te observa desde detrás de un mostrador.",
        "exits": {"east": "platform", "north": "abandoned_depot"},
        "items": ["ration_pack", "rope"],
        "npcs": {
            "vendor": { 
                "name": "Vendedor",
                "description": "El Vendedor es una figura corpulenta con una cara llena de cicatrices. No habla mucho, solo observa cada uno de tus movimientos.",
                "dialogue": {
                    "greeting": "¿Necesitas algo o solo estás mirando?",
                    "default": "No causes problemas."
                }
            }
        }
    },
    "flooded_tunnel": {
        "description": "El agua llega hasta los tobillos en este túnel, y el aire es húmedo y frío. Extraños hongos brillan tenuemente en las paredes. Una pasarela estrecha y resbaladiza bordea el agua más profunda. Oyes débiles correteos y a veces vislumbras algo moviéndose en las sombras.",
        "exits": {"north": "platform", "south": "engine_room"},
        "items": ["glowing_fungus", "scrap_metal"],
        "enemies": [
            {"name": "Rata Gigante", "description": "Un roedor grande y agresivo, común en estos túneles.", "health": 8, "attack_power": 3, "agility": 2, "loot": ["rat_tail"], "xp_value": 25},
            {"name": "Acechador", "description": "Una figura sombría que parece mezclarse con la tenue luz. Sus ojos brillan y se mueve con una velocidad inquietante, lo que dificulta acertarle.", "health": 35, "attack_power": 6, "loot": ["ammo_scraps", "mutant_claws"], "xp_value": 75}
        ]
    },
    "abandoned_depot": {
        "description": "Una vieja cochera de trenes, llena de armazones oxidados de vagones de metro. Las telarañas cuelgan espesas como cortinas y el silencio es desconcertante. Un leve correteo y el ocasional ruido metálico resuenan desde el interior. Sientes como si te observaran ojos desesperados.",
        "exits": {"south": "market_station"},
        "items": ["crowbar", "old_map_fragment", "antique_glasses"], 
        "enemies": [
            {"name": "Humano Salvaje Carroñero", "description": "Un Humano Salvaje demacrado, moviéndose entre las sombras, agarrando una daga oxidada.", "health": 18, "attack_power": 7, "loot": ["scrap_metal", "bandage"], "xp_value": 45},
            {"name": "Humano Salvaje Matón", "description": "Un Humano Salvaje más grande e imponente, blandiendo una pesada tubería con aire amenazante.", "health": 25, "attack_power": 9, "loot": ["scrap_metal", "bandage", "moldy_bread"], "xp_value": 60}
        ]
    },
    "security_checkpoint": {
        "description": "Un puesto de control desierto. Las barricadas están apartadas y una garita de guardia está vacía, con la ventana rota. Carteles de advertencia sobre mutantes se despegan de las paredes. El Capitán Dimitri monta guardia, con aspecto sombrío.",
        "exits": {"west": "station_entrance", "east": "makeshift_library"},
        "items": ["ammo_clip", "first_aid_kit"],
        "npcs": {
            "dimitri": {
                "name": "Capitán Dimitri",
                "description": "Dimitri es un hombre de rostro severo con una armadura de guardia desgastada. Tiene la mirada cansada de alguien que ha visto demasiado.",
                "dialogue": {
                    "greeting": "¡Alto! Identifícate. Este puesto de control está en alerta máxima.",
                    "offer_tunnel_clearing_quest": "La vieja cochera cercana se ha convertido en un nido de Humanos Salvajes. Se están volviendo más audaces, amenazando nuestro perímetro. Necesitamos a alguien que entre allí y... los disuada. Permanentemente. Elimina a dos de ellos y haré que valga la pena. ¿Interesado?",
                    "quest_accepted": "Bien. Ten cuidado. Son rápidos y están desesperados. Dos menos de ellos harán esta zona más segura para todos.",
                    "quest_reminder_incomplete": "El problema de los Humanos Salvajes en la cochera aún no está resuelto. Necesito que elimines a {remaining} más.",
                    "completion": "¿Has diezmado a esos Salvajes? Buen trabajo. No muchos se arriesgarían. Aquí tienes tu paga: una reserva de munición militar. Y te has ganado esto.",
                    "quest_completed_already": "Gracias de nuevo por limpiar ese nido. Las cosas han estado más tranquilas.",
                    "default": "Mantente vigilante. Los túneles nunca son verdaderamente seguros."
                },
                "quest_id": "tunnel_clearing_quest",
                "reward_item": "cache_of_military_rounds",
                "xp_reward": 100
            }
        }
    },
    "engine_room": {
        "description": "El aire vibra con el sonido de generadores antiguos. La sala está caliente y llena de olor a aceite y ozono. Pasarelas cruzan por encima de maquinaria masiva y ruidosa. Una puerta reforzada está incrustada en la pared del fondo, con la inscripción 'SALA DE CONTROL'.",
        "exits": {"north": "flooded_tunnel", "south": "control_room"},
        "items": ["battery", "copper_wire"]
    },
    "makeshift_library": {
        "description": "Alguien ha convertido este tranquilo rincón en una pequeña biblioteca. Estanterías hechas de cajas contienen una sorprendente colección de libros de antes de la guerra. La Bibliotecaria Agnes, una mujer anciana, organiza meticulosamente unos pergaminos.",
        "exits": {"west": "security_checkpoint"},
        "items": ["old_book", "reading_glasses"], 
        "npcs": {
            "agnes": { 
                "name": "Bibliotecaria Agnes", 
                "description": "La Bibliotecaria Agnes es una mujer delgada y anciana con ojos amables. Parece preocupada por algo.",
                "dialogue": {
                    "greeting": "Oh, hola querido/a. Bienvenido/a a nuestro pequeño santuario del saber.",
                    "offer_side_quest": "Parece que he perdido mis antiguas gafas de leer. Ya no sirven mucho para leer, pero tienen... valor sentimental. Creo que las dejé en la vieja Cochera Abandonada cuando buscaba trastos. ¿Podrías echar un vistazo si vas por allí?",
                    "quest_accepted": "¡Oh, gracias, querido/a! Sería maravilloso. Son unas gafas sencillas, con montura de alambre.",
                    "quest_reminder": "¿Has encontrado mis gafas antiguas? Creo que podrían estar en la Cochera Abandonada.",
                    "quest_item_not_found": "Oh, parece que no las tienes contigo. Bueno, sigue buscando si puedes. Te lo agradecería enormemente.",
                    "completion": "¡Mis gafas! ¡Oh, gracias, gracias! Sé que son solo cosas viejas, pero significaban mucho para mí. Por favor, toma este libro valioso como muestra de mi gratitud. Es una edición rara de antes de la guerra.",
                    "quest_completed_already": "Gracias de nuevo por encontrar mis gafas, querido/a. Ese libro que te di es bastante especial."
                },
                "quest_id": "side_librarian_glasses",
                "quest_item_needed": "antique_glasses", 
                "reward_item": "valuable_book",
                "xp_reward": 75
            }
        },
        "details": {
            "shelves": "Las estanterías están repletas de libros de todo tipo, desde manuales técnicos hasta novelas andrajosas."
        }
    },
    "control_room": {
        "description": "Esta debe ser la Sala de Control que mencionó Elías. Consolas cubiertas de polvo bordean las paredes, con las pantallas oscuras. Una gran terminal central zumba débilmente. Hay un panel aquí que parece que podría activarse.",
        "exits": {"north": "engine_room"},
        "items": ["circuit_board", "log_entry_1"],
        "details": {
            "consoles": "La mayoría de las consolas están muertas, pero algunas parpadean con energía residual. Una muestra un mensaje confuso: '...SISTEMA OFFLINE...ENERGÍA_AUX_BAJA...ESTADO_ANTENA_PRINCIPAL: DESCONOCIDO...'",
            "terminal": "La terminal principal parece estar consumiendo energía. Una pequeña escotilla de mantenimiento está abierta en un lateral.",
            "panel": "Un botón grande y atractivo en el panel brilla débilmente en verde. Está etiquetado como 'ACTIVACIÓN_ANTENA_COMMS'."
        },
        "on_enter_event": "main_quest_control_room_entry"
    }
}

# --- Player ---
player_inventory = []
player_stats = {
    "name": "Superviviente", # Default name in Spanish
    "max_health": 20,
    "current_health": 20,
    "strength": 5, 
    "agility": 3,
    "level": 1,
    "xp": 0,
    "xp_to_next_level": 100,
    "first_aid_skill": 1 
}
player_quests = {
    "main_comms_array": "inactive", 
    "side_librarian_glasses": "inactive",
    "tunnel_clearing_quest": "inactive" 
}
current_location = "station_entrance"

# --- Command Handlers ---
def handle_stats(args):
    """Handles the 'stats' command."""
    print(f"\n--- Estadísticas de {player_stats['name']} ---")
    print(f"Nivel: {player_stats['level']}")
    print(f"XP: {player_stats['xp']}/{player_stats['xp_to_next_level']}")
    print(f"Salud: {player_stats['current_health']}/{player_stats['max_health']}")
    print(f"Fuerza: {player_stats['strength']}")
    print(f"Agilidad: {player_stats['agility']}")
    print(f"Habilidad Primeros Auxilios: {player_stats['first_aid_skill']}")
    print("--------------------")

# --- XP and Leveling System ---
def handle_level_up_stat_increase():
    """Allows player to choose a stat to increase upon leveling up."""
    global player_stats
    print("\n¡Enhorabuena! Te sientes con más experiencia. Elige una estadística para mejorar:")
    print("  1. Vigor (+5 Salud Máx., curación completa)")
    print("  2. Destreza (+1 Fuerza)")
    print("  3. Finura (+1 Agilidad)")

    while True:
        choice = input("Introduce tu elección (1-3): ").strip()
        if choice == "1":
            player_stats["max_health"] += 5
            player_stats["current_health"] = player_stats["max_health"] 
            print(f"¡Tu salud máxima aumentó a {player_stats['max_health']}! Te sientes más resistente y estás completamente curado/a.")
            break
        elif choice == "2":
            player_stats["strength"] += 1
            print(f"¡Tu fuerza aumentó a {player_stats['strength']}! Te sientes más poderoso/a.")
            break
        elif choice == "3":
            player_stats["agility"] += 1
            print(f"¡Tu agilidad aumentó a {player_stats['agility']}! Te sientes más ágil.")
            break
        else:
            print("Elección inválida. Por favor, introduce un número entre 1 y 3.")
    handle_stats([]) 

def check_level_up():
    """Checks if the player has enough XP to level up and handles the process."""
    global player_stats
    if player_stats["xp"] >= player_stats["xp_to_next_level"]:
        player_stats["level"] += 1
        player_stats["xp"] -= player_stats["xp_to_next_level"] 
        player_stats["xp_to_next_level"] = player_stats["level"] * 100 
        
        print(f"\n*** ¡SUBISTE DE NIVEL! ¡Has alcanzado el Nivel {player_stats['level']}! ***")
        handle_level_up_stat_increase()
        check_level_up() 

def gain_xp(amount):
    """Grants XP to the player and triggers a level-up check."""
    global player_stats
    if amount <= 0:
        return
    
    print(f"\nHas ganado {amount} XP.")
    player_stats["xp"] += amount
    check_level_up()
# --- End XP and Leveling System ---

def handle_help(args):
    """Handles the 'help' command."""
    print("\n--- Comandos Disponibles ---")
    print("  look              - Describe tu ubicación actual, incluyendo objetos, NPCs y enemigos.")
    print("  look at [cosa]    - Describe un objeto específico, NPC o detalle en tu ubicación.")
    print("  go [dirección]    - Muévete en la dirección especificada (ej: 'go north').")
    print("  take [objeto]     - Recoge un objeto de tu ubicación y añádelo a tu inventario.")
    print("  inventory / inv   - Muestra los objetos que llevas actualmente.")
    print("  stats             - Muestra la salud y atributos actuales de tu personaje.")
    print(f"  attack [objetivo] - Ataca a un enemigo en tu ubicación actual (ej: 'attack {world['flooded_tunnel']['enemies'][0]['name']}')") 
    print("  fight [objetivo]  - Alias para 'attack'.")
    print(f"  talk to [npc]     - Habla con un NPC en tu ubicación actual (ej: 'talk to {world['station_entrance']['npcs']['elias']['name']}')") 
    print("  quests / journal  - Ve el estado de tus misiones actuales.")
    print(f"  use [objeto]      - Usa un objeto de tu inventario (ej: 'use {ITEM_DISPLAY_NAMES.get('first_aid_kit', 'first_aid_kit')}').") 
    print("  save              - Guarda tu progreso actual en el juego.")
    print("  load              - Carga tu partida guardada previamente.")
    print("  help              - Muestra esta lista de comandos.")
    print("  quit / exit       - Salir del juego.")
    print("--------------------")

# --- Save/Load Game Functionality ---
SAVE_FILE_NAME = "metro_savegame.json" 

def handle_save_game(args):
    """Saves the current game state to a file."""
    global player_stats, player_inventory, current_location, player_quests, world
    
    game_state = {
        "player_stats": copy.deepcopy(player_stats),
        "player_inventory": copy.deepcopy(player_inventory),
        "current_location": current_location, 
        "player_quests": copy.deepcopy(player_quests),
        "world": copy.deepcopy(world) 
    }
    
    try:
        with open(SAVE_FILE_NAME, 'w', encoding='utf-8') as f: 
            json.dump(game_state, f, indent=4, ensure_ascii=False) 
        print("Partida guardada.")
    except IOError:
        print("Error: No se pudo guardar la partida.")

def handle_load_game(args):
    """Loads the game state from a file."""
    global player_stats, player_inventory, current_location, player_quests, world
    
    try:
        with open(SAVE_FILE_NAME, 'r', encoding='utf-8') as f: 
            game_state = json.load(f)
            
            player_stats = game_state["player_stats"]
            player_inventory = game_state["player_inventory"]
            current_location = game_state["current_location"]
            player_quests = game_state["player_quests"]
            world = game_state["world"] 
            
            print("\nPartida cargada.")
            handle_look([]) 
    except FileNotFoundError:
        print("No se encontró ninguna partida guardada.")
    except IOError:
        print("Error: No se pudo cargar la partida.")
    except json.JSONDecodeError:
        print("Error: El archivo de guardado está corrupto.")


# --- Item Usage Handler ---
def handle_use_item(args):
    """Handles the 'use [item]' command."""
    global player_stats
    global player_inventory

    if not args:
        print(f"¿Usar qué? (ej: 'use {ITEM_DISPLAY_NAMES.get('first_aid_kit', 'first_aid_kit')}')") 
        return

    item_to_use_input = " ".join(args).lower() 
    
    item_internal_key = None
    for key, display_name in ITEM_DISPLAY_NAMES.items():
        if item_to_use_input == display_name.lower():
            item_internal_key = key
            break
    if not item_internal_key: 
        item_internal_key = item_to_use_input

    if item_internal_key not in player_inventory: 
        print(f"No tienes {item_to_use_input} en tu inventario.") 
        return

    if item_internal_key == "first_aid_kit": 
        if player_stats["current_health"] >= player_stats["max_health"]:
            print(f"Ya estás con la salud al máximo. No necesitas usar un {ITEM_DISPLAY_NAMES.get('first_aid_kit', 'botiquín')}.")
            return

        base_heal = 15
        skill_bonus = player_stats.get("first_aid_skill", 1) * 5 
        total_heal = base_heal + skill_bonus
        
        healed_amount = 0
        if player_stats["current_health"] + total_heal > player_stats["max_health"]:
            healed_amount = player_stats["max_health"] - player_stats["current_health"]
            player_stats["current_health"] = player_stats["max_health"]
        else:
            healed_amount = total_heal
            player_stats["current_health"] += total_heal
            
        player_inventory.remove("first_aid_kit") 
        print(f"Has usado un {ITEM_DISPLAY_NAMES.get('first_aid_kit', 'botiquín')} y te has curado {healed_amount} PS.") 
        print(f"Tu salud actual es {player_stats['current_health']}/{player_stats['max_health']}.")
    
    
    elif item_internal_key == "bandage": 
        if player_stats["current_health"] >= player_stats["max_health"]:
            print(f"Ya estás con la salud al máximo. No necesitas usar una {ITEM_DISPLAY_NAMES.get('bandage', 'venda')}.")
            return
        
        heal_amount = 10 
        
        actual_healed = 0
        if player_stats["current_health"] + heal_amount > player_stats["max_health"]:
            actual_healed = player_stats["max_health"] - player_stats["current_health"]
            player_stats["current_health"] = player_stats["max_health"]
        else:
            actual_healed = heal_amount
            player_stats["current_health"] += heal_amount
            
        player_inventory.remove("bandage")
        print(f"Te aplicas una {ITEM_DISPLAY_NAMES.get('bandage', 'venda')} y te curas {actual_healed} PS.") 
        print(f"Tu salud actual es {player_stats['current_health']}/{player_stats['max_health']}.")

    else:
        print(f"No puedes usar {item_to_use_input} de esa manera (o no es utilizable).")


def handle_quests(args):
    """Handles the 'quests' or 'journal' command."""
    global player_quests
    print("\n--- Tus Misiones ---") 
    active_quests_found = False
    completed_quests_found = False

    main_quest_title = "La Señal"
    if player_quests.get("main_comms_array") == "active":
        print(f"- (Activa) {main_quest_title}: Alcanza la Sala de Control para investigar la vieja antena de comunicaciones. Elías mencionó que es accesible por la Sala de Máquinas.")
        active_quests_found = True
    elif player_quests.get("main_comms_array") == "completed":
        print(f"- (Completada) {main_quest_title}: Llegaste a la Sala de Control y activaste el panel de la antena de comunicaciones.")
        completed_quests_found = True
    
    side_quest_1_title = "Objetos Perdidos"
    if player_quests.get("side_librarian_glasses") == "active":
        print(f"- (Activa) {side_quest_1_title}: Encuentra las {ITEM_DISPLAY_NAMES.get('antique_glasses', 'gafas antiguas')} de la Bibliotecaria Agnes. Cree que están en la Cochera Abandonada.")
        active_quests_found = True
    elif player_quests.get("side_librarian_glasses") == "completed":
        print(f"- (Completada) {side_quest_1_title}: Devolviste las {ITEM_DISPLAY_NAMES.get('antique_glasses', 'gafas antiguas')} a la Bibliotecaria Agnes y recibiste un {ITEM_DISPLAY_NAMES.get('valuable_book', 'libro valioso')}.")
        completed_quests_found = True

    side_quest_2_title = "Limpieza de Túnel"
    tunnel_quest_data = player_quests.get("tunnel_clearing_quest")
    if isinstance(tunnel_quest_data, dict): 
        defeated = tunnel_quest_data.get('humans_defeated', 0)
        required = tunnel_quest_data.get('humans_required', 2)
        if tunnel_quest_data.get('status') == "active":
            print(f"- (Activa) {side_quest_2_title}: Derrota a los Humanos Salvajes en la Cochera Abandonada para el Capitán Dimitri. ({defeated}/{required} derrotados)")
            active_quests_found = True
        elif tunnel_quest_data.get('status') == "completed":
            print(f"- (Completada) {side_quest_2_title}: Eliminaste a los Humanos Salvajes para el Capitán Dimitri.")
            completed_quests_found = True
    elif tunnel_quest_data == "inactive": 
        pass


    if not active_quests_found and not completed_quests_found:
        has_inactive_quests = False
        if player_quests.get("main_comms_array") == "inactive": has_inactive_quests = True
        if player_quests.get("side_librarian_glasses") == "inactive": has_inactive_quests = True
        tunnel_quest_status = player_quests.get("tunnel_clearing_quest") 
        if isinstance(tunnel_quest_status, str) and tunnel_quest_status == "inactive": 
            has_inactive_quests = True
        elif isinstance(tunnel_quest_status, dict) and tunnel_quest_status.get("status") == "inactive": 
             has_inactive_quests = True 
        
        if has_inactive_quests:
             print("Tienes misiones potenciales disponibles. Intenta hablar con la gente en las estaciones.")
        else: 
            print("No tienes misiones activas o completadas en este momento.")
    elif not active_quests_found and completed_quests_found:
        print("No tienes misiones activas, solo completadas.")
    elif active_quests_found and not completed_quests_found:
        pass 
    print("--------------------")

def handle_look(args):
    """Handles the 'look' command."""
    global current_location
    global player_quests
    location_data = world.get(current_location)
    if not location_data:
        print("Error: ¡Ubicación desconocida!") 
        return

    print(location_data["description"]) 

    if location_data.get("npcs"):
        for npc_id, npc_data_val in location_data["npcs"].items():
            if isinstance(npc_data_val, dict): 
                npc_name_display = npc_data_val.get("name", npc_id.capitalize())
                base_desc = npc_data_val.get("description", f"Ves a {npc_name_display}.") 
                
                quest_hint = ""
                npc_quest_id = npc_data_val.get("quest_id")
                dialogues = npc_data_val.get("dialogue", {})
                has_offer_dialogue = any(key.startswith("offer_") for key in dialogues)

                actual_quest_status = player_quests.get(npc_quest_id)
                is_inactive = False
                if isinstance(actual_quest_status, dict):
                    is_inactive = actual_quest_status.get("status") == "inactive"
                else:
                    is_inactive = actual_quest_status == "inactive"

                if npc_quest_id and is_inactive and has_offer_dialogue:
                    quest_hint = f" {npc_name_display} parece querer hablar. (Intenta 'talk to {npc_id}')"
                print(base_desc + quest_hint)
            else: 
                print(f"Ves a {npc_id.capitalize()}. {npc_data_val}") 

    if location_data.get("enemies"):
        print("Enemigos presentes:") 
        for enemy in location_data["enemies"]:
            enemy_name = enemy.get('name', 'Enemigo Desconocido') 
            enemy_health = enemy.get('health', 'N/A')
            print(f"- {enemy_name} (Salud: {enemy_health})")

    if location_data.get("items"):
        display_items = [ITEM_DISPLAY_NAMES.get(item_key, item_key) for item_key in location_data["items"]]
        print("Objetos aquí: " + ", ".join(display_items)) 
    else:
        print("No ves objetos aquí.") 

    available_exits = ", ".join(location_data["exits"].keys())
    if available_exits:
        print(f"Salidas: {available_exits}") 
    else:
        print("No hay salidas obvias.") 

    if len(args) > 0 and args[0] == "at": 
        if len(args) > 1:
            detail_name_input = " ".join(args[1:]).lower() 

            found_detail = False
            if "details" in location_data and detail_name_input in location_data["details"]:
                print(location_data["details"][detail_name_input])
                found_detail = True
            
            if not found_detail and "npcs" in location_data:
                for npc_id, npc_data_val in location_data["npcs"].items():
                    if isinstance(npc_data_val, dict) and \
                       (detail_name_input == npc_id.lower() or detail_name_input == npc_data_val.get("name","").lower()):
                        npc_name_display = npc_data_val.get("name", detail_name_input.capitalize())
                        desc = npc_data_val.get("description", f"Ves a {npc_name_display}.")
                        quest_hint = ""
                        npc_quest_id = npc_data_val.get("quest_id")
                        if npc_quest_id: 
                            quest_status_obj = player_quests.get(npc_quest_id)
                            actual_status = ""
                            if isinstance(quest_status_obj, dict): actual_status = quest_status_obj.get("status")
                            else: actual_status = quest_status_obj

                            if actual_status == "inactive":
                                quest_hint = f" Parece querer discutir algo. (Intenta 'talk to {npc_id}')" 
                            elif actual_status == "active":
                                quest_hint = f" Tienes una tarea pendiente para él/ella."
                            elif actual_status == "completed":
                                quest_hint = f" Ya le has ayudado con su tarea."
                        print(desc + quest_hint)
                        found_detail = True
                        break
                if found_detail: return 
            
            if not found_detail and "items" in location_data: 
                for item_key in location_data.get("items", []):
                    if detail_name_input == item_key.lower() or \
                       detail_name_input == ITEM_DISPLAY_NAMES.get(item_key, "").lower():
                        print(f"Es un(a) {ITEM_DISPLAY_NAMES.get(item_key, item_key)}.")
                        found_detail = True
                        break
                if found_detail: return 
            
            if not found_detail and "enemies" in location_data: 
                for enemy_obj in location_data["enemies"]:
                    if detail_name_input == enemy_obj["name"].lower(): 
                        print(enemy_obj.get("description", f"Un {enemy_obj['name']} de aspecto amenazante."))
                        found_detail = True
                        break
                if found_detail: return 
            
            if not found_detail: 
                print(f"No ves ningún detalle específico sobre '{detail_name_input}' aquí.")
        else:
            print("¿Mirar qué?") 


def handle_talk(args):
    """Handles the 'talk to [npc]' command."""
    global current_location
    global player_quests
    global player_inventory 

    if not args:
        print("¿Hablar con quién?") 
        return

    npc_target_name_input = " ".join(args).lower() 
    location_data = world.get(current_location)

    if not location_data.get("npcs"):
        print("No hay nadie con quien hablar aquí.") 
        return

    found_npc_id = None
    npc_data_to_use = None 

    for current_npc_id, current_npc_data_val in location_data["npcs"].items():
        if isinstance(current_npc_data_val, dict):
            if npc_target_name_input == current_npc_id.lower() or \
               npc_target_name_input == current_npc_data_val.get("name","").lower():
                found_npc_id = current_npc_id
                npc_data_to_use = current_npc_data_val
                break
            elif npc_target_name_input in current_npc_data_val.get("name","").lower(): 
                found_npc_id = current_npc_id
                npc_data_to_use = current_npc_data_val
    
    if not npc_data_to_use:
        print(f"No ves a nadie llamado '{npc_target_name_input}' aquí para hablar.")
        return


    npc_display_name = npc_data_to_use.get("name", found_npc_id.capitalize())
    dialogue = npc_data_to_use.get("dialogue", {})
    quest_id = npc_data_to_use.get("quest_id")
    
    print(f"\nTe acercas a {npc_display_name}.") 

    if quest_id: 
        quest_status_obj = player_quests.get(quest_id) 
        current_quest_status_val = ""
        if isinstance(quest_status_obj, dict):
            current_quest_status_val = quest_status_obj.get("status", "unavailable")
        else:
            current_quest_status_val = quest_status_obj if quest_status_obj else "unavailable"


        if current_quest_status_val == "inactive":
            offer_dialogue_key = None
            for key in dialogue:
                if key.startswith("offer_"): offer_dialogue_key = key; break 
            
            if offer_dialogue_key:
                print(f"{npc_display_name}: \"{dialogue[offer_dialogue_key]}\"")
                accept_input = input(f"¿Ayudar a {npc_display_name}? (si/no): ").strip().lower() 
                if accept_input in ["yes", "y", "si", "sí"]: 
                    if quest_id == "tunnel_clearing_quest":
                        player_quests[quest_id] = {'status': 'active', 'humans_defeated': 0, 'humans_required': 2}
                    else:
                        player_quests[quest_id] = "active"
                    print(f"{npc_display_name}: \"{dialogue.get('quest_accepted', '¡Gracias! Se agradece tu ayuda.')}\"")
                else:
                    print(f"{npc_display_name}: \"{dialogue.get('quest_declined', 'Oh, de acuerdo entonces. Avísame si cambias de opinión.')}\"")
            else: 
                 print(f"{npc_display_name}: \"{dialogue.get('greeting', 'Te mira pero dice poco.')}\"")
        
        elif current_quest_status_val == "active":
            if quest_id == "side_librarian_glasses" and npc_data_to_use.get("quest_item_needed"):
                item_needed_key = npc_data_to_use["quest_item_needed"] 
                if item_needed_key in player_inventory:
                    print(f"{npc_display_name}: \"{dialogue.get('completion', '¡Las encontraste! ¡Increíble!')}\"")
                    player_inventory.remove(item_needed_key)
                    print(f"(Le entregas el objeto: {ITEM_DISPLAY_NAMES.get(item_needed_key, item_needed_key)}.)") 
                    reward_key = npc_data_to_use.get("reward_item")
                    if reward_key: player_inventory.append(reward_key); print(f"Recibiste un {ITEM_DISPLAY_NAMES.get(reward_key, reward_key)} como recompensa.") 
                    player_quests[quest_id] = "completed" 
                    quest_xp_reward = npc_data_to_use.get("xp_reward", 0)
                    if quest_xp_reward > 0: gain_xp(quest_xp_reward)
                else:
                    print(f"{npc_display_name}: \"{dialogue.get('quest_item_not_found', '¿Sigues buscándolas?')}\"")
            
            elif quest_id == "tunnel_clearing_quest":
                current_quest_data_dict = player_quests.get(quest_id, {}) 
                defeated = current_quest_data_dict.get('humans_defeated', 0)
                required = current_quest_data_dict.get('humans_required', 2)
                
                if defeated >= required: 
                    print(f"{npc_display_name}: \"{dialogue.get('completion', '¡Excelente trabajo eliminándolos!')}\"")
                    
                    reward_item_key = npc_data_to_use.get("reward_item")
                    if reward_item_key: 
                        player_inventory.append(reward_item_key)
                        print(f"Recibiste {ITEM_DISPLAY_NAMES.get(reward_item_key, reward_item_key)}.") 
                    
                    quest_xp = npc_data_to_use.get("xp_reward", 0)
                    if quest_xp > 0: gain_xp(quest_xp)
                    
                    current_quest_data_dict['status'] = "completed" 
                else: 
                    remaining = required - defeated
                    reminder_text = dialogue.get('quest_reminder_incomplete', "Aún queda trabajo por hacer.").format(remaining=remaining, defeated=defeated, required=required) 
                    print(f"{npc_display_name}: \"{reminder_text}\"")

            elif quest_id == "main_comms_array":
                 print(f"{npc_display_name}: \"{dialogue.get('quest_reminder', '¿Algún progreso en llegar a la Sala de Control?')}\"")
            else: 
                print(f"{npc_display_name}: \"{dialogue.get('quest_reminder', '¿Cómo va esa tarea?')}\"")
        
        elif current_quest_status_val == "completed":
            print(f"{npc_display_name}: \"{dialogue.get('quest_completed_already', '¡Gracias de nuevo por tu ayuda!')}\"")
        
        else: 
            print(f"{npc_display_name}: \"{dialogue.get('default', 'No hay nada más que decir por ahora.')}\"")
    else: 
        print(f"{npc_display_name}: \"{dialogue.get('greeting', dialogue.get('default', 'Te saluda con un asentimiento.'))}\"")


def handle_go(args):
    """Handles the 'go' command."""
    global current_location
    global player_quests 
    if not args:
        print("¿Ir adónde?") 
        return

    direction = args[0].lower()
    current_room_data = world.get(current_location) 

    if current_room_data and direction in current_room_data["exits"]:
        next_location_id = current_room_data["exits"][direction]
        if next_location_id in world:
            current_location = next_location_id
            print(f"\nVas hacia {direction}...") 
            
            new_location_data = world.get(current_location) 
            if new_location_data and new_location_data.get("on_enter_event") == "main_quest_control_room_entry":
                if player_quests.get("main_comms_array") == "active":
                    print("\n[MISIÓN COMPLETADA] Al entrar en la Sala de Control, un panel en la terminal principal parpadea con una suave luz verde. ¡Has activado con éxito el panel de la antena de comunicaciones!")
                    print("Elías se alegrará de saber que los sistemas centrales de la estación vuelven a responder.")
                    player_quests["main_comms_array"] = "completed"
                    gain_xp(150) 
            
            handle_look([]) 
        else:
            print(f"Error: El camino {direction} lleva a un lugar desconocido.") 
    else:
        print(f"No puedes ir hacia {direction}.") 


def handle_attack(args):
    """Handles the 'attack' command."""
    global current_location
    global player_stats

    location_data = world.get(current_location)
    if not location_data or not location_data.get("enemies"):
        print("No hay nada que atacar aquí.") 
        return

    if not args:
        if location_data.get("enemies"):
            first_enemy_name = location_data["enemies"][0].get("name", "enemigo")
            example_target = first_enemy_name.split()[0] if first_enemy_name else "enemigo"
            print(f"¿Atacar a qué? (ej: 'attack {example_target}')")
        else:
            print("¿Atacar a qué?")
        return

    target_name_input = " ".join(args).lower() 
    target_enemy = None
    enemy_index = -1

    for i, enemy_data in enumerate(location_data["enemies"]):
        if target_name_input in enemy_data["name"].lower(): 
            target_enemy = enemy_data
            enemy_index = i
            break
    
    if not target_enemy:
        print(f"No ves ningún '{target_name_input}' para atacar aquí.") 
        return

    enemy_name_display = target_enemy.get("name", "Enemigo Misterioso") 
    print(f"\n--- Combate con {enemy_name_display} ---")

    player_damage = player_stats["strength"] 
    target_enemy["health"] -= player_damage
    print(f"Golpeas a {enemy_name_display} y le haces {player_damage} de daño.") 

    if target_enemy["health"] <= 0:
        print(f"¡Has derrotado a {enemy_name_display}!") 
        
        if "humano salvaje" in enemy_name_display.lower(): 
            tunnel_quest = player_quests.get("tunnel_clearing_quest")
            if isinstance(tunnel_quest, dict) and tunnel_quest.get("status") == "active":
                tunnel_quest["humans_defeated"] = tunnel_quest.get("humans_defeated", 0) + 1
                print(f"[Actualización Misión] Humanos Salvajes derrotados: {tunnel_quest['humans_defeated']}/{tunnel_quest['humans_required']}")

        possible_loot = target_enemy.get("loot")
        if possible_loot:
            dropped_item_key = None
            if isinstance(possible_loot, list) and possible_loot: 
                dropped_item_key = random.choice(possible_loot)
            elif isinstance(possible_loot, str): 
                dropped_item_key = possible_loot
            
            if dropped_item_key:
                if "items" not in location_data: 
                    location_data["items"] = []
                location_data["items"].append(dropped_item_key) 
                dropped_item_display = ITEM_DISPLAY_NAMES.get(dropped_item_key, dropped_item_key)
                print(f"{enemy_name_display} dejó caer un(a) {dropped_item_display}.") 
        
        location_data["enemies"].pop(enemy_index) 
        
        if not location_data["enemies"]: 
            del location_data["enemies"] 
        
        xp_from_enemy = target_enemy.get("xp_value", 0)
        if xp_from_enemy > 0:
            gain_xp(xp_from_enemy)
            
        return 

    enemy_damage = target_enemy["attack_power"]
    player_stats["current_health"] -= enemy_damage
    print(f"{enemy_name_display} contraataca, haciéndote {enemy_damage} de daño.") 

    if player_stats["current_health"] <= 0:
        player_stats["current_health"] = 0 
        print(f"Tu salud es {player_stats['current_health']}/{player_stats['max_health']}.")
        print("\nHas sucumbido a tus heridas. Tu aventura termina aquí.") 
        print("Fin del Juego.") 
    else:
        print(f"Tu salud es {player_stats['current_health']}/{player_stats['max_health']}.")
    print("--------------------")


def handle_take(args):
    """Handles the 'take' command."""
    global current_location
    global player_inventory
    if not args:
        print("¿Tomar qué?") 
        return

    item_name_input = " ".join(args).lower() 
    location_data = world.get(current_location)
    
    found_item_key = None
    if location_data and location_data.get("items"):
        for item_key in location_data["items"]:
            if item_name_input == item_key.lower() or \
               item_name_input == ITEM_DISPLAY_NAMES.get(item_key, "").lower():
                found_item_key = item_key
                break
    
    if found_item_key:
        player_inventory.append(found_item_key) 
        location_data["items"].remove(found_item_key)
        print(f"Tomas el/la {ITEM_DISPLAY_NAMES.get(found_item_key, found_item_key)}.") 
    else:
        print(f"No ves un(a) {item_name_input} aquí.") 

def handle_inventory(args):
    """Handles the 'inventory' command."""
    global player_inventory
    if player_inventory:
        display_inventory = [ITEM_DISPLAY_NAMES.get(item_key, item_key) for item_key in player_inventory]
        print("Llevas contigo: " + ", ".join(display_inventory)) 
    else:
        print("Tu inventario está vacío.") 

def handle_quit(args):
    """Handles the 'quit' command."""
    print("¡Gracias por jugar!") 
    exit()

# --- Placeholder Functions ---
def new_game_placeholder():
    """Displays a placeholder message for the 'New Game' option."""
    messagebox.showinfo("New Game", "New Game - Not Implemented Yet")

# --- Main Application Class ---
class MainApplication(tk.Tk):
    """Main application window for the Metro Game and Editor."""
    def __init__(self):
        """Initializes the main application window and its menu."""
        super().__init__()
        self.title("Map Editor and Game")
        self.geometry("800x600")

        menubar = Menu(self)
        self.config(menu=menubar)

        main_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=main_menu)

        main_menu.add_command(label="New Game", command=new_game_placeholder)
        main_menu.add_command(label="Editor", command=self.open_editor_window)
        main_menu.add_separator()
        main_menu.add_command(label="Exit", command=self.quit)

        self.editor_window = None # Attribute to hold the editor window instance

    def open_editor_window(self):
        """Opens the Province Editor window. Creates a new instance if one doesn't exist
        or brings the existing one to the front."""
        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = EditorWindow(self) # Pass self as parent
            self.editor_window.focus_set() 
        else:
            self.editor_window.focus_set() 

# --- EditorWindow Class ---
class EditorWindow(tk.Toplevel):
    """Editor window for creating and managing map provinces."""
    def __init__(self, parent):
        """Initializes the Editor window, its widgets, and variables."""
        super().__init__(parent)
        self.title("Province Editor")
        self.geometry("1000x750") 

        # Image display attributes
        self.image_on_canvas = None # ID of the image object on the canvas
        self.photo_image = None   # PhotoImage object (to prevent garbage-collection)
        
        # Point and province data storage
        self.drawn_points_visuals = []    # Stores IDs of ovals drawn for current points
        self.current_province_points = [] # Stores (x,y) tuples for the province currently being defined
        self.provinces_visuals = []       # Stores IDs of province polygons drawn on the canvas
        self.provinces_data = []          # Stores lists of (x,y) tuples, each list defining a province

        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Reference Image", command=self.load_reference_image)
        file_menu.add_separator()
        file_menu.add_command(label="Close Editor", command=self.destroy)

        # Frame for Canvas to allow button placement below
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(pady=5, padx=10, expand=True, fill=tk.BOTH)

        self.map_canvas = tk.Canvas(canvas_frame, bg="lightgrey") # Removed fixed size to allow expand
        self.map_canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        
        self.map_canvas.bind("<Button-1>", self.place_point_on_canvas)

        # Button to create province
        self.create_province_button = tk.Button(self, text="Create Province", command=self.create_province)
        self.create_province_button.pack(pady=5, side=tk.BOTTOM) # Explicitly pack at bottom

    def load_reference_image(self):
        """Opens a file dialog to load a reference image onto the canvas."""
        try:
            # Ensure Pillow is available (this check is also at top-level import)
            from PIL import Image, ImageTk
        except ImportError:
            messagebox.showerror("Error", "Pillow library is not installed or couldn't be loaded. Please install it to use image features (e.g., pip install Pillow).", parent=self)
            return

        file_path = filedialog.askopenfilename(
            parent=self,
            title="Select a Reference Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")]
        )

        if not file_path: # User cancelled
            return

        try:
            # Open the image using Pillow
            image = Image.open(file_path)

            # Convert the Pillow image to a Tkinter PhotoImage
            self.photo_image = ImageTk.PhotoImage(image)

            # Clear previous image if any
            if self.image_on_canvas:
                self.map_canvas.delete(self.image_on_canvas)

            # Display the image on the canvas
            # Place image at top-left corner (0,0) with anchor 'nw' (north-west)
            self.image_on_canvas = self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            
            # When new image loaded, clear all previously drawn provinces and points
            self.clear_all_provinces_and_points()
            
            # Optional: Configure canvas scrollregion if image is larger than canvas
            # self.map_canvas.config(scrollregion=self.map_canvas.bbox(tk.ALL))
            
            # Optional: Resize canvas to fit image (can be complex if image is very large)
            # self.map_canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
            # self.map_canvas.pack_propagate(False) # Prevent canvas from shrinking to original pack size

            print(f"Loaded image: {file_path}")

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Error Loading Image", f"An error occurred: {e}", parent=self)
            print(f"Error loading image: {e}")

    def place_point_on_canvas(self, event):
        """Places a point on the canvas at the clicked coordinates (event.x, event.y)."""
        x, y = event.x, event.y
        self.current_province_points.append((x, y))
        
        # Draw a visual representation of the point (small red circle)
        radius = 4 
        # The tag "point_marker" can be used to manage these visuals if needed later
        point_visual_id = self.map_canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, 
            fill="red", outline="red", tags="point_marker"
        )
        self.drawn_points_visuals.append(point_visual_id)
        
        print(f"Point placed at: ({x}, {y}). Current points for province: {self.current_province_points}")

    def create_province(self):
        """Creates a province polygon from the currently placed points."""
        if len(self.current_province_points) < 3:
            messagebox.showwarning(
                "Create Province", 
                "You need at least 3 points to create a province.", 
                parent=self
            )
            return

        # Create the polygon on the canvas
        # Style options:
        # - outline: Color of the border
        # - fill: Fill color of the polygon
        # - width: Border width in pixels
        # - stipple: Pattern for the fill (e.g., "gray50", "gray25") for pseudo-transparency
        # - tags: Allows grouping and managing canvas items
        polygon_id = self.map_canvas.create_polygon(
            self.current_province_points,
            outline="blue",        
            fill="blue",           
            width=2,               
            stipple="gray25",      
            tags="province_polygon" 
        )
        self.provinces_visuals.append(polygon_id) # Store the visual ID
        
        # Store the coordinate data for this province (make a copy)
        self.provinces_data.append(list(self.current_province_points))

        print(f"Province created with {len(self.current_province_points)} points: {self.current_province_points}")

        # Clear current points (visuals and data) to ready for a new province
        self.clear_current_points()

    def clear_current_points(self):
        """Clears the points that are currently being placed (not yet a full province)."""
        for visual_id in self.drawn_points_visuals:
            self.map_canvas.delete(visual_id)
        self.drawn_points_visuals.clear()
        self.current_province_points.clear()
        print("Current (active) points cleared from canvas and memory.")

    def clear_all_provinces_and_points(self):
        """Clears all drawn provinces and any currently active points."""
        self.clear_current_points() # Clear any active, unformed points first
        
        for province_visual_id in self.provinces_visuals:
            self.map_canvas.delete(province_visual_id)
        self.provinces_visuals.clear()
        self.provinces_data.clear()
        print("All provinces and active points cleared from canvas and data.")
        
    # Add other editor methods here later (e.g., saving/loading provinces, editing existing ones)

# --- Command Parser ---
command_handlers = {
    "look": handle_look,
    "go": handle_go,
    "take": handle_take,
    "inventory": handle_inventory,
    "inv": handle_inventory,
    "quit": handle_quit,
    "exit": handle_quit,
    "help": handle_help,
    "stats": handle_stats,
    "attack": handle_attack,
    "fight": handle_attack, 
    "talk": handle_talk, 
    "quests": handle_quests,
    "journal": handle_quests,
    "use": handle_use_item,
    "save": handle_save_game,
    "load": handle_load_game,
}

# --- Main Game Loop ---
if __name__ == "__main__":
    # print("Bienvenido al Metro. Escribe 'help' para ver los comandos.")
    # handle_look([]) 

    # while True:
    #     try:
    #         user_input = input("> ").strip().lower()
    #         if not user_input:
    #             continue

    #         parts = user_input.split()
    #         command = parts[0]
    #         args = parts[1:]

    #         if command in command_handlers:
    #             command_handlers[command](args)
    #             if player_stats["current_health"] <= 0: # Check for game over after command
    #                 break
    #         else:
    #             print("Comando desconocido. Escribe 'help' para ver la lista de comandos.")
    #     except EOFError: # Handle Ctrl+D or end of input stream
    #         print("\nSaliendo del juego...")
    #         break
    #     except KeyboardInterrupt: # Handle Ctrl+C
    #         print("\nInterrupción del teclado. Saliendo del juego...")
    #         break
    #     except Exception as e: # Catch any other unexpected errors
    #         print(f"Ha ocurrido un error inesperado: {e}")
    #         print("Intentando guardar el progreso...")
    #         handle_save_game([]) # Attempt to save before potential crash
    #         break 
    app = MainApplication()
    app.mainloop()
