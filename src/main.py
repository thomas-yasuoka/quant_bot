"""
Docs:
https://www.mql5.com/en/docs/integration/python_metatrader5

Notas:
VSCode: se usar o virtualenvwrapper tem q mudar o path pra Envs/env_name/python.exe
        no workspace settings, dps q rodar a primeira vez entra no env

Gerais: ñ instala pylint, ele aponta erros aleatórios com o MetaTrader5
"""
import sys
import MetaTrader5 as mt5
import time
from multiprocessing import Process, Pool, Pipe

from passwords import *
from functions import *
from strategy import *
# from passwords_blank import *
def test(i, j):
    print(i, j)
def f(name):
    print('hello', name)

def logg(conn):
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    print(f'ACCOUNT INFO: {mt5.account_info()}') if log else sys.exit("Nope"); 
    conn.send("hello")

def woo():
    print("wooo")

def f(*symbols):
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    print(f'Log In successful: {mt5.account_info()}') if log else sys.exit("Nope"); 
    with Pool() as p:
        # p.starmap(vwap, [("PETR4",), ("CVCB3", )])
        p.map(vwap_reversion, [i for i in args])


if __name__ == "__main__":
    """
    dá pra inicializar e fazer o login dps se precisar:
    mt5.initialize()
    log = mt5.login(37130907, password=passw_test, server="MetaQuotes-Demo")"
    """
    # o log inicializa o programa e faz o login, ele retorna True se tiver sido bem sucedido e False se não
    # log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    # print(f'ACCOUNT INFO: {mt5.account_info()}') if log else sys.exit("Nope"); 

    # prints symbols in the mkt watch
    # symbols=mt5.symbols_get()
    # count=0
    # # printa alguns symbols que pega do metatrader
    # for s in symbols:
    #     count+=1
    #     print("{}. {}".format(count,s.name))
    #     if count==5: break
    
    """
    Essas funções estão comentadas pra não rodar elas sem querer
    """

    # função importada de functions.py que abre uma ordem de compra de 1 unidade
    # mt5.symbol_select("SMLS3F")
    # print(open_order("SMLS3F", "buy", 1))

    # esse pega a estratégia montada em strategy.py (que retorna uma lista de ações) e compra um de cada
    # for i in top_10_rets_last_month():
    #     try:
    #         mt5.symbol_select(i)
    #         p = Process(target=vwap_reversion, args=(i, 300))
    #         p.start()
    #         p.join()
    #         print(mt5.last_error())
    #     except Exception as e:
    #         print(i, e)

    # time.sleep(10)
    # ticker = input("SYMBOL: ")
    # vwap_reversion(ticker, 300)

    f("PETR4", "CVCB3")
    # sell_all()
