import itertools
import random
import sys
from multiprocessing.dummy import Pool as ThreadPool

import whois
import sqlite3

SYMBOLS = [
    "q",
    "w",
    "e",
    "r",
    "t",
    "y",
    "u",
    "i",
    "o",
    "p",
    "a",
    "s",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "z",
    "x",
    "c",
    "v",
    "b",
    "n",
    "m",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "-",
]

TLDS = ["com", "net", "org"]

DOMAINS = sqlite3.connect("domains.db")

LENGTHS = range(1, 4)

POOL = ThreadPool(20)

ERROR = 1
OK = 2
FREE = 3


def main():
    setup(DOMAINS)
    for domain_length in LENGTHS:
        domains = list(itertools.product(SYMBOLS, repeat=domain_length))
        random.shuffle(domains)
        domains_pool = []
        for domain in domains:
            domain_name = "".join(domain)
            for tld in TLDS:
                if is_valid_domain(domain_name) and is_new_name(
                    domain_name, tld, DOMAINS
                ):
                    if len(domains_pool) < 1000:
                        domains_pool.append((domain, tld))
                    else:
                        results = POOL.map(get_whois, domains_pool)
                        domains_pool = []
                        for result in results:
                            actions = {
                                ERROR: lambda res: print(
                                    "Checking {}.{}\tERROR".format(
                                        "".join(res[2][0]), res[2][1]
                                    )
                                ),
                                OK: lambda res: add_to_db(
                                    res[1], "".join(res[2][0]), res[2][1], DOMAINS
                                ),
                                FREE: lambda res: add_to_db(
                                    None, "".join(res[2][0]), res[2][1], DOMAINS
                                ),
                            }
                            actions[result[0]](result)


def is_valid_domain(domain_name):
    if domain_name.startswith("-") or domain_name.endswith("-"):
        return False
    return True


def get_whois(domain):
    domain_name = "{}.{}".format("".join(domain[0]), domain[1])
    try:
        query_result = whois.query(domain_name)
        print(".", end="")
        sys.stdout.flush()
        if query_result:
            return OK, query_result, domain
        else:
            return FREE, None, domain
    except:
        return ERROR, None, domain


def setup(db):
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS domains ("
        "name TEXT NOT NULL,"
        "tld TEXT NOT NULL,"
        "registrar TEXT,"
        "creation_date INTEGER,"
        "expiration_date INTEGER,"
        "last_updated INTEGER,"
        "status TEXT,"
        "name_servers TEXT,"
        "PRIMARY KEY (name, tld)"
        ")"
    )
    db.commit()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS free_domains ("
        "name TEXT NOT NULL,"
        "tld TEXT NOT NULL,"
        "PRIMARY KEY (name, tld)"
        ")"
    )
    db.commit()


def is_new_name(name, tld, db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT "
        "(SELECT COUNT(name) FROM domains WHERE name = '{0}' AND tld = '{1}') + "
        "(SELECT COUNT(name) FROM free_domains WHERE name = '{0}' AND tld = '{1}')".format(
            name, tld
        )
    )
    if cursor.fetchone()[0] == 0:
        return True
    return False


def add_to_db(whois_info, name, tld, db):
    cursor = db.cursor()
    query = "INSERT INTO free_domains VALUES ('{}', '{}')".format(name, tld)
    if whois_info:
        print("Checking {}.{}\tOK\t{}".format(name, tld, whois_info.registrar))
        query = "INSERT INTO domains VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            name,
            tld,
            whois_info.registrar.replace("'", '"'),
            time_or_null(whois_info, "creation_date"),
            time_or_null(whois_info, "expiration_date"),
            time_or_null(whois_info, "last_update"),
            whois_info.status,
            str(whois_info.name_servers).replace("'", '"'),
        )
    else:
        print("Checking {}.{}\tFREE".format(name, tld))
    cursor.execute(query)
    db.commit()


def time_or_null(whois_info, value):
    if getattr(whois_info, value, None):
        return int(getattr(whois_info, value).timestamp())
    return "NULL"


if __name__ == "__main__":
    main()
