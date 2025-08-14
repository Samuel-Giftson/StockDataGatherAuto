import threading
from enum import Enum
from typing import Dict, Tuple
from webull import webull


class Status(Enum):
    SUCCESS = 200
    FAILURE = 201


class DataGather:
    __instance = None
    __initialized = False
    __lock = threading.Lock()

    def __new__(cls):
        """
        Thread-safe Singleton pattern.

        Ensures only one instance of this class exists across the program's lifetime.
        Useful for shared resources like configs, loggers, or data caches.

        Returns:
            DataGather: The single shared instance.
        """
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.__my_information: Dict[str, dict] = {}
            self.__status = Status.FAILURE
            self.__initialized = True

    def return_stocks_to_get_info(self) -> Tuple[str, ...]:
        """Returns the list of tickers to fetch."""
        return ("AAPL", "TSLA")

    def fetch_and_update(self) -> None:
        """
        Fetch stock information and update the internal cache.
        Does not clear existing data — overwrites only if ticker already exists.
        """
        try:
            my_stocks = self.return_stocks_to_get_info()
            my_obj = webull()
            fetched_data = {ticker: my_obj.get_ticker_info(ticker) for ticker in my_stocks}

            cleaned_data = self._clean_information(fetched_data)
            self.__my_information.update(cleaned_data)
            self.__status = Status.SUCCESS
        except Exception as e:
            print(f"[ERROR] Failed to fetch stock data: {e}")
            self.__status = Status.FAILURE

    def _clean_information(self, dirty_dict: Dict[str, dict]) -> Dict[str, dict]:
        """
        Placeholder for cleaning logic.
        For now, returns the dict unchanged.
        """
        return dirty_dict

    def get_information(self) -> Dict[str, dict]:
        """Returns the cached stock data."""
        return self.__my_information

    def get_status(self) -> Status:
        """Returns the current status of the last operation."""
        return self.__status
