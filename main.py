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

class HelpMenu(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="role", description="關於身分組的主命令"),
            disnake.SelectOption(label="role auto", description="設定新成員自動獲得的身分組"),
            # ... 可以根据需要加入更多命令描述
        ]
        super().__init__(placeholder="選擇一個命令來查詢", min_values=1, max_values=1, options=options)

    async def callback(self, inter: disnake.Interaction):
        selected_command = self.values[0]
        description = {
            "role": "關於身分組的主命令...",
            "role auto": "設定新成員自動獲得的身分組...",
            # ... 可以根据需要加入更多命令描述
        }.get(selected_command, "找不到該命令的描述")
        
        embed = disnake.Embed(title=f"命令：{selected_command}", description=description, color=0x00FF00)
        await inter.response.send_message(embed=embed)

@bot.slash_command(description="顯示所有可用的命令和說明")
async def help(inter):
    view = disnake.ui.View()
    view.add_item(HelpMenu())
    await inter.response.send_message("選擇一個命令來查詢:", view=view)

bot.load_extension("cmds.role_commands")  # 載入 role_commands 模組

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
