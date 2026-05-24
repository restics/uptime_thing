import threading
import time
import requests
from db import CardRepository, Card
from logger import logger
from concurrent.futures import ThreadPoolExecutor

class CardService:
    def __init__(self, is_active : bool = True, delay = 10):

        self.is_active = is_active
        self.repository = CardRepository()
        self.delay = delay

        self.main_loop = threading.Thread(target=self.loop)
        self.main_loop.daemon = True
        self.main_loop.start()
        

    def loop(self):
        while self.is_active:
            
            logger.info('updating cards... (delay = %s)', self.delay)
            cards = self.repository.get_all_cards()

            logger.info('initializing theadpoolexecutor')
            with ThreadPoolExecutor(thread_name_prefix='pinger_executor') as executor:
                results = executor.map(self.ping, cards)
            
            logger.info('finished updating cards, writing to db...')
            for card in results:
                self.repository.update_card(card)
            logger.info('db write complete.')
            time.sleep(self.delay)


    def ping(self, card : Card):

        logger.info('pinging service %s', card.name)
        start = time.perf_counter()
        try:
            r= requests.get(card.url)
            if r.status_code >= 500:
                card.status = "DOWN"
            else:
                card.status = "UP"
        except requests.exceptions.RequestException:
            card.status = "DOWN"

        card.latency = int((time.perf_counter() - start) * 1000)
        logger.info('service ping for %s is %d', card.name, card.latency)
        logger.info('returned code: %s', r.status_code)

        

        

        return card
        

        