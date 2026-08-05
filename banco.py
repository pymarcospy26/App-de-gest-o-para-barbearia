import sqlite3
import asyncio
from pathlib import Path

BANCO = Path(__file__).resolve().parent
BANCO = BANCO / 'banco.db'

def servico_valor_base():
    con = sqlite3.connect(BANCO)
    cursor = con.cursor()

    cursor.execute('''SELECT setor, servico, valor FROM catalogo''')

    resultados_s_v = cursor.fetchall()
    con.close()

    return resultados_s_v

async def servico_valor():
    return await asyncio.to_thread(servico_valor_base)

def setores_base():
    con = sqlite3.connect(BANCO)
    cursor = con.cursor()

    cursor.execute('''SELECT DISTINCT setor FROM catalogo''')

    resultados_set = cursor.fetchall()
    con.close()

    return [setor[0] for setor in resultados_set]

async def setores():
    return await asyncio.to_thread(setores_base)