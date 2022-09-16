import nonebot
from nonebot import require
from fastapi import FastAPI
from config import *
from nonebot.adapters.onebot.v11 import Adapter as OneBot_V11_Adapter

nonebot.init()
app: FastAPI = nonebot.get_asgi()
nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")
driver = nonebot.get_driver()
driver.register_adapter(OneBot_V11_Adapter)
nonebot.load_builtin_plugins()



if __name__ == "__main__":
    nonebot.run(host=host, port=port)
