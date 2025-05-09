import asyncio
import json
import re
import sys
import os
from telethon import TelegramClient, events, Button
from rich.console import Console
from rich.progress import Progress

console = Console()

# Vérifier que config.json existe
if not os.path.isfile("config.json"):
    console.print("[bold red]Erreur : le fichier config.json est introuvable.[/bold red]")
    sys.exit(1)

# Charger la configuration
with open("config.json", "r") as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError:
        console.print("[bold red]Erreur : config.json est mal formé.[/bold red]")
        sys.exit(1)

api_id = config.get("api_id")
api_hash = config.get("api_hash")
phone = config.get("phone")
bot_username = "Free_Binance_Bnb_Pay_Bot"

client = TelegramClient("bnb_session", api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    msg = event.message.message
    console.print(f"[bold green]Réponse du bot :[/bold green] {msg}")

    # Si des boutons sont présents, chercher ceux avec 🎁 ou "treasury" ou "collect"
    if event.buttons:
        for row in event.buttons:
            for button in row:
                if hasattr(button, "text"):
                    b_text = button.text.lower()
                    if "🎁" in b_text or "collect" in b_text or "treasury" in b_text:
                        console.print(f"[bold blue]→ Clic automatique sur :[/bold blue] {button.text}")
                        try:
                            await button.click()  # <-- correction ici
                            await asyncio.sleep(2)
                        except Exception as e:
                            console.print(f"[bold red]Erreur lors du clic :[/bold red] {e}")

    # Déterminer le temps d'attente
    match = re.search(r"Wait (\d+) seconds", msg)
    wait_time = int(match.group(1)) if match else 60

    # Animation d'attente
    with Progress() as progress:
        task = progress.add_task("[cyan]Attente avant prochaine commande...", total=wait_time)
        for _ in range(wait_time):
            await asyncio.sleep(1)
            progress.update(task, advance=1)

    # Relancer la commande
    try:
        await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
        console.print("[bold green]Commande envoyée avec succès.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Erreur lors de l'envoi :[/bold red] {e}")

async def main():
    try:
        await client.start(phone=phone)
        console.print("[bold yellow]Bot démarré...[/bold yellow]")

        # Vérifier que le bot est valide
        try:
            await client.get_entity(bot_username)
        except ValueError:
            console.print(f"[bold red]Erreur : le bot @{bot_username} est introuvable.[/bold red]")
            return

        await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
        await client.run_until_disconnected()

    except Exception as e:
        console.print(f"[bold red]Erreur lors du démarrage :[/bold red] {e}")

with client:
    client.loop.run_until_complete(main())
