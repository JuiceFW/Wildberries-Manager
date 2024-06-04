import pandas as pd

from logging import getLogger


logger = getLogger(__name__)


class Excel:
    def __init__(self):
        self.name = "results.xlsx"


    def write_data(self, data: dict[list]):
        logger.debug(f"Writing {self.name}")

        frame = pd.DataFrame(data)
        frame.to_excel(self.name, sheet_name="Sheet1", index=False, index_label=False)

