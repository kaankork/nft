# # OpenSea NFT API
# https://docs.opensea.io/reference/api-overview

import json
import requests


filters_assets = {
    "owner":'',
    "token_ids":'1',
    "asset_contract_address":'',
    "asset_contract_addresses":'',
    "order_by":'',
    "order_direction":'',
    "offset":'',
    "limit":'',
    "collection":'mutant-ape-yacht-club'
}

filters_events = {
    "asset_contract_address":'',
    "collection_slug":'',
    "token_id":'',
    "account_address":'',
    "event_type":'',
    "only_opensea":'false',
    "auction_type":'',
    "offset":0,
    "limit":20,
    "occurred_before":'',
    "occurred_after":''
}

filters_collections = {
    "asset_owner":"",
    "offset":0,
    "limit":300
}

filters_bundles = {
    "on_sale":"",
    "owner":"",
    "asset_contract_address":"",
    "asset_contract_addresses":"",
    "token_ids":"",
    "limit":20,
    "offset":0    
}

filters_asset = {
    "asset_contract_address":"0x0239769a1adf4def9f07da824b80b9c4fcb59593",
    "token_id":"1"
}

filters_contract = {
    "asset_contract_address":"0x06012c8cf97bead5deae237070f9587f8e7a266d"
}

filters_collection = {
    "collection_slug":"mutant-ape-yacht-club"
}

filters_collection_stats = {
    "collection_slug":"toyboogers"
}

def prepare_assets_filter_dict(token_id):
    filters_assets = {
        "owner":'',
        "token_ids":token_id,
        "asset_contract_address":'',
        "asset_contract_addresses":'',
        "order_by":'',
        "order_direction":'',
        "offset":'',
        "limit":'',
        "collection":'mutant-ape-yacht-club'
    }
    return filters_assets

def response_as_json(selected_filter_type, token_id):
    # If filter value is not empty, add it to filter collection
    # filter collection is then used in url to make the query.
    filter_collection = ''
    
    if selected_filter_type=='assets':
        # filter_dict = filters_assets
        filter_dict = prepare_assets_filter_dict(token_id)
        
    elif selected_filter_type=='events':
        filter_dict = filters_events
    elif selected_filter_type=='collections':
        filter_dict = filters_collections
    elif selected_filter_type=='bundles':
        filter_dict = filters_bundles
    elif selected_filter_type=='asset':
        filter_dict = filters_asset
    elif selected_filter_type=='asset_contract':
        filter_dict = filters_contract
    elif selected_filter_type=='collection':
        filter_dict = filters_collection
    elif selected_filter_type=='collection_stats':
        filter_dict = filters_collection_stats
    
    for filter_name, filter_value in filter_dict.items():
        if filter_value != '':
            if selected_filter_type in ['asset', 'asset_contract', 'collection']:
                print('FRIENDLY WARNING!!!')
                print('Double check required fields in query parameters for {}'.format(selected_filter_type))
                filter_collection = filter_collection+'{}/'.format(filter_value)
            elif selected_filter_type == 'collection_stats':
                filter_collection = '{}'.format(filter_value)
            else:
                filter_collection = filter_collection+'{}={}&'.format(filter_name, filter_value)

    # Remove last ? 
    if selected_filter_type != 'collection_stats':
        filter_collection=filter_collection[:-1]   
    
    if selected_filter_type in ['asset', 'asset_contract', 'collection']:
        url = "https://api.opensea.io/api/v1/{}/{}".format(selected_filter_type, filter_collection)
    elif selected_filter_type == 'collection_stats':
        url = "https://api.opensea.io/api/v1/collection/{}/stats".format(filter_collection)
    else:
        url = "https://api.opensea.io/api/v1/{}?{}".format(selected_filter_type, filter_collection)
    
    # print(url)
    
    # Headers only used in events
    headers = {"Accept": "application/json"}

    if 'events' not in url:
        response = requests.request("GET", url)
    elif 'stats' not in url:
        response = requests.request("GET", url)
    else:
        response = requests.request("GET", url, headers=headers)

    # Convert str outcome to dictionary
    response_dict = json.loads(response.text)
    return response_dict