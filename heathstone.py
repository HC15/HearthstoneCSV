import csv
import requests

headers = {"X-Mashape-Key": "INSERT KEY FROM hearthstoneapi.com HERE"}
cards = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards" + "?collectible=1", headers=headers)
cardInfo = cards.json()

standardSet = ["Basic", "Classic", "Blackrock Mountain", "The Grand Tournament",
               "The League of Explorers", "Whispers of the Old Gods"]
wildSet = ["Naxxramas", "Goblins vs Gnomes", "Reward", "Promotion"]
allSet = standardSet + wildSet

with open('hearthstone.csv', 'w', newline = '') as csvfile:
    fieldNames = ["Card Name", "Card Set", "Card Type", "Class", "Rarity", "Mana Cost", "Attack", "Health", "Race"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
    writer.writeheader()

    for cardSet in allSet:
        cardSetInfo = cardInfo[cardSet]
        for card in cardSetInfo:
            if card["type"] == "Minion":
                if "playerClass" in card:
                    writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                     "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                     "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                     "Attack": str(card.get("attack")), "Health": str(card.get("health")),
                                     "Race": card.get("race")})
                else:
                    writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                     "Card Type": card.get("type"), "Class": "Neutral",
                                     "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                     "Attack": str(card.get("attack")), "Health": str(card.get("health")),
                                     "Race": card.get("race")})
            if card["type"] == "Spell":
                writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                 "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                 "Rarity": card.get("rarity"), "Mana Cost": card.get("cost")})
            if card["type"] == "Weapon":
                writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                 "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                 "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                 "Attack": str(card.get("attack")), "Health": str(card.get("durability"))})