import os

def setup():
    print("========================================")
    print("   DARKCORE v5.0 - SETUP CONFIGURATOR   ")
    print("========================================\n")
    
    token = input("1. Insira o TOKEN do seu Bot: ").strip()
    guild_id = input("2. Insira o ID do seu Servidor: ").strip()
    notice_id = input("3. Insira o ID do Canal de avisos: ").strip()
    
    env_content = f"DISCORD_TOKEN={token}\nGUILD_ID={guild_id}\nNOTICE_CHANNEL_ID={notice_id}\n"
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("\n[✅] Arquivo .env criado! Agora pode rodar o DarkCore_v5_Ultimate.py")

if __name__ == "__main__":
    setup()
