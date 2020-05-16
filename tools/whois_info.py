import sqlite3
import csv
from pathlib import Path

DOMAINS = sqlite3.connect("domains.db")

TLDS = ["com", "net", "org"]
TLD_LENGTHS = [1, 2, 3]
CSV_HEADER = [
    "domain",
    "registrar",
    "creation_date",
    "expiration_date",
    "status",
    "name_servers",
]
CSV_HEADER_FREE = ["domain"]
CSV_FOLDER = "../csv_registered"
CSV_FOLDER_FREE = "../csv_free"


def main():
    Path(CSV_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(CSV_FOLDER_FREE).mkdir(parents=True, exist_ok=True)
    cursor = DOMAINS.cursor()
    result_table = {}
    for tld in TLDS:
        result_table[tld] = {}
        for tld_length in TLD_LENGTHS:
            registered_count = write_csv(
                CSV_FOLDER,
                tld,
                tld_length,
                cursor,
                CSV_HEADER,
                "domains",
                (
                    ", registrar, "
                    "creation_date, "
                    "expiration_date, "
                    "status, "
                    "name_servers "
                ),
            )
            free_count = write_csv(
                CSV_FOLDER_FREE,
                tld,
                tld_length,
                cursor,
                CSV_HEADER_FREE,
                "free_domains",
            )
            result_table[tld][tld_length] = {
                "registered": registered_count,
                "free": free_count,
                "tld": tld,
                "tld_length": tld_length,
            }
    create_readme(result_table)


def create_readme(table):
    with open("../readme.md", "w") as readme_file:
        readme_file.write(
            "# Registered and free 1-3 chars domains info for COM, NET and ORG\n\n"
            "This dataset contains set of csv files with information of registered and free domains in COM, NET and ORG TLDs for 1-3 char name lenths. \n\n"
            "In the [tools](tree/master/tools) folder you can find two python scripts:\n"
            "* `whois_test.py` - get whois information and put it into sqlite database;\n"
            "* `whois_info.py` - create CSVs from database and update this readme file.\n"
            "## Please note:\n"
            "1. This dataset is incomplete and could be outdated. It's possible that I'll update it in the future;\n"
            "2. Part of 'free' domains could be reserved and unavailable for a registration (e.g. i.com, vc.org). To get the latest information please check the domains in whois service.\n"
            "##Datasets summary:\n"
        )
        header = "\n| Length | "
        table_delimiter = "|---|"
        for tld in table.keys():
            header += tld.upper() + " | "
            table_delimiter += "---|"
        readme_file.write(header + "\n")
        readme_file.write(table_delimiter + "\n")
        lengths = table[list(table)[0]].keys()
        for tld_length in lengths:
            registered_row = "| {} | ".format(tld_length)
            free_row = "| | "
            for tld in table.keys():
                registered_row += "Registered: [{registered}](blob/master/csv_registered/{tld}_{tld_length}.csv) |".format(
                    **table[tld][tld_length]
                )
                free_row += "Free: [{free}](blob/master/csv_free/{tld}_{tld_length}.csv) |".format(
                    **table[tld][tld_length]
                )
            readme_file.write(registered_row + "\n")
            readme_file.write(free_row + "\n")


def write_csv(folder, tld, tld_length, cursor, header, table, columns=""):
    with open(
        "{}/{}_{}.csv".format(folder, tld, tld_length), "w", newline=""
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        query = (
            "SELECT "
            " name || '.{tld}' as domain"
            " {columns} "
            "FROM {table} "
            "WHERE tld='{tld}' AND length(name) = {tld_length} "
            "ORDER BY domain".format(
                columns=columns, tld=tld, tld_length=tld_length, table=table
            )
        )
        cursor.execute(query)
        count = 0
        for row in cursor.fetchall():
            writer.writerow(row)
            count += 1
        return count


if __name__ == "__main__":
    main()
