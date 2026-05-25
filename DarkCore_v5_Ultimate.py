import os
import asyncio
import threading
import discord
import customtkinter as ctk
try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

# --- Configurações de Estilo Hacker ---
THEME_COLOR = "#00FF00"  # Verde Matrix/Hacker
BG_COLOR = "#000000"     # Preto Absoluto
INPUT_BG = "#050505"
BTN_COLOR = "#0a0a0a"
BORDER_COLOR = "#00FF00"
FONT_TERMINAL = ("Courier New", 14, "bold")
ACCESS_PASSWORD = "0201" # Senha de acesso

# --- MODAL PARA NOTICE_RAID ---
class NoticeRaidModal(discord.ui.Modal, title='SYSTEM ALERT - SKYBOT'):
    link = discord.ui.TextInput(label='TARGET LINK', placeholder='https://discord.gg/...', style=discord.TextStyle.short, required=True )
    reason = discord.ui.TextInput(label='REASON / EVIDENCE', placeholder='Describe the violation...', style=discord.TextStyle.paragraph, required=True)

    def __init__(self, raid_type: str):
        super().__init__()
        self.raid_type = raid_type

    async def on_submit(self, interaction: discord.Interaction):
        notice_id = os.getenv('NOTICE_CHANNEL_ID')
        channel = interaction.guild.get_channel(int(notice_id)) if notice_id and notice_id.isdigit() else None
        if not channel: channel = discord.utils.get(interaction.guild.text_channels, name='notice-raid')
        
        if not channel:
            await interaction.response.send_message("SYSTEM ERROR: DESTINATION CHANNEL NOT FOUND.", ephemeral=True)
            return

        embed = discord.Embed(title="⚡ SKYBOT INTRUSION ALERT ⚡", color=0x00FF00)
        embed.add_field(name="[PROTOCOL]", value=f"`{self.raid_type}`", inline=True)
        embed.add_field(name="[OPERATOR]", value=interaction.user.mention, inline=True)
        embed.add_field(name="[TARGET]", value=f"```{self.link.value}```", inline=False)
        embed.add_field(name="[REASON]", value=f"```{self.reason.value}```", inline=False)
        embed.set_footer(text=f"SKYBOT.EXE | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        await channel.send(embed=embed)
        await interaction.response.send_message("ALERTA ENVIADO AO SISTEMA CENTRAL.", ephemeral=True)

# --- BOT CORE ---
class DarkCoreBot(commands.Bot):
    def __init__(self, log_callback):
        intents = discord.Intents.all()
        super().__init__(command_prefix=".", intents=intents)
        self.log_callback = log_callback

    async def setup_hook(self):
        @self.tree.command(name="painel", description="Abre o terminal SkyBot no Discord")
        async def painel_cmd(interaction: discord.Interaction):
            embed = discord.Embed(title="📟 SKYBOT.EXE TERMINAL", description="Selecione o módulo de operação:", color=0x00FF00)
            embed.set_thumbnail(url="https://files.manuscdn.com/user_upload_by_module/session_file/310519663690963991/jMwSsfOXXoWrYeix.png")
            embed.set_image(url="https://i.imgur.com/8jrG4oP7FPWD.gif")
            view = discord.ui.View()
            options = [
                discord.SelectOption(label="Raid de Servidor", value="SERVER_RAID", emoji="⚔️"),
                discord.SelectOption(label="Conteúdo Inapropriado", value="ILLEGAL_CONTENT", emoji="🔞"),
                discord.SelectOption(label="Spam/Flood", value="SPAM_ATTACK", emoji="📢"),
            ]
            select = discord.ui.Select(placeholder="[ SELECT MODULE ]", options=options)
            async def callback(inter): await inter.response.send_modal(NoticeRaidModal(select.values[0]))
            select.callback = callback
            view.add_item(select)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        @self.tree.command(name="notice_raid", description="Formulário rápido de aviso")
        async def notice_cmd(interaction: discord.Interaction):
            await interaction.response.send_modal(NoticeRaidModal("QUICK_NOTICE"))

        @self.tree.command(name="raid_send", description="Envia uma mensagem repetidamente")
        @app_commands.describe(mensagem="Qualquer mensagem", vezes="Raid normal")
        async def raid_send_cmd(interaction: discord.Interaction, mensagem: str, vezes: int):
            self.log_callback(f"[CMD] {interaction.user.name} iniciou /raid_send ({vezes}x)")
            await interaction.response.send_message(f"INICIANDO PROTOCOLO DE ENVIO: {vezes} VEZES.", ephemeral=True)
            for i in range(vezes):
                try:
                    await interaction.channel.send(mensagem)
                    await asyncio.sleep(0.2)
                except Exception as e:
                    self.log_callback(f"[!] Erro no envio repetitivo: {e}")
                    break
            self.log_callback(f"[OK] Protocolo /raid_send finalizado.")

        @self.tree.command(name="raid_image", description="Envia uma imagem repetidamente")
        @app_commands.describe(url="URL da imagem", vezes="Número de vezes para enviar")
        async def raid_image_cmd(interaction: discord.Interaction, url: str, vezes: int):
            self.log_callback(f"[CMD] {interaction.user.name} iniciou /raid_image ({vezes}x)")
            await interaction.response.send_message(f"INICIANDO PROTOCOLO DE ENVIO DE IMAGEM: {vezes} VEZES.", ephemeral=True)
            for i in range(vezes):
                try:
                    await interaction.channel.send(url)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    self.log_callback(f"[!] Erro no envio repetitivo de imagem: {e}")
                    break
            self.log_callback(f"[OK] Protocolo /raid_image finalizado.")

        @self.tree.command(name="raid_ban", description="Bane um usuário do servidor")
        @app_commands.describe(membro="O membro a ser banido", motivo="Motivo do banimento (opcional)")
        async def raid_ban_cmd(interaction: discord.Interaction, membro: discord.Member, motivo: str = "Sem motivo especificado"):
            self.log_callback(f"[CMD] {interaction.user.name} iniciou /raid_ban contra {membro.name}")
            if not interaction.user.guild_permissions.ban_members:
                await interaction.response.send_message("ERRO: Você não tem permissão para banir membros.", ephemeral=True)
                self.log_callback(f"[!] Erro: {interaction.user.name} não tem permissão de ban.")
                return
            
            try:
                await membro.ban(reason=motivo)
                await interaction.response.send_message(f"USUÁRIO BANIDO: {membro.display_name} por {motivo}", ephemeral=True)
                self.log_callback(f"[OK] {membro.name} foi banido com sucesso.")
            except discord.Forbidden:
                await interaction.response.send_message("ERRO: Não tenho permissão para banir este membro.", ephemeral=True)
                self.log_callback(f"[!] Erro: Bot sem permissão para banir {membro.name}")
            except Exception as e:
                await interaction.response.send_message(f"ERRO INESPERADO: {e}", ephemeral=True)
                self.log_callback(f"[!] Erro crítico no ban: {e}")

        @self.tree.command(name="raid_mixed", description="Envia uma imagem com texto repetidamente")
        @app_commands.describe(url="URL da imagem", texto="Texto a ser enviado", vezes="Número de vezes para enviar")
        async def raid_mixed_cmd(interaction: discord.Interaction, url: str, texto: str, vezes: int):
            self.log_callback(f"[CMD] {interaction.user.name} iniciou /raid_mixed ({vezes}x)")
            await interaction.response.send_message(f"INICIANDO PROTOCOLO DE ENVIO MISTO: {vezes} VEZES.", ephemeral=True)
            for i in range(vezes):
                try:
                    await interaction.channel.send(content=texto, embed=discord.Embed().set_image(url=url))
                    await asyncio.sleep(0.7)
                except Exception as e:
                    self.log_callback(f"[!] Erro no envio misto: {e}")
                    break
            self.log_callback(f"[OK] Protocolo /raid_mixed finalizado.")

        @self.tree.command(name="sky_nuke", description="Destruição Massiva (Cria categorias e canais)")
        @app_commands.describe(nome="Nome base para tudo", quantidade="Quantidade de categorias")
        async def sky_nuke_cmd(interaction: discord.Interaction, nome: str, quantidade: int = 5):
            self.log_callback(f"[🚀] SKYBOT.EXE: PROTOCOLO NUKE ATIVADO POR {interaction.user.name}")
            await interaction.response.send_message("🚀 INICIANDO DESTRUIÇÃO SKYBOT...", ephemeral=True)
            
            for i in range(quantidade):
                try:
                    cat = await interaction.guild.create_category(name=f"{nome}-{i+1}")
                    self.log_callback(f"[+] Categoria: {cat.name}")
                    for j in range(3): # Cria 3 canais por categoria
                        chan = await interaction.guild.create_text_channel(name=nome, category=cat)
                        self.log_callback(f"  └─ Canal: {chan.name}")
                        await asyncio.sleep(0.2)
                except Exception as e:
                    self.log_callback(f"[!] Erro no Nuke: {e}")
                    break
            self.log_callback("[OK] SKYBOT: Operação concluída.")

        @self.tree.command(name="sky_spam_voice", description="Cria múltiplos canais de voz rapidamente")
        @app_commands.describe(nome="Nome dos canais", quantidade="Quantidade")
        async def sky_voice_cmd(interaction: discord.Interaction, nome: str, quantidade: int = 10):
            self.log_callback(f"[🎤] SKYBOT: Criando {quantidade} canais de voz...")
            await interaction.response.send_message("🎤 INICIANDO SPAM DE VOZ...", ephemeral=True)
            for i in range(quantidade):
                try:
                    v = await interaction.guild.create_voice_channel(name=nome)
                    self.log_callback(f"[+] Voz: {v.name}")
                    await asyncio.sleep(0.2)
                except Exception as e:
                    self.log_callback(f"[!] Erro: {e}")
                    break
            self.log_callback("[OK] SKYBOT: Canais de voz prontos.")

        @self.tree.command(name="sky_purge", description="Limpeza Total (Apaga TODOS os canais e categorias)")
        async def sky_purge_cmd(interaction: discord.Interaction):
            self.log_callback(f"[🧹] SKYBOT: PROTOCOLO PURGE ATIVADO POR {interaction.user.name}")
            await interaction.response.send_message("🧹 INICIANDO LIMPEZA TOTAL...", ephemeral=True)
            
            # Deleta canais
            for channel in interaction.guild.channels:
                try:
                    await channel.delete()
                    self.log_callback(f"[-] Deletado: {channel.name}")
                    await asyncio.sleep(0.1)
                except:
                    continue
            
            # Cria um canal de emergência para não ficar vazio
            try:
                new = await interaction.guild.create_text_channel(name="skybot-zone")
                self.log_callback(f"[!] Canal de emergência criado: {new.name}")
            except:
                pass
                
            self.log_callback("[OK] SKYBOT: Servidor limpo.")

        @self.tree.command(name="sky_trailer", description="Exibe o trailer cinematográfico do SkyBot.exe")
        @app_commands.describe(versao="Escolha qual versão do trailer exibir")
        @app_commands.choices(versao=[
            app_commands.Choice(name="Oficial (The Ascension)", value="trailer_oficial.mp4"),
            app_commands.Choice(name="Teaser (Ameaça)", value="teaser_ameaca.mp4"),
            app_commands.Choice(name="Raid Promo", value="raid_promo.mp4")
        ])
        async def sky_trailer_cmd(interaction: discord.Interaction, versao: str):
            self.log_callback(f"[🎬] SKYBOT: Preparando envio do {versao} para {interaction.user.name}")
            video_path = os.path.join(os.path.dirname(__file__), versao)
            embed = discord.Embed(title=f"🎞️ SKYBOT.EXE: {versao.replace('.mp4', '').upper()}", description="***A verdadeira ameaça...***", color=0x00FF00)
            if os.path.exists(video_path):
                await interaction.response.send_message(embed=embed, file=discord.File(video_path))
                self.log_callback(f"[OK] {versao} enviado.")
            else:
                await interaction.response.send_message("ERRO: Arquivo de vídeo não encontrado.")

        @self.tree.command(name="sky_spam_clip", description="Spam massivo de vídeo + texto")
        @app_commands.describe(texto="Mensagem para o spam", vezes="Quantidade de vezes")
        async def sky_spam_clip_cmd(interaction: discord.Interaction, texto: str, vezes: int = 5):
            self.log_callback(f"[🚀] SKYBOT: Iniciando Spam de Clip ({vezes}x) por {interaction.user.name}")
            await interaction.response.send_message(f"🚀 INICIANDO ATAQUE DE CLIP: {vezes} VEZES.", ephemeral=True)
            
            video_path = os.path.join(os.path.dirname(__file__), "oficial.mp4")
            
            for i in range(vezes):
                try:
                    if os.path.exists(video_path):
                        await interaction.channel.send(content=texto, file=discord.File(video_path))
                    else:
                        await interaction.channel.send(content=f"{texto}\n[!] Erro: trailer_oficial.mp4 não encontrado.")
                    await asyncio.sleep(1.5) # Delay maior para upload de vídeo
                except Exception as e:
                    self.log_callback(f"[!] Erro no spam de clip: {e}")
                    break
            self.log_callback("[OK] SKYBOT: Spam de clip finalizado.")

        try:
            # Força a sincronização global (pode demorar alguns minutos para aparecer em todos os servers)
            await self.tree.sync()
            self.log_callback("[*] COMANDOS SINCRONIZADOS GLOBALMENTE.")
        except Exception as e:
            self.log_callback(f"[!] Erro na sincronização: {e}")

    # --- EVENTOS DE MONITORAMENTO ---
    async def on_guild_channel_create(self, channel):
        self.log_callback(f"[EVENT] Novo canal criado: #{channel.name} ({channel.type})")

    async def on_member_ban(self, guild, user):
        self.log_callback(f"[EVENT] Usuário banido do servidor: {user.name}#{user.discriminator}")

    async def on_guild_channel_delete(self, channel):
        self.log_callback(f"[EVENT] Canal deletado: #{channel.name}")

    async def on_message(self, message):
        if message.author == self.user: return
        # Opcional: Logar mensagens se quiser monitorar o chat
        # self.log_callback(f"[MSG] {message.author.name}: {message.content[:50]}")
        await self.process_commands(message)

# --- INTERFACE GUI ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SKYBOT.EXE - ELITE HACKER TERMINAL")
        self.geometry("1200x850")
        self.configure(fg_color=BG_COLOR)
        self.bot = None
        self.show_login()
        # winsound doesn't need initialization

    def show_login(self):
        self.login_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.login_frame, text="[ ACCESS RESTRICTED ]", font=("Courier New", 24, "bold"), text_color=THEME_COLOR).pack(pady=20)
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="ENTER PASSWORD", show="*", width=300, fg_color=INPUT_BG, border_color=THEME_COLOR)
        self.pass_entry.pack(pady=10)
        ctk.CTkButton(self.login_frame, text="LOGIN", command=self.check_login, fg_color=BTN_COLOR, border_width=1, border_color=THEME_COLOR).pack(pady=20)

    def check_login(self):
        if self.pass_entry.get() == ACCESS_PASSWORD:
            self.login_frame.destroy()
            self.setup_main_ui()
            self.play_sound("access_granted.wav")
            self.animate_intro()
        else:
            self.pass_entry.configure(border_color="red")
            self.log_login_error()

    def log_login_error(self):
        print("[!] ACCESS DENIED: INVALID PASSWORD")

    def setup_main_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color=INPUT_BG, border_width=1, border_color=THEME_COLOR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="⚡ SKYBOT.EXE", font=("Courier New", 20, "bold"), text_color=THEME_COLOR).pack(pady=30)

        menu_items = [
            ("INITIATE BOT", self.start_bot, "#003300"),
            ("NOTICE RAID", lambda: self.log("Use /notice_raid no Discord"), BTN_COLOR),
            ("SERVER RAID", lambda: self.log("Use /painel no Discord"), BTN_COLOR),
            ("CLEAN SYSTEM", lambda: self.log("Cleaning cache..."), BTN_COLOR),
            ("EXIT", self.quit, "#330000")
        ]

        for text, cmd, color in menu_items:
            ctk.CTkButton(self.sidebar, text=text, command=cmd, fg_color=color, border_width=1, border_color=THEME_COLOR, hover_color="#00FF00").pack(fill="x", padx=20, pady=8)

        # MAIN TERMINAL
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.terminal = ctk.CTkTextbox(self.main_frame, fg_color="#050505", text_color=THEME_COLOR, font=FONT_TERMINAL, border_width=1, border_color=THEME_COLOR)
        self.terminal.pack(expand=True, fill="both", pady=(0, 15))
        self.terminal.configure(state="disabled")

        self.cmd_input = ctk.CTkEntry(self.main_frame, placeholder_text="[ ROOT@ZIOLES:~$ ]", fg_color=INPUT_BG, border_color=THEME_COLOR, height=45, font=FONT_TERMINAL)
        self.cmd_input.pack(fill="x")

    def log(self, msg):
        # Thread-safe logging for CustomTkinter
        def _append():
            self.terminal.configure(state="normal")
            self.terminal.insert("end", f">>> {msg}\n")
            self.terminal.see("end")
            self.terminal.configure(state="disabled")
        self.after(0, _append)

    def play_sound(self, sound_file):
        if WINSOUND_AVAILABLE:
            try:
                # Get the absolute path of the script directory
                base_path = os.path.dirname(os.path.abspath(__file__))
                full_path = os.path.join(base_path, sound_file)
                
                if os.path.exists(full_path):
                    # Play sound asynchronously using the full absolute path
                    threading.Thread(target=lambda: winsound.PlaySound(full_path, winsound.SND_FILENAME), daemon=True).start()
                else:
                    self.log(f"[!] Arquivo de som não encontrado em: {full_path}")
            except Exception as e:
                self.log(f"[!] Erro ao reproduzir som: {e}")

    def animate_intro(self):
        intro = [
            "DECRYPTING SYSTEM FILES...",
            "BYPASSING SECURITY LAYERS...",
            "ACCESS GRANTED TO ZIOLES.",
            "",
            "██╗  ██╗███████╗██╗     ██╗      ██████╗ ",
            "██║  ██║██╔════╝██║     ██║     ██╔═══██╗",
            "███████║█████╗  ██║     ██║     ██║   ██║",
            "██╔══██║██╔══╝  ██║     ██║     ██║   ██║",
            "██║  ██║███████╗███████╗███████╗╚██████╔╝",
            "╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ",
            "",
            "   >>> HELLO ZIOLES <<<   ",
            "   [ DARKCORE ULTIMATE ]  ",
            "",
            "SYSTEM STATUS: READY"
        ]
        self.terminal.configure(state="normal")
        def add(i):
            if i < len(intro):
                self.terminal.insert("end", intro[i] + "\n")
                self.after(40, lambda: add(i+1))
            else: self.terminal.configure(state="disabled")
        add(0)

    def start_bot(self):
        token = self.cmd_input.get().strip() or os.getenv('DISCORD_TOKEN')
        if not token: return self.log("ERROR: TOKEN REQUIRED")
        
        def run():
            try:
                self.bot = DarkCoreBot(self.log)
                self.log("CONNECTING TO DISCORD GATEWAY...")
                self.bot.run(token)
            except Exception as e:
                self.log(f"CRITICAL ERROR: {str(e)}")
        
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    App().mainloop()