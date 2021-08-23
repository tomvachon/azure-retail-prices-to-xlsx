
#External Dependancies
import pandas as pd
import requests, openpyxl

#Build in Dependancies 
import json, tempfile, os
from datetime import datetime


def do_request(rs, price_uri, page=0):
    
    r = rs.get(price_uri)
    json_resp = r.json()

    next_page_uri = json_resp['NextPageLink']
    price_resp = json_resp['Items']

    return price_resp, next_page_uri


def merge_prices(price_list, price_resp):
    
    for price in price_resp:
        price_list.append(price)
        
    return price_list

def convert_xls(price_list):
    dir_name = "AzurePrices"
    try:
        os.mkdir(f"./{dir_name}")
    except OSError as e:
        print("Directory exists")
    
    now = datetime.now()
    file_name = now.strftime("%Y%m%d-%H%M")
    df_json=pd.read_json(json.dumps(price_list))

    full_file_path = f"./{dir_name}/{file_name}.xlsx"
    df_json.to_excel(full_file_path)

    return full_file_path

def main():
    price_uri = "https://prices.azure.com/api/retail/prices"
    rs = requests.Session()
    price_list = []


    #Initial call
    price_resp, next_page_uri = do_request(rs=rs, price_uri=price_uri)
    merge_prices(price_list=price_list, price_resp=price_resp)

    #Loop through until next page isn't set
    while next_page_uri:
        price_resp, next_page_uri = do_request(rs=rs, price_uri=next_page_uri)
        merge_prices(price_list=price_list, price_resp=price_resp)

    xls_file_path = convert_xls(price_list=price_list)
    print(xls_file_path)

if __name__ == "__main__":
    main()
