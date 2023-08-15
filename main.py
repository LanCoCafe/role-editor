import disnake
from disnake.ext import commands
from disnake import OptionType

import tracemalloc
tracemalloc.start()

import os
from dotenv import load_dotenv

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    global auto_role_name
    if auto_role_name:
        role = disnake.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
            print(f"已經給予 {member.name} 身分組：{role.name}！")

@bot.slash_command(name="set_autorole", description="設定新成員自動獲得的身分組")
async def set_autorole(inter, role: disnake.Role = disnake.Option(name="role", description="新的身分組名稱", type=OptionType.role)):
    global auto_role_name
    auto_role_name = role.name
    await inter.response.send_message(f"已設定新成員將自動獲得的身分組為 `{role.name}`！")


# @bot.slash_command(name="giveroles", description="給予使用者指定的身分組")
# async def giveroles(inter, 
#                     user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"),
#                     role: disnake.Role = disnake.Option(name="role", description="身分組名稱")):
    
#     member = await inter.guild.fetch_member(user.id)

#     role_to_add = disnake.utils.get(inter.guild.roles, name=role.name)

#     if role_to_add:
#         await member.add_roles(role_to_add)

#         await inter.response.send_message(f"已給予 {member.display_name} 身分組：{role_to_add.name}！")
#     else:
#         await inter.response.send_message(f"找不到指定的身分組！")

@bot.slash_command(name="giveroles", description="給予使用者指定的身分組")
async def giveroles(inter, 
                    user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"),
                    role1: disnake.Role = disnake.Option(name="role1", description="第一個身分組名稱", required=False),
                    role2: disnake.Role = disnake.Option(name="role2", description="第二個身分組名稱", required=False),
                    role3: disnake.Role = disnake.Option(name="role3", description="第三個身分組名稱", required=False)):
    
    member = await inter.guild.fetch_member(user.id)

    roles_to_add = [role for role in [role1, role2, role3] if role]

    if roles_to_add:
        await member.add_roles(*roles_to_add)
        
        role_names = ", ".join(role.name for role in roles_to_add)
        await inter.response.send_message(f"已給予 {member.display_name} 身分組：{role_names}！")
    else:
        await inter.response.send_message(f"請至少選擇一個身分組！")


@bot.slash_command(name="removerole", description="移除使用者的指定身分組")
async def removerole(inter, user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"), role: disnake.Role = disnake.Option(name="role", description="選擇一個身分組", type=OptionType.role)):
    member = await inter.guild.fetch_member(user.id)
    await member.remove_roles(role)
    await inter.response.send_message(f"已從 {member.display_name} 移除身分組：{role.name}！")

@bot.slash_command(name="createrole", description="在伺服器中創建一個新的身分組")
async def createrole(inter, role_name: str = disnake.Option(name="role_name", description="新的身分組名稱", type=OptionType.string)):
    await inter.guild.create_role(name=role_name)
    await inter.response.send_message(f"已創建身分組：{role_name}！")

@bot.slash_command(name="deleterole", description="刪除指定的身分組")
async def deleterole(inter, role: disnake.Role = disnake.Option(name="role", description="選擇一個要刪除的身分組", type=OptionType.role)):
    await role.delete()
    await inter.response.send_message(f"已刪除身分組：{role.name}！")

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
