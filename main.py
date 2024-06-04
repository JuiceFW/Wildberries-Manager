from config import logging_format

from logging import getLogger, basicConfig
from logging import FileHandler, Formatter
from logging import INFO
import traceback
import os

from dotenv import load_dotenv

from src.wildberries.api import WildberriesApi
from src.excel.excel import Excel


load_dotenv()


logger = getLogger()
basicConfig(
    level=INFO,
    format=logging_format
)
fh = FileHandler(
    "logs.log",
    encoding='utf-8'
)
fh.setFormatter(Formatter(logging_format))
logger.addHandler(fh)


try:
    WildberriesApi = WildberriesApi()
    Excel = Excel()
except:
    logger.critical(traceback.format_exc())
    os._exit(0)


def main():
    warehouses = WildberriesApi.get_warehouses()
    if not warehouses:
        logger.info("No warehouses found! Closing program...")
        return

    warehouses_ids = []
    warehouses_dict = {}

    for warehouse in warehouses:
        warehouses_ids.append(warehouse.get("officeId"))

        warehouses_dict[str(warehouse.get("officeId"))] = warehouse.get("name")

    warehouses.clear()


    stocks = WildberriesApi.get_stocks(warehouses_ids)
    data = {
        "Sku": [],
        "Amount": [],
        "Warehouse Name": [],
        "Warehouse Id": []
    }

    for warehouseId, stock in stocks.items():
        data["Sku"].append(stock.get("sku"))
        data["Amount"].append(stock.get("amount"))
        data["Warehouse Name"].append(warehouses_dict.get(warehouseId).get("name"))
        data["Warehouse Name"].append(warehouses_dict.get(int(warehouseId)).get("officeId"))

    Excel.write_data(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Closing program...")
    except:
        logger.critical(traceback.format_exc())
