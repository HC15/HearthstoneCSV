import csv
import requests

headers = {"X-Mashape-Key": "NcRwezHwkamshpfs6yqjQfFhtDmip19NUG9jsnqWHT3KfRcM0g"}
cards = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards" + "?collectible=0", headers=headers)
cardInfo = cards.json()

standardSet = ["Basic", "Classic", "Journey to Un'Goro", "Knights of the Frozen Throne",
               "Kobolds & Catacombs", "The Witchwood"]
wildSet = ["Hall of Fame", "Naxxramas", "Goblins vs Gnomes",
           "Blackrock Mountain", "The Grand Tournament", "The League of Explorers",
           "Whispers of the Old Gods", "One Night in Karazhan", "Mean Streets of Gadgetzan"]
allSet = standardSet + wildSet

with open('hearthstone.csv', 'w', newline='') as csvfile:
    fieldNames = ["Card Name", "Card Set", "Card Type", "Class", "Rarity",
                  "Mana Cost", "Attack", "Health", "Card Mechanics", "Race",
                  "Card ID"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
    writer.writeheader()

    for cardSet in allSet:
        cardSetInfo = cardInfo[cardSet]

        for card in cardSetInfo:
            cardMechanicsList = []
            if card.get("mechanics") is not None:
                cardMechanicsList = card.get("mechanics")

            cardMechanicsStr = ""
            for i in range(len(cardMechanicsList)):
                cardMechanic = cardMechanicsList[i]["name"]
                if cardMechanic == "ImmuneToSpellpower":
                    cardMechanic = "Immune to Spell Power"
                elif cardMechanic == "HealTarget":
                    cardMechanic = "Heal Target"
                elif cardMechanic == "AdjacentBuff":
                    cardMechanic = "Adjacent Buff"
                elif cardMechanic == "AffectedBySpellPower":
                    cardMechanic = "Affected by Spell Power"

                if i == 0:
                    cardMechanicsStr += cardMechanic
                else:
                    cardMechanicsStr += ", " + cardMechanic

            if card["type"] == "Minion":
                if "playerClass" in card:
                    writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                     "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                     "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                     "Attack": str(card.get("attack")), "Health": str(card.get("health")),
                                     "Card Mechanics": cardMechanicsStr, "Race": card.get("race"),
                                     "Card ID": card.get("cardId")})
                else:
                    writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                     "Card Type": card.get("type"), "Class": "Neutral",
                                     "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                     "Attack": str(card.get("attack")), "Health": str(card.get("health")),
                                     "Card Mechanics": cardMechanicsStr, "Race": card.get("race"),
                                     "Card ID": card.get("cardId")})
            if card["type"] == "Spell":
                writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                 "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                 "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                 "Card Mechanics": cardMechanicsStr, "Card ID": card.get("cardId")})
            if card["type"] == "Weapon":
                writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                 "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                 "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                 "Attack": str(card.get("attack")), "Health": str(card.get("durability")),
                                 "Card Mechanics": cardMechanicsStr, "Card ID": card.get("cardId")})
            if card["type"] == "Hero":
                writer.writerow({"Card Name": card.get("name"), "Card Set": card.get("cardSet"),
                                 "Card Type": card.get("type"), "Class": card.get("playerClass"),
                                 "Rarity": card.get("rarity"), "Mana Cost": card.get("cost"),
                                 "Health": str(card.get("health")),
                                 "Card Mechanics": cardMechanicsStr, "Card ID": card.get("cardId")})
