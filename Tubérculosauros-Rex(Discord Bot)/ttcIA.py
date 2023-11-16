import discord, random
from discord.ext import commands
import copy

# ------------------------------------------------------------------
async def mostra_tabuleiro(ctx, T):
    print(T[0:3])
    print(T[3:6])
    print(T[6:9])
    await ctx.send(T[0:3])
    await ctx.send(T[3:6])
    await ctx.send(T[6:9])
    

# ------------------------------------------------------------------
# devolve a lista de ações que se podem executar partido de um estado
def acoes(T):
    Lista_acoes = []
    for i in range(0,9):
        if T[i] == 0:
            Lista_acoes.append(i)
    
    return Lista_acoes
            
# ------------------------------------------------------------------
# devolve o estado que resulta de partir de um estado e executar uma ação Check
def resultado(T,a,jog):
    aux = copy.copy(T)
    aux[a] = jog
    return aux

# ------------------------------------------------------------------
# existem 8 possíveis alinhamentos vencedores, para cada jogador
WinCondicion = ([-1,-1,-1],[1,1,1])
def utilidade(T):
    if T[0:9:4] in WinCondicion or T[2:7:2] in WinCondicion:    	return T[4]
    for i in range(0,3):
        if T[0+i*3:3+i*3] in WinCondicion:                          return T[0+i*3]
        if T[0+i:7+i:3] in WinCondicion:                            return T[0+i]
    return 0

# ------------------------------------------------------------------
# devolve True se T é terminal, senão devolve False
def estado_terminal(T):
    return True if not(0 in T) or utilidade(T) != 0 else False

# ------------------------------------------------------------------
# algoritmo da wikipedia
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
# ignoramos a profundidade e devolvemos o valor, a ação e o estado resultante
def alfabeta(T,alfa,beta,jog):
    if estado_terminal(T):
        return utilidade(T),-1,-1
    if jog:
        v = -10
        ba = -1
        for a in acoes(T):
            v1,ac,es = alfabeta(resultado(T,a,1),alfa,beta,False)
            if v1 > v: # guardo a ação que corresponde ao melhor
                v = v1
                ba = a
            alfa = max(alfa,v)
            if v >= beta:
                break
        return v,ba,resultado(T,ba,1)
    else:
        v = 10
        ba = 1
        for a in acoes(T):
            v1,ac,es = alfabeta(resultado(T,a,-1),alfa,beta,True)
            if v1 < v:
                v = v1
                ba = a
            beta = min(beta,v)
            if v <= alfa:
                break
        return v,ba,resultado(T,ba,-1)

# ------------------------------------------------------------------
def joga_max(T):
    v,a,e = alfabeta(T,-10,10,True)
    print ('MAX joga para ',a)
    return e

# ------------------------------------------------------------------
def joga_min(T):
    v,a,e = alfabeta(T,-10,10,False)
    print('MIN joga para ', a)
    return e

# ------------------------------------------------------------------
def posicao(pos):
    pos = int(input())
    return pos

def joga(T, pos):
    print("Escolha um posição:")
    T[pos] = -1
    return T
    
# ------------------------------------------------------------------
def jogo(ctx, p1: discord.Member, p2):
    # cria tabuleiro vazio
    T = [0,0,0,0,0,0,0,0,0]
    while acoes(T) != [] and not estado_terminal(T):
        T = p1(T)
        mostra_tabuleiro(ctx, T)
        if acoes(T) != [] and not estado_terminal(T):
            T = p2(T)
            mostra_tabuleiro(ctx, T)

    # fim
    if utilidade(T) == 1:
        print ('Venceu o jog1')
    elif utilidade(T) == -1:
        print ('Venceu o jog2')
    else:
        print ('Empate')

# ------------------------------------------------------------------

@commands.command()
async def jogo(ctx, p1: discord.Member, p2: list):
    await jogo(ctx, p1, joga)
    
@commands.command()
async def place(ctx, pos: int):
    await posicao(ctx, pos)
    

