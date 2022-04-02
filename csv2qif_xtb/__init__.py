import csv
from csv2qif.core import Transaction
import datetime

__mapping = {
    'what': 1,
    'date': 2,
    'price': 5,
    'recipient': 3,
    'desc': 4,
}


class dialect(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


def row_converter(csv_row) -> Transaction:
    recipient = csv_row[__mapping['recipient']]
    desc = csv_row[__mapping['what']] + ' - ' + csv_row[__mapping['desc']]
    return Transaction(
        date=__get_date(csv_row),
        price=__get_price(csv_row),
        recipient=recipient,
        desc=desc
    )


def row_filter(csv_row) -> bool:
    try:
        __get_price(csv_row)
        __get_date(csv_row)
    except (IndexError, ValueError):
        return False
    else:
        return True


def __get_price(csv_row) -> float:
    price = csv_row[__mapping['price']]
    return float(price)


def __get_date(csv_row) -> datetime.datetime:
    return datetime.datetime.strptime(csv_row[__mapping['date']], '%d.%m.%Y %H:%M:%S')
