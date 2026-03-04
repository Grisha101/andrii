import tkinter as tk
from tkinter import messagebox
import random

class HorrorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("The Haunted Mansion")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Game state
        self.health = 100
        self.sanity = 100
        self.inventory = []
        self.current_room = "entrance"
        self.visited_rooms = set()
        
        # Room descriptions
        self.rooms = {
            "entrance": {
                "description": "You stand at the entrance of an old, decrepit mansion.\nThe door creaks in the wind. Moonlight illuminates the skeletal trees.\nWhere do you go?",
                "choices": [
                    {"text": "Enter the mansion", "next": "hallway", "sanity": -10},
                    {"text": "Run away (Game Over)", "next": "ending_coward", "sanity": 5}
                ]
            },
            "hallway": {
                "description": "You're in a dark hallway. Portraits on the walls seem to follow you with their eyes.\nYou hear faint whispers echoing from different directions.\nA chandelier hangs precariously above.",
                "choices": [
                    {"text": "Go to the library (left)", "next": "library", "sanity": -15},
                    {"text": "Go to the kitchen (right)", "next": "kitchen", "sanity": -20},
                    {"text": "Go upstairs", "next": "bedroom", "sanity": -25},
                    {"text": "Go back outside", "next": "entrance", "sanity": 10}
                ]
            },
            "library": {
                "description": "Dusty bookshelves stretch to the ceiling. You find a leather journal with strange symbols.\nPages are stained with what looks like blood.\nYour flashlight flickers ominously.",
                "choices": [
                    {"text": "Take the journal (gain item)", "next": "hallway", "sanity": -20, "item": "journal"},
                    {"text": "Ignore it and leave", "next": "hallway", "sanity": -5},
                    {"text": "Read the journal deeper", "next": "library_deep", "sanity": -40}
                ]
            },
            "library_deep": {
                "description": "The journal reveals terrifying rituals performed in this house.\nYou read about the previous owner... a dark cultist.\nSuddenly, you hear footsteps above you. Something is moving upstairs.",
                "choices": [
                    {"text": "Hide behind the bookshelf", "next": "library_hide", "sanity": -15},
                    {"text": "Confront the sound", "next": "entity_encounter", "sanity": -50}
                ]
            },
            "library_hide": {
                "description": "You crouch behind a dusty bookshelf. The footsteps pass by your hiding spot.\nYou glimpse a shadow - human-shaped but moving unnaturally.\nIt disappears into the wall.",
                "choices": [
                    {"text": "Wait for silence", "next": "hallway", "sanity": -10},
                    {"text": "Follow the entity", "next": "entity_encounter", "sanity": -40}
                ]
            },
            "kitchen": {
                "description": "The kitchen is frozen in time. Dirty dishes still sit on the table.\nA strong smell of rot emanates from the locked cellar door.\nYou find a rusty key on the counter.",
                "choices": [
                    {"text": "Take the key (gain item)", "next": "hallway", "sanity": -10, "item": "rusty_key"},
                    {"text": "Try to open the cellar door", "next": "cellar", "sanity": -30},
                    {"text": "Leave immediately", "next": "hallway", "sanity": -5}
                ]
            },
            "cellar": {
                "description": "The cellar is a nightmare.\nMutilated furniture, candles arranged in occult patterns, bones scattered on the floor.\nA voice whispers your name from the darkness.",
                "choices": [
                    {"text": "Run upstairs", "next": "hallway", "sanity": -35},
                    {"text": "Investigate the symbols", "next": "ritual_room", "sanity": -50}
                ]
            },
            "ritual_room": {
                "description": "You reveal the ritual room. Ancient symbols glow with an eerie light.\nIn the center stands a stone altar with fresh flowers - and fresh bloodstains.\nSomething ancient awakens in response to your presence.",
                "choices": [
                    {"text": "Flee for your life", "next": "ending_escape", "sanity": -40},
                    {"text": "Try to break the spell", "next": "entity_encounter", "sanity": -50}
                ]
            },
            "bedroom": {
                "description": "A master bedroom with a four-poster bed.\nOn the nightstand, a medication bottle for 'extreme paranoia'.\nThe mirror shows your reflection... but it moves a second too late.",
                "choices": [
                    {"text": "Check the mirror closely", "next": "mirror_encounter", "sanity": -45},
                    {"text": "Search the drawers", "next": "bedroom_search", "sanity": -15},
                    {"text": "Leave immediately", "next": "hallway", "sanity": -10}
                ]
            },
            "mirror_encounter": {
                "description": "Your reflection smiles while your face remains expressionless.\nIt begins to exit the mirror.\nYou feel a cold touch on your shoulder.",
                "choices": [
                    {"text": "Shatter the mirror", "next": "ending_escape", "sanity": -40},
                    {"text": "Accept your fate", "next": "ending_possessed", "sanity": -100}
                ]
            },
            "bedroom_search": {
                "description": "You find a diary. The owner was slowly going insane.\nLast entry: 'It's inside me now. I can't stop it.'\nYou hear a disturbing sound coming from inside your own throat.",
                "choices": [
                    {"text": "Leave quickly", "next": "hallway", "sanity": -25},
                    {"text": "Continue reading", "next": "entity_encounter", "sanity": -50}
                ]
            },
            "entity_encounter": {
                "description": "You come face to face with IT.\nA humanoid shadow with too many limbs and a mouth that opens too wide.\nIt whispers forbidden knowledge directly into your mind.",
                "choices": [
                    {"text": "Fight back (use journal)", "next": "ending_victory" if "journal" in self.inventory else "ending_death", "sanity": -50},
                    {"text": "Accept darkness", "next": "ending_possessed", "sanity": -100}
                ]
            },
            "ending_coward": {
                "description": "You run away and never look back.\nBut you know what you saw. The nightmares never stop.\nYou check locks three times every night.\n\n[ENDING: COWARD'S PATH - TRUE HORROR IS UNCERTAINTY]",
                "choices": [
                    {"text": "Play Again", "next": "entrance", "sanity": 100}
                ]
            },
            "ending_escape": {
                "description": "You burst through the mansion doors just as the sun rises.\nBehind you, the building seems to sink deeper into the earth.\nYou're alive... but haunted.\n\n[ENDING: NARROW ESCAPE - SURVIVAL AT WHAT COST?]",
                "choices": [
                    {"text": "Play Again", "next": "entrance", "sanity": 100}
                ]
            },
            "ending_death": {
                "description": "The entity's touch is ice cold.\nYour vision fades to black.\nYou never leave the mansion.\n\n[ENDING: CONSUMED BY DARKNESS]",
                "choices": [
                    {"text": "Play Again", "next": "entrance", "sanity": 100}
                ]
            },
            "ending_possessed": {
                "description": "You feel yourself slipping away.\nThe entity is now in control.\nYou are a passenger in your own body.\n\n[ENDING: THE HOUSE HAS A NEW MASTER]",
                "choices": [
                    {"text": "Play Again", "next": "entrance", "sanity": 100}
                ]
            },
            "ending_victory": {
                "description": "You read the binding incantation from the journal.\nThe entity shrieks and dissolves into shadows.\nThe mansion crumbles around you as you escape.\n\n[ENDING: VICTORY - BUT AT WHAT COST TO YOUR SANITY?]",
                "choices": [
                    {"text": "Play Again", "next": "entrance", "sanity": 100}
                ]
            }
        }
        
        # UI Setup
        self.setup_ui()
        self.load_room("entrance")
        
    def setup_ui(self):
        # Top panel - Stats
        top_frame = tk.Frame(self.root, bg="#2a2a2a", height=80)
        top_frame.pack(fill=tk.X)
        
        stats_label = tk.Label(
            top_frame, 
            text="", 
            fg="#00ff00", 
            bg="#2a2a2a", 
            font=("Arial", 10),
            justify=tk.LEFT
        )
        stats_label.pack(pady=10)
        self.stats_label = stats_label
        
        # Middle panel - Story
        self.story_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.story_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.story_text = tk.Text(
            self.story_frame,
            height=15,
            width=80,
            bg="#0a0a0a",
            fg="#ffff00",
            font=("Arial", 11),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.story_text.pack(fill=tk.BOTH, expand=True)
        
        # Bottom panel - Buttons
        self.button_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        
    def load_room(self, room_name):
        if room_name == "entrance":
            self.health = 100
            self.sanity = 100
            self.inventory = []
        
        self.current_room = room_name
        self.visited_rooms.add(room_name)
        
        room = self.rooms[room_name]
        
        # Update story
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, room["description"])
        self.story_text.config(state=tk.DISABLED)
        
        # Update stats
        self.update_stats()
        
        # Clear and update buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        for choice in room["choices"]:
            btn = tk.Button(
                self.button_frame,
                text=choice["text"],
                command=lambda c=choice: self.make_choice(c),
                bg="#333333",
                fg="#00ff00",
                font=("Arial", 10),
                width=50,
                pady=8
            )
            btn.pack(pady=5)
    
    def make_choice(self, choice):
        # Apply sanity change
        if "sanity" in choice:
            self.sanity += choice["sanity"]
            self.sanity = max(0, min(100, self.sanity))
        
        # Add item if available
        if "item" in choice:
            self.inventory.append(choice["item"])
        
        # Check game over conditions
        if self.sanity <= 0:
            messagebox.showwarning("Game Over", "Your sanity has completely shattered.\nYou lose touch with reality.")
            self.load_room("ending_possessed")
            return
        
        # Load next room
        self.load_room(choice["next"])
    
    def update_stats(self):
        inventory_str = ", ".join(self.inventory) if self.inventory else "Empty"
        
        stats_text = f"""HEALTH: {self.health}/100  |  SANITY: {self.sanity}/100  |  INVENTORY: {inventory_str}"""
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = HorrorGame(root)
    root.mainloop()
