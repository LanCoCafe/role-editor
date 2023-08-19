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

@bot.slash_command(description="顯示所有可用的命令和說明")
async def help(inter):
    embed = disnake.Embed(title="幫助", description="這是我們的命令列表和說明：", color=0x00FF00)

    embed.add_field(name="/role", value="關於身分組的主命令", inline=False)
    embed.add_field(name="/role auto", value="設定新成員自動獲得的身分組", inline=False)
    embed.add_field(name="/role give_everyone", value="給予所有成員指定的身分組", inline=False)
    embed.add_field(name="/role give_bot", value="給予所有機器人指定的身分組", inline=False)
    embed.add_field(name="/role give_member", value="給予所有非機器人成員指定的身分組", inline=False)
    embed.add_field(name="/role give_specify", value="給予特定身分組的成員指定的身分組", inline=False)
    embed.add_field(name="/role give", value="給予使用者指定的身分組", inline=False)
    embed.add_field(name="/role remove", value="移除使用者的指定身分組", inline=False)
    embed.add_field(name="/role create", value="在伺服器中創建一個新的身分組", inline=False)
    embed.add_field(name="/role delete", value="刪除指定的身分組", inline=False)

    await inter.response.send_message(embed=embed)


bot.load_extension("cmds.role_commands")  # 載入 role_commands 模組

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
