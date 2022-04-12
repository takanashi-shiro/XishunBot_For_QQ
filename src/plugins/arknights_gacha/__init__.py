import nonebot
from nonebot import get_driver
from .config import Config

try:
    nonebot.get_driver()
    from . import arknights_gacha
    from . import gacha
except ValueError:
    pass

# global_config = get_driver().config
# config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
