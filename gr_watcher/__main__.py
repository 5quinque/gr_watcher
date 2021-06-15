#!/usr/bin/env python

import os
import logging
from prometheus_client import start_http_server, Gauge
import time


from .watcher import Watcher


def main():
    list = os.environ.get("GR_LIST")

    if list is None:
        exit("Provide a list with `export GR_LIST=<GoodReads List URL>`")

    # Start up the server to expose the metrics.
    start_http_server(5000, addr="0.0.0.0")

    watcher = Watcher(list)

    while True:
        watcher.get_books()
        watcher.get_prices()
        watcher.output_prices()

        time.sleep(3000)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler("gr_watcher.log"), logging.StreamHandler()],
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main()
