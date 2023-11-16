import discord, random
from discord.ext import commands

player1 = ""
player2 = ""
turn = ""
board = []
GameProgress = True
WinCondiction = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

async def tictactoe_command(ctx, p1: discord.Member, p2: discord.Member):
    global player1
    global player2
    global turn
    global GameProgress
    global count
    
    if GameProgress:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        GameProgress = False
        count = 0
        player1 = p1
        player2 = p2
        # print do tabuleiro
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line) 
                line = ""
            else:
                line += " " + board[x]
        num = random.randint(0,1)
        if num == 0:
            turn = player1
            await ctx.send("Turno do jogador: " + str(player1.display_name))
        elif num == 1:
            turn = player2
            await ctx.send("Turno do jogador: " + str(player2.display_name))
    else:
        await ctx.send("Acabe o jogo que está em progesso antes de iniciar um novo.")
        
async def place_command(ctx, pos: int):
    global turn 
    global player1
    global player2
    global board
    global count
    
    if not GameProgress:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":regional_indicator_o:"
            if 0 < pos < 10 and board[pos-1] == ":white_large_square:":
                board[pos-1] = mark
                count += 1
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line) 
                        line = ""
                    else:
                        line += " " + board[x]
                CheckWinner(WinCondiction, mark)
                if count >= 9:
                    await ctx.send("Empate!") 
                elif GameProgress:
                    await ctx.send(str(turn.display_name) + " Ganhou!")
                    count = 9
                #Trocar de jogador
                if turn == player1:
                    turn = player2
                    if count < 9:
                        await ctx.send("Turno do jogador: " + turn.display_name)    
                elif turn == player2:
                    turn = player1
                    if count < 9:
                        await ctx.send("Turno do jogador: " + turn.display_name) 
            else:
                await ctx.send("Escolha um número entre 1-9 e um lugar não ocupado.")
        else:
            await ctx.send("Não é o teu turno filho da puta.")

def CheckWinner(WinCondiction, mark):
    global GameProgress
    for condiction in WinCondiction:
        if board[condiction[0]] == mark and board[condiction[1]] == mark and board[condiction[2]] == mark:
            GameProgress = True
               
@commands.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    await tictactoe_command(ctx, p1, p2)

@commands.command()
async def place(ctx, pos: int):
    await place_command(ctx, pos)
    
@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Tem de haver 2 jogadores diferentes para ser possível jogar burro do caralho.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Tem de estar tudo certo burro do caralho.")
        
@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Coloca a merda da posição que queres jogar.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("És burro? Coloca um número caralho.")
        