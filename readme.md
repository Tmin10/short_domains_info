# Registered and free 1-3 chars domains info for COM, NET and ORG

This dataset contains set of csv files with information of registered and free domains in COM, NET and ORG TLDs for 1-3 char name lenths. 

In the [tools](tools) folder you can find two python scripts:
* `whois_test.py` - get whois information and put it into sqlite database;
* `whois_info.py` - create CSVs from database and update this readme file.

## Please note:
1. This dataset is incomplete and could be outdated. It's possible that I'll update it in the future;
2. Part of 'free' domains could be reserved and unavailable for a registration (e.g. i.com, vc.org). To get the latest information please check the domains in whois service.

## Datasets summary:

| Length | COM | NET | ORG | 
|---|---|---|---|
| 1 | Registered: [3](csv_registered/com_1.csv) |Registered: [2](csv_registered/net_1.csv) |Registered: [33](csv_registered/org_1.csv) |
| | Free: [33](csv_free/com_1.csv) |Free: [34](csv_free/net_1.csv) |Free: [0](csv_free/org_1.csv) |
| 2 | Registered: [1242](csv_registered/com_2.csv) |Registered: [1164](csv_registered/net_2.csv) |Registered: [1222](csv_registered/org_2.csv) |
| | Free: [1](csv_free/com_2.csv) |Free: [7](csv_free/net_2.csv) |Free: [74](csv_free/org_2.csv) |
| 3 | Registered: [46561](csv_registered/com_3.csv) |Registered: [45509](csv_registered/net_3.csv) |Registered: [25043](csv_registered/org_3.csv) |
| | Free: [1](csv_free/com_3.csv) |Free: [1088](csv_free/net_3.csv) |Free: [8882](csv_free/org_3.csv) |
