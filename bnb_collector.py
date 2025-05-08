import asyncio
import json
import re
import sys
import os
from telethon import TelegramClient, events
from rich.console import Console
from rich.progress import Progress

console = Console()

# Charger la configuration
with open("config.json", "r") as f:
    config = json.load(f)

api_id = config["api_id"]
api_hash = config["api_hash"]
phone = config["phone"]
bot_username = "LegitBotsOnline"

client = TelegramClient("bnb_session", api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    msg = event.message.message
    console.print(f"[bold green]Réponse du bot :[/bold green] {msg}")

    match = re.search(r"Wait (\d+) seconds", msg)
    wait_time = int(match.group(1)) if match else 60

    with Progress() as progress:
        task = progress.add_task("[cyan]Attente...", total=wait_time)
        for _ in range(wait_time):
            await asyncio.sleep(1)
            progress.update(task, advance=1)

    try:
        await client.send_message(bot_username, "✅ Free Bnb Collect 🏛️")
        console.print("[bold green]Commande envoyée avec succès.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Erreur lors de l'envoi :[/bold red] {e}")

async def main():
    await client.start(phone=phone)
    console.print("[bold yellow]Bot démarré...[/bold yellow]")
    await client.send_message(bot_username, "✅ Free Bnb Collect 🏛️")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
