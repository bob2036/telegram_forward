#!/usr/bin/env python3
import os
from telethon.sync import TelegramClient
from telethon import events
import time
import sys

# Configuration
API_ID = os.getenv('API_ID', '31975468')
API_HASH = os.getenv('API_HASH', '87be4666f1aaa47bb3f7a643793f9bb5')
PHONE = os.getenv('PHONE', '+33658026889')
SOURCE_CHAT = os.getenv('SOURCE_CHAT', '@XCommasBot')
TARGET_CHAT = os.getenv('TARGET_CHAT', '@n8nph007bot')
SESSION_PATH = os.getenv('SESSION_PATH', '/app/sessions/chat_forward_session')

def log(message):
    """Log avec timestamp"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print("[{}] {}".format(timestamp, message))
    sys.stdout.flush()

def main():
    log("=" * 60)
    log("🚀 TELEGRAM MESSAGE FORWARDER")
    log("=" * 60)
    log("📱 Téléphone : {}".format(PHONE))
    log("📂 Source    : {}".format(SOURCE_CHAT))
    log("📤 Dest      : {}".format(TARGET_CHAT))
    log("💾 Session   : {}".format(SESSION_PATH))
    log("=" * 60)
    log("")
    
    # Créer le répertoire si nécessaire
    os.makedirs('/app/sessions', exist_ok=True)
    
    # Connexion
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    
    try:
        log("🔐 Connexion à Telegram...")
        client.start(phone=PHONE)
        
        me = client.get_me()
        log("✅ Connecté : {} {} (@{})".format(
            me.first_name, 
            me.last_name or '', 
            me.username or 'N/A'
        ))
        log("")
        
        # Récupérer le bot source
        log("🔍 Recherche bot source...")
        try:
            source_entity = client.get_entity(SOURCE_CHAT)
            log("✅ Source : {} (@{})".format(
                source_entity.first_name,
                source_entity.username
            ))
        except ValueError:
            log("❌ Bot source non trouvé : {}".format(SOURCE_CHAT))
            log("   Envoyez /start au bot depuis votre Telegram")
            return 1
        
        # Récupérer le bot destination
        log("🔍 Recherche bot destination...")
        try:
            target_entity = client.get_entity(TARGET_CHAT)
            log("✅ Destination : {} (@{})".format(
                target_entity.first_name,
                target_entity.username
            ))
        except ValueError:
            log("❌ Bot destination non trouvé : {}".format(TARGET_CHAT))
            log("   Envoyez /start au bot depuis votre Telegram")
            return 1
        
        log("")
        log("=" * 60)
        log("🟢 TRANSFERT ACTIF")
        log("=" * 60)
        log("")
        
        # Handler pour transférer les messages
        @client.on(events.NewMessage(chats=source_entity))
        async def handler(event):
            try:
                if event.text:
                    await client.send_message(target_entity, event.text)
                    preview = event.text[:50]
                    if len(event.text) > 50:
                        preview += "..."
                    log("📨 Transféré : {}".format(preview))
                elif event.media:
                    await client.send_file(
                        target_entity, 
                        event.media, 
                        caption=event.message.message if event.message else ''
                    )
                    log("📎 Media transféré")
            except Exception as e:
                log("❌ Erreur : {}".format(str(e)))
        
        # Rester actif
        log("⏳ En attente de messages... (Ctrl+C pour arrêter)")
        client.run_until_disconnected()
        
    except KeyboardInterrupt:
        log("")
        log("⏹️  Arrêt demandé")
        return 0
    except Exception as e:
        log("❌ ERREUR : {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if client.is_connected():
            client.disconnect()
        log("👋 Déconnexion")
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)