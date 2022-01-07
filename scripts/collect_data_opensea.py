from request_from_opensea import response_as_json
import pandas as pd
from tqdm import tqdm
pd.set_option('display.max_colwidth', 100)

# https://www.coingecko.com/en/nft/mutant-ape-yacht-club
NO_ASSETS_IN_COLLECTION = 14653

# Create Pandas Dataframe
columns = ["id",
           "token_id", 
           "asset_contract_address", 
           "permalink", 
           "traits", 
           "image_original_url",
           "created_date", 
           "current_price", 
           "last_sale_total_price", 
           "last_sale_event_timestamp"]
df = pd.DataFrame(columns=columns)


# Data Collection

for i in tqdm(range(NO_ASSETS_IN_COLLECTION-1)):
    
    response = response_as_json('assets', i)
    
    # If entry has an empty response, skip. Else, collect data.
    if response['assets']==[]:
        continue
    else:
        response_base = response['assets'][0]

        # Custom logic for current_price
        if response_base['sell_orders'] is None:
            current_price='Not on sale. Taking offers.'
        else:
            current_price=int(float(response_base['sell_orders'][0]['current_price']))/1000000000000000000

        # Custom logic for last_sale_total_price & last_sale_event_timestamp
        if response_base['last_sale'] is None:
            last_sale_total_price='Not available.'
            last_sale_event_timestamp='Not available.'
        else:
            last_sale_total_price=int(response_base['last_sale']['total_price'])/1000000000000000000
            last_sale_event_timestamp=response_base['last_sale']['event_timestamp']

        df = df.append({
            "id":response_base['id'], 
            "token_id":response_base['token_id'],
            "asset_contract_address":response_base['asset_contract']['address'], 
            "permalink":response_base['permalink'], 
            "traits":response_base['traits'], 
            "image_original_url":response_base['image_original_url'],
            "created_date":response_base['collection']['created_date'], 
            "current_price":current_price, 
            "last_sale_total_price":last_sale_total_price, 
            "last_sale_event_timestamp":last_sale_event_timestamp
        }, ignore_index=True)



df.to_csv('./data/mutant-ape-collection.csv')

x