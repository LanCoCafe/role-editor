import disnake
from disnake.ext import commands
from disnake import OptionType
from config import auto_role_name

@commands.slash_command(name="role", description="關於身分組的主命令")
async def role(inter):
    pass

@role.sub_command(name="auto", description="設定新成員自動獲得的身分組")
async def role_auto(inter, role: disnake.Role = disnake.Option(name="role", description="新的身分組名稱", type=OptionType.role)):
    global auto_role_name
    auto_role_name = role.name
    await inter.response.send_message(f"已設定新成員將自動獲得的身分組為 `{role.name}`！")

@role.sub_command(name="give_everyone", description="給予所有成員指定的身分組")
async def role_give_everyone(inter, role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱")):
    members_to_update = inter.guild.members
    await _give_roles_to_members(inter, members_to_update, role)

@role.sub_command(name="give_bot", description="給予所有機器人指定的身分組")
async def role_give_bot(inter, role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱")):
    members_to_update = [m for m in inter.guild.members if m.bot]
    await _give_roles_to_members(inter, members_to_update, role)

@role.sub_command(name="give_member", description="給予所有非機器人成員指定的身分組")
async def role_give_member(inter, role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱")):
    members_to_update = [m for m in inter.guild.members if not m.bot]
    await _give_roles_to_members(inter, members_to_update, role)

@role.sub_command(name="give_specify", description="給予特定身分組的成員指定的身分組")
async def role_give_specify(inter, role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱"), target_role: disnake.Role = disnake.Option(name="target_role", description="要給誰的身分組")):
    members_to_update = [m for m in inter.guild.members if target_role in m.roles]
    await _give_roles_to_members(inter, members_to_update, role)

@role.sub_command(name="give", description="給予使用者指定的身分組")
async def role_give(inter, user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"), role: disnake.Role = disnake.Option(name="role", description="身分組名稱")):
    member = await inter.guild.fetch_member(user.id)
    role_to_add = disnake.utils.get(inter.guild.roles, name=role.name)
    if role_to_add:
        await member.add_roles(role_to_add)
        await inter.response.send_message(f"已給予 {member.display_name} 身分組：{role_to_add.name}！")
    else:
        await inter.response.send_message(f"找不到指定的身分組！")

@role.sub_command(name="remove", description="移除使用者的指定身分組")
async def role_remove(inter, user: disnake.User = disnake.Option(name="user", description="選擇一位使用者"), role: disnake.Role = disnake.Option(name="role", description="選擇一個身分組", type=OptionType.role)):
    member = await inter.guild.fetch_member(user.id)
    await member.remove_roles(role)
    await inter.response.send_message(f"已從 {member.display_name} 移除身分組：{role.name}！")

@role.sub_command(name="create", description="在伺服器中創建一個新的身分組")
async def role_create(inter, role_name: str = disnake.Option(name="role_name", description="新的身分組名稱", type=OptionType.string)):
    await inter.guild.create_role(name=role_name)
    await inter.response.send_message(f"已創建身分組：{role_name}！")

@role.sub_command(name="delete", description="刪除指定的身分組")
async def role_delete(inter, role: disnake.Role = disnake.Option(name="role", description="選擇一個要刪除的身分組", type=OptionType.role)):
    await role.delete()
    await inter.response.send_message(f"已刪除身分組：{role.name}！")

async def _give_roles_to_members(inter, members, role):
    for member in members:
        try:
            await member.add_roles(role)
        except disnake.Forbidden:
            await inter.response.send_message(f"沒有權限為 {member.display_name} 增加身分組!")
            return
        except Exception as e:
            await inter.response.send_message(f"為 {member.display_name} 增加身分組時出錯: {e}")
            return
    await inter.response.send_message(f"已給予所選成員身分組：{role.name}！")

def setup(bot):
    bot.add_slash_command(role)
