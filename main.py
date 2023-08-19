import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv


intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    try:
        with open("auto_role.txt", "r") as file:
            auto_role_name = file.readline().strip()
    except FileNotFoundError:
        auto_role_name = None

    if auto_role_name:
        role = disnake.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
            print(f"已經給予 {member.name} 身分組：{role.name}！")


bot.load_extension("cmds.role_commands")  # 載入 role_commands 模組

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
