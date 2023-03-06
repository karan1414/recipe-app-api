# # open, high, low, ltp

# import requests
# from bs4 import BeautifulSoup

# nse_url = "https://www1.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm"


# resp = requests.get(nse_url)

# soup = BeautifulSoup(resp.content, 'lxml')

# table_soup = soup.find("table", attrs={"id": "dataTable"})
# if not table_soup:
#     print("Table not found")

# tbody_soup = table_soup.find("tbody")
# if not tbody_soup: 
#     print("Tbody not found")

# tr_soup = tbody_soup.find_all("tr")
# result_data = []
# company_data = {}
# for tr in tr_soup[1:]:
#     tds_soup = tr.find_all("td")
#     if not tds_soup[0] or not tds_soup[0].get_text():
#         print("symbol name not found")
#         continue
#     company_data["symbol"] = tds_soup[0].get_text().strip()
#     company_data["ca"] = tds_soup[1].get_text().strip() if tds_soup[1] and tds_soup[1].get_text() else None

#     print(company_data) 
#     result_data.append(company_data)


# print("final data===>")
# print(result_data)


new_str = "aaabbcccd"
result = {}

for i in new_str:
    if i not in result.keys():
        result[i] = 0
    # if i in result.keys():
    result[i] = result[i] + 1
print(result)
