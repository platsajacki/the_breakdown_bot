import logging as log
import sys

log.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=log.ERROR, stream=sys.stdout
)
handler: log.FileHandler = log.FileHandler('bot_log.log')
handler.setLevel(log.ERROR)
log.getLogger().addHandler(handler)
