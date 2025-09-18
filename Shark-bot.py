import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

TOKEN = 'Discord_bot_token'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')  # Удаляем встроенную команду .help до регистрации

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов к работе!')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int = 60):
    try:
        timeout_until = datetime.now(tz=timezone.utc) + timedelta(minutes=duration)
        await member.timeout(timeout_until, reason='Мут от модера')
        await ctx.send(f'{member.mention} замучен на {duration} минут!')
    except discord.Forbidden:
        await ctx.send('Нет прав для мута!')
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None, reason='Снятие мута')
        await ctx.send(f'{member.mention} размучен!')
    except discord.Forbidden:
        await ctx.send('Нет прав для снятия мута!')
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = 'Бан от модера'):
    try:
        await member.ban(reason=reason, delete_message_days=0)
        await ctx.send(f'{member.mention} забанен! Причина: {reason}')
    except discord.Forbidden:
        await ctx.send('Нет прав для бана!')
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
    try:
        await ctx.guild.unban(user, reason='Снятие бана')
        await ctx.send(f'{user.mention} разбанен!')
    except discord.Forbidden:
        await ctx.send('Нет прав для снятия бана!')
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def newban(ctx, member: discord.Member):
    try:
        account_age = (datetime.now(tz=timezone.utc) - member.created_at).days
        if account_age < 14:
            await member.ban(reason='Аккаунт младше 14 дней!', delete_message_days=0)
            await ctx.send(f'{member.mention} забанен! Аккаунт младше 14 дней.')
        else:
            await ctx.send(f'{member.mention} слишком стар для .newban!')
    except discord.Forbidden:
        await ctx.send('Нет прав для бана!')
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')

@bot.command()
async def help(ctx):
    help_text = """
**Команды бота:**
`.mute @пользователь [минуты]` - Замутить пользователя (по умолчанию 60 минут).
`.unmute @пользователь` - Снять мут с пользователя.
`.ban @пользователь [причина]` - Забанить пользователя.
`.unban @пользователь` - Снять бан с пользователя.
`.newban @пользователь` - Забанить пользователя, если его аккаунт младше 14 дней.
"""
    await ctx.send(help_text)

bot.run(TOKEN)
