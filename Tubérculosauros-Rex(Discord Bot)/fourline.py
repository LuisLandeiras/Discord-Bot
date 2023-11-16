import discord, random
from discord.ext import commands

player1 = ""
player2 = ""
turn = ""
board = []
GameProgress = True

async def fourline_command(ctx, p1: discord.Member, p2: discord.Member):
    global player1
    global player2
    global turn
    global GameProgress
    global count
    
    if GameProgress:
        global board
        board = [[":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"],
                 [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"],
                 [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"],
                 [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"],
                 [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"],
                 [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"]]
        
        turn = ""
        GameProgress = False
        count = 0
        
        player1 = p1
        player2 = p2
        
        # print do tabuleiro            
        line = ""
        for row in board:
            for column in row:
                line += column + " "
            await ctx.send(line)
            line = ""

        num = random.randint(0,1)
        if num == 0:
            turn = player1
            await ctx.send("Turno do jogador: " + str(player1.display_name))
        elif num == 1:
            turn = player2
            await ctx.send("Turno do jogador: " + str(player2.display_name))
    else:
        await ctx.send("Acabe o jogo que está em progesso antes de iniciar um novo.")
        
async def play_command(ctx, pos: int):
    global turn 
    global player1
    global player2
    global board
    global count
    
    if not GameProgress:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":red_circle:"
            elif turn == player2:
                mark = ":green_circle:"
            if 0 < pos < 8:
                row_to_place = None
                for row_index in range(5, -1, -1):
                    if board[row_index][pos - 1] == ":white_large_square:":
                        row_to_place = row_index
                        break
                    
                if row_to_place is not None:
                    board[row_to_place][pos - 1] = mark
                else:
                    await ctx.send("A coluna está cheia escolhe outra corno.")
                    
                line = ""
                for row in board:
                    for column in row:
                        line += column + " "
                    await ctx.send(line)
                    line = ""
                
                Check4LineWin(board, mark)
                if count >= 42:
                    await ctx.send("Empate!") 
                elif GameProgress:
                    await ctx.send(str(turn.display_name) + " Ganhou!")
                    count = 42
                    
                #Trocar de jogador
                if turn == player1:
                    turn = player2
                    if count < 42:
                        await ctx.send("Turno do jogador: " + turn.display_name)    
                elif turn == player2:
                    turn = player1
                    if count < 42:
                        await ctx.send("Turno do jogador: " + turn.display_name) 
            else:
                await ctx.send("Escolha um número entre 1-7 e um lugar não ocupado. Ou és burro?")
        else:
            await ctx.send("Não é o teu turno filho da puta.")
            
def Check4LineWin(board, mark):
    global GameProgress
    N = len(board)
    M = len(board[0])
    
    #Horizontal
    for i in range(N):
        for j in range(M - 3):
            if board[i][j] == mark and board[i][j + 1] == mark and board[i][j + 2] == mark and board[i][j + 3] == mark:
                GameProgress = True
    
    #Vertical
    for i in range(N - 3):
        for j in range(M):
            if board[i][j] == mark and board[i + 1][j] == mark and board[i + 2][j] == mark and board[i + 3][j] == mark:
                GameProgress = True
    
    #Obliquo bot-esquerda para top-direita
    for i in range(N - 3):
        
        for j in range(M - 3):
            if board[i][j] == mark and board[i + 1][j + 1] == mark and board[i + 2][j + 2] == mark and board[i + 3][j + 3] == mark:
                GameProgress = True
    
    #Obliquo top-esquerda para bot-direita
    for i in range(3, N):
        for j in range(M - 3):
            if board[i][j] == mark and board[i - 1][j + 1] == mark and board[i - 2][j + 2] == mark and board[i - 3][j + 3] == mark:
                GameProgress = True        
     
@commands.command()
async def fourline(ctx, p1: discord.Member, p2: discord.Member):
    await fourline_command(ctx, p1, p2)

@commands.command()
async def column(ctx, pos: int):
    await play_command(ctx, pos)     
                
@fourline.error
async def fourline_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Tem de haver 2 jogadores diferentes para ser possível jogar burro do caralho.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Tem de estar tudo certo burro do caralho.")
        
@column.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Coloca a merda da posição que queres jogar.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("És burro? Coloca um número caralho.")