import csv
import requests

headers = {"X-Mashape-Key": "INSERT hearthstoneapi.com KEY HERE"}
cards = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards", headers=headers)
cards_info = cards.json()

standard_set = ["Basic", "Classic",
                "Journey to Un'Goro", "Knights of the Frozen Throne", "Kobolds & Catacombs",
                "The Witchwood"]
wild_set = ["Hall of Fame",
            "Naxxramas", "Goblins vs Gnomes",
            "Blackrock Mountain", "The Grand Tournament", "The League of Explorers",
            "Whispers of the Old Gods", "One Night in Karazhan", "Mean Streets of Gadgetzan"]
all_set = standard_set + wild_set

with open('hearthstone.csv', 'w', newline='') as csv_file:
    field_names = ["Card ID", "Card Name", "Card Set", "Card Type", "Class", "Rarity", "Mana Cost",
                   "Attack", "Health", "Card Mechanics", "Race", "Collectible"]
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for card_set in all_set:
        card_set_info = cards_info[card_set]

        for card in card_set_info:

            if card.get("type") == "Enchantment":
                continue

            card_id = card.get("cardId")
            card_name = card.get("name")
            card_set = card.get("cardSet")
            card_type = card.get("type")
            card_class = card.get("playerClass")
            rarity = card.get("rarity")
            mana_cost = card.get("cost")

            attack = ""
            if card_type == "Minion" or card_type == "Weapon":
                attack = str(card.get("attack"))

            health = ""
            if card_type == "Minion" or card_type == "Hero":
                health = str(card.get("health"))
            elif card_type == "Weapon":
                health = str(card.get("durability"))

            card_mechanics_list = []
            if card.get("mechanics") is not None:
                card_mechanics_list = card.get("mechanics")
            card_mechanics_str = ""
            for i in range(len(card_mechanics_list)):
                card_mechanic = card_mechanics_list[i]["name"]
                if card_mechanic == "ImmuneToSpellpower":
                    card_mechanic = "Immune to Spell Power"
                elif card_mechanic == "HealTarget":
                    card_mechanic = "Heal Target"
                elif card_mechanic == "AdjacentBuff":
                    card_mechanic = "Adjacent Buff"
                elif card_mechanic == "AffectedBySpellPower":
                    card_mechanic = "Affected by Spell Power"

                if i != 0:
                    card_mechanics_str += ", "
                card_mechanics_str += card_mechanic

            race = card.get("race")

            collectible = card.get("collectible")
            if collectible is None:
                collectible = False

            writer.writerow({"Card ID": card_id, "Card Name": card_name, "Card Set": card_set,
                             "Card Type": card_type, "Class": card_class, "Rarity": rarity, "Mana Cost": mana_cost,
                             "Attack": attack, "Health": health, "Card Mechanics": card_mechanics_str,
                             "Race": race, "Collectible": collectible})
