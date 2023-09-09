import json
import disnake
from disnake import Embed
from disnake.ext import commands
from disnake import OptionType
from disnake import ButtonStyle, ActionRow, Button
from disnake import TextInputStyle
from disnake.ext.commands import has_permissions


@commands.slash_command(name="role", description="關於身分組的主命令")
@has_permissions(administrator=True)
async def role(inter):
    pass

@role.sub_command(description="創建一個自定義身分組按鈕")
async def create_role_button(inter, title: str, description: str,  role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱")):
    class RoleButton(disnake.ui.Button):
        def __init__(self, role_id):
            super().__init__(style=disnake.ButtonStyle.primary, label=f"點擊以獲得身分組")
            self.role_id = role_id

        async def callback(self, inter: disnake.Interaction):
            role = disnake.utils.get(inter.guild.roles, id=self.role_id)
            if role:
                await inter.user.add_roles(role)
                await inter.response.send_message(f"你已獲得 '{role.name}' 身分組!")
            else:
                await inter.response.send_message(f"找不到為 '{self.role_id}' 的身分組")

    role_button = RoleButton(role)
    
    embed = disnake.Embed(title=title, description=description, color=0x91fcff)
    
    view = disnake.ui.View()
    view.add_item(role_button)
    
    await inter.response.send_message(embed=embed, view=view)



@role.sub_command(name="auto", description="設定新成員自動獲得的身分組")
async def role_auto(inter, role: disnake.Role = disnake.Option(name="role", description="新的身分組名稱", type=OptionType.role)):
    # 使用 set_auto_role 函數來設定自動身分組
    await set_auto_role(inter, role=role)

async def set_auto_role(ctx, *, role: disnake.Role):
    # 首先將角色資訊儲存到 JSON
    with open("auto_roles.json", "r") as file:
        data = json.load(file)

    data[str(ctx.guild.id)] = str(role.id)  # 儲存身分組ID為字串格式

    with open("auto_roles.json", "w") as file:
        json.dump(data, file, indent=4)

    await ctx.response.send_message(f"新成員現在將自動獲得 {role.name} 身分組！")

@commands.Cog.listener()
async def on_member_join(self, member):
    # 當新成員加入時，從 JSON 獲取身分組資訊並賦予身分組
    with open("auto_roles.json", "r") as file:
        data = json.load(file)

    role_id = data.get(str(member.guild.id))
    if role_id:
        role = disnake.utils.get(member.guild.roles, id=int(role_id))  # 使用 int 將身分組ID從字串轉為整數
        if role:
            await member.add_roles(role)

@role.sub_command(name="nuke", description="移除所有成員的指定身分組")
async def role_nuke(inter, role: disnake.Role = disnake.Option(name="role", description="要移除的身分組名稱", type=OptionType.role)):
    await inter.response.defer()
    members_to_update = [m for m in inter.guild.members if role in m.roles]
    total_members = len(members_to_update)
    errors = []

    embed = Embed(title="清除身分組", description=f"開始更新成員身分組... (0/{total_members})", color=0x91fcff)
    progress_message = await inter.followup.send(embed=embed)

    for index, member in enumerate(members_to_update):
        try:
            await member.remove_roles(role)
        except disnake.Forbidden:
            errors.append(f"沒有權限為 {member.display_name} 移除身分組!")
        except Exception as e:
            errors.append(f"為 {member.display_name} 移除身分組時出錯: {e}")

        if index % 10 == 0:
            embed.description = f"更新進度: 已處理 {index}/{total_members} 成員"
            await progress_message.edit(embed=embed)

    embed.description = f"所有成員的更新已完成，已從所選成員移除身分組：{role}！"
    if errors:
        embed.add_field(name="錯誤", value="\n".join(errors), inline=False)
    await progress_message.edit(embed=embed)


@role.sub_command(name="give_everyone", description="給予所有成員指定的身分組")
async def role_give_everyone(inter, role: disnake.Role = disnake.Option(name="role", description="要給予的身分組名稱")):
    await inter.response.defer()
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
    total_members = len(members)
    errors = []

    embed = Embed(title="身分組更新", description=f"開始更新成員身分組... (0/{total_members})", color=0x91fcff)
    progress_message = await inter.followup.send(embed=embed)

    for index, member in enumerate(members):
        try:
            await member.add_roles(role)
        except disnake.Forbidden:
            errors.append(f"沒有權限為 {member.display_name} 增加身分組!")
        except Exception as e:
            errors.append(f"為 {member.display_name} 增加身分組時出錯: {e}")

        if index % 1 == 0:
            embed.description = f"更新進度: 已處理 {index}/{total_members} 成員"
            await progress_message.edit(embed=embed)

    embed.description = f"所有成員的更新已完成，已給予所選成員身分組：{role}！"
    if errors:
        embed.add_field(name="錯誤", value="\n".join(errors), inline=False)
    await progress_message.edit(embed=embed)

@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("警告: 您沒有使用此命令的權限!")

def setup(bot):
    bot.add_slash_command(role)
    
