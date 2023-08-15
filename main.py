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


# /set_autorole 
@bot.event
async def on_member_join(member):
    global auto_role_name
    if auto_role_name:
        role = disnake.utils.get(member.guild.roles, name=auto_role_name)
        if role:
            await member.add_roles(role)
            print(f"已經給予 {member.name} 身分組：{role.name}！")

@bot.slash_command(name="role_auto", description="設定新成員自動獲得的身分組")
async def set_autorole(inter, role: disnake.Role = disnake.Option(name="role", description="新的身分組名稱", type=OptionType.role)):
    global auto_role_name
    auto_role_name = role.name
    await inter.response.send_message(f"已設定新成員將自動獲得的身分組為 `{role.name}`！")


# /giveallroles

@bot.slash_command(name="role_give_multiple", description="給予指定成員群組的身分組")
async def giveroles(
    inter, 
    target_type: str = disnake.Option(name="target_type", description="目標群組類型 (everyone/bot/member/specify)", type=OptionType.string),
    role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱"),
    target_role: disnake.Role = disnake.Option(name="target_role", description="當目標為 'specify' 時，要給誰的身分組", required=False)
):

    if target_type == "everyone":
        members_to_update = inter.guild.members
    elif target_type == "bot":
        members_to_update = [m for m in inter.guild.members if m.bot]
    elif target_type == "member":
        members_to_update = [m for m in inter.guild.members if not m.bot]
    elif target_type == "specify":
        if not target_role:
            await inter.response.send_message("請指定目標身分組!")
            return
        members_to_update = [m for m in inter.guild.members if target_role in m.roles]
    else:
        await inter.response.send_message("無效的目標類型!")
        return

    for member in members_to_update:
        try:
            await member.add_roles(role)
        except disnake.Forbidden:
            await inter.response.send_message(f"沒有權限為 {member.display_name} 增加身分組!")
            return
        except Exception as e:
            await inter.response.send_message(f"為 {member.display_name} 增加身分組時出錯: {e}")
            return

    await inter.response.send_message(f"已給予所選成員身分組：{role.name}！")


# @bot.slash_command(name="giveallroles", description="給予指定成員群組的身分組")
# async def giveallroles(
#     inter, 
#     role: disnake.Role = disnake.Option(name="role", description="身分組名稱"),
#     target: str = disnake.Option(name="target", description="目標群組 (all/bots/non-bots/specific_role)", type=OptionType.string),
#     specific_role: disnake.Role = disnake.Option(name="specific_role", description="當目標為 specific_role 時，要給誰的身分組", required=False)
# ):

#     if target == "all":
#         members_to_update = inter.guild.members
#     elif target == "bots":
#         members_to_update = [m for m in inter.guild.members if m.bot]
#     elif target == "non-bots":
#         members_to_update = [m for m in inter.guild.members if not m.bot]
#     elif target == "specific_role":
#         if not specific_role:
#             await inter.response.send_message("請指定特定的身分組!")
#             return
#         members_to_update = [m for m in inter.guild.members if specific_role in m.roles]
#     else:
#         await inter.response.send_message("無效的目標選項!")
#         return

#     for member in members_to_update:
#         try:
#             await member.add_roles(role)
#         except disnake.Forbidden:
#             await inter.response.send_message(f"沒有權限為 {member.display_name} 增加身分組!")
#             return
#         except Exception as e:
#             await inter.response.send_message(f"為 {member.display_name} 增加身分組時出錯: {e}")
#             return

#     await inter.response.send_message(f"已給予所選成員身分組：{role.name}！")


# @bot.slash_command(name="giveallroles", description="給予所有成員指定的身分組")
# async def giveallroles(inter, role: disnake.Role = disnake.Option(name="role", description="身分組名稱")):
    
#     for member in inter.guild.members:
#         try:
#             await member.add_roles(role)
#         except disnake.Forbidden:
#             await inter.response.send_message(f"沒有權限為 {member.display_name} 增加身分組!")
#             return  # 可以選擇在這裡終止，或者只記錄錯誤並繼續
#         except Exception as e:
#             await inter.response.send_message(f"為 {member.display_name} 增加身分組時出錯: {e}")
#             return

#     await inter.response.send_message(f"已給予所有成員身分組：{role.name}！")


# /giveroles
@bot.slash_command(name="role_give", description="給予使用者指定的身分組")
async def giveroles(inter, 
                    user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"),
                    role: disnake.Role = disnake.Option(name="role", description="身分組名稱")):
    
    member = await inter.guild.fetch_member(user.id)

    role_to_add = disnake.utils.get(inter.guild.roles, name=role.name)

    if role_to_add:
        await member.add_roles(role_to_add)

        await inter.response.send_message(f"已給予 {member.display_name} 身分組：{role_to_add.name}！")
    else:
        await inter.response.send_message(f"找不到指定的身分組！")


@bot.slash_command(name="role_remove", description="移除使用者的指定身分組")
async def removerole(inter, user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"), role: disnake.Role = disnake.Option(name="role", description="選擇一個身分組", type=OptionType.role)):
    member = await inter.guild.fetch_member(user.id)
    await member.remove_roles(role)
    await inter.response.send_message(f"已從 {member.display_name} 移除身分組：{role.name}！")

@bot.slash_command(name="role_create", description="在伺服器中創建一個新的身分組")
async def createrole(inter, role_name: str = disnake.Option(name="role_name", description="新的身分組名稱", type=OptionType.string)):
    await inter.guild.create_role(name=role_name)
    await inter.response.send_message(f"已創建身分組：{role_name}！")

@bot.slash_command(name="role_delete", description="刪除指定的身分組")
async def deleterole(inter, role: disnake.Role = disnake.Option(name="role", description="選擇一個要刪除的身分組", type=OptionType.role)):
    await role.delete()
    await inter.response.send_message(f"已刪除身分組：{role.name}！")

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
