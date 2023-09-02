import json
import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    try:
        with open("auto_roles.json", "r") as file:
            _ = json.load(file)
    except FileNotFoundError:
        with open("auto_roles.json", "w") as file:
            json.dump({}, file, indent=4)
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
            disnake.SelectOption(label="/role auto", description="設定新使用者的指定身分組"),
            disnake.SelectOption(label="/role give_everyone", description="給予所有人指定身分組"),
            disnake.SelectOption(label="/role give_bot", description="設定新成員自動獲得的身分組"),
            disnake.SelectOption(label="/role give_member", description="設定新成員自動獲得的身分組"),
            disnake.SelectOption(label="/role give_specify", description="設定新成員自動獲得的身分組"),
            disnake.SelectOption(label="/role give", description="移除一位使用者指定身分組"),
            disnake.SelectOption(label="/role remove", description="移除一位使用者指定身分組"),
            disnake.SelectOption(label="/role create", description="創建身分組"),
            disnake.SelectOption(label="/role delete", description="刪除身分組"),
            # disnake.SelectOption(label="", description="設定新成員自動獲得的身分組"),
            # disnake.SelectOption(label="/role auto", description="設定新成員自動獲得的身分組"),
            # disnake.SelectOption(label="/role auto", description="設定新成員自動獲得的身分組"),
            # disnake.SelectOption(label="/role auto", description="設定新成員自動獲得的身分組"),
            # ... 可以根据需要加入更多命令描述
        ]
        super().__init__(placeholder="選擇一個命令來查詢", min_values=1, max_values=1, options=options)

    async def callback(self, inter: disnake.Interaction):
        selected_command = self.values[0]
        description = {
            "/role auto": "設定新使用者的指定身分組",
            "/role give_everyone": "給予所有人指定身分組",
            "/role give_bot": "給予所有機器人指定身分組",
            "/role give_member": "給予所有使用者指定身分組",
            "/role give_specify": "給予擁有此身分組(target_role)的使用者(role)指定身分組",
            "/role give": "給予一位使用者指定身分組",
            "/role remove": "移除一位使用者指定身分組",
            "/role create": "創建身分組",
            "/role delete": "刪除身分組",
            # ... 可以根据需要加入更多命令描述
        }.get(selected_command, "找不到該命令的描述")
        
        embed = disnake.Embed(title=f"命令：{selected_command}", description=description, color=0x91fcff)
        await inter.response.send_message(embed=embed)

class LinkButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(style=disnake.ButtonStyle.link, label="LanCo Café 官方支援伺服器", url="https://discord.gg/seZ3WNTC4J", emoji=":LanCoImage:1135956618262098022")

@bot.slash_command(description="顯示所有可用的命令和說明")
async def help(inter):
    embed = disnake.Embed(
        # title="Role Editor",
        description="感謝你的邀請！我是由 LanCo Café 團隊製作的 Role Editor！\n 專門讓管理身分組變得更輕鬆的機器人！",
        color=0x91fcff 
    )
    embed.set_author(name="Role Editor", icon_url="https://cdn.discordapp.com/attachments/1135881121276629033/1141345683929055312/Untitled.png")
    embed.add_field(name="開發者", value="@langmao", inline=False)
    embed.add_field(name="頭像製作者", value="@yubuur_0614", inline=False)

    view = disnake.ui.View()
    view.add_item(HelpMenu())
    view.add_item(LinkButton())  # 添加 link button 到 view 中
    await inter.response.send_message(embed=embed, view=view)

bot.load_extension("cmds.role_commands")  # 載入 role_commands 模組

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)