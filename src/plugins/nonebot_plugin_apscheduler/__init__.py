import logging

from nonebot import export, get_driver
from nonebot.log import LoguruHandler, logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import Config

driver = get_driver()
global_config = driver.config
plugin_config = Config(**global_config.dict())

scheduler = AsyncIOScheduler()
scheduler.configure(plugin_config.apscheduler_config)
export().scheduler = scheduler


async def _start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.opt(colors=True).info("<y>Scheduler Started</y>")


if plugin_config.apscheduler_autostart:
    driver.on_startup(_start_scheduler)

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(plugin_config.apscheduler_log_level)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())
