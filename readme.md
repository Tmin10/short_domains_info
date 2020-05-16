# Registered and free 1-3 chars domains info for COM, NET and ORG

This dataset contains set of csv files with information of registered and free domains in COM, NET and ORG TLDs for 1-3 char name lenths. 
In the [tools](tree/master/tools) folder you can find two python scripts:
* `whois_test.py` - get whois information and put it into sqlite database;
* `whois_info.py` - create CSVs from database and update this readme file.
## Please note:
1. This dataset is incomplete and could be outdated. It's possible that I'll update it in the future;
2. Part of 'free' domains could be reserved and unavailable for a registration (e.g. i.com, vc.org). To get the latest information please check the domains in whois service.
##Datasets summary:

| Length | COM | NET | ORG | 
|---|---|---|---|
| 1 | Registered: 3 |Registered: 2 |Registered: 33 |
| | Free: 33 |Free: 34 |Free: 0 |
| 2 | Registered: 1242 |Registered: 1164 |Registered: 1222 |
| | Free: 1 |Free: 7 |Free: 74 |
| 3 | Registered: 46561 |Registered: 45509 |Registered: 25043 |
| | Free: 1 |Free: 1088 |Free: 8882 |
