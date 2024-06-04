from logging import getLogger
from typing import Union
import traceback
import time
import os

import requests

from src.exceptions.exceptions import TokenMissing


logger = getLogger(__name__)


class WildberriesApi:
    """ Класс для выполнения запросов к API Wilberries. """

    def __init__(self):
        self.main_url = "https://suppliers-api.wildberries.ru/"
        self.warehouses_url = self.main_url + "api/v3/warehouses"
        self.get_stocks_url = self.main_url + "api/v3/stocks/{warehouseId}"

        self.base_headers = {
            "Authorization": os.getenv("wildberries_api_token")
        }

        if not self.base_headers.get("Authorization"):
            raise TokenMissing


    def get_warehouses(self) -> list[dict]:
        """ Возвращает список складов продавца с их данными (складов).

            Returns: list[dict]
            Example:
            [
                {
                    "name": "ул. Троицкая, Подольск, Московская обл.",
                    "officeId": 15,
                    "id": 1,
                    "cargoType": 1,
                    "deliveryType": 1
                }
            ]
        """

        for i in range(3):
            try:
                response = requests.get(self.warehouses_url, headers=self.base_headers)

                if response.status_code != 200:
                    logger.debug(f"get_warehouses : status_code: {response.status_code}")
                    time.sleep(2)
                    continue
    
                response = response.json()
                return response

            except:
                logger.error(traceback.format_exc())
                time.sleep(2)


    def get_stocks(self, warehouses_ids: Union[list[int], int]) -> Union[dict[list[dict]], dict]:
        """ Возвращает остатки товаров со складов по данным складам. 
        
            Returns: dict[list[dict]]
            Example:
            {
                "warehouseId": [
                    {
                        "sku": "BarcodeTest123",
                        "amount": 10
                    }
                ]
            }
        """

        if isinstance(warehouses_ids, int):
            warehouses_ids = [warehouses_ids]

        stocks = {}

        for warehouse_id in warehouses_ids:
            for i in range(3):
                try:
                    response = requests.get(
                                            self.get_stocks_url.format(warehouseId=warehouse_id),
                                            headers=self.base_headers
                                        )

                    if response.status_code != 200:
                        logger.debug(f"get_warehouses : status_code: {response.status_code}")
                        time.sleep(2)
                        continue
        
                    response = response.json()

                    stocks[str(warehouse_id)] = response
                except:
                    logger.error(traceback.format_exc())
                    time.sleep(2)

        return stocks
