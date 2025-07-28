# from algoliasearch.search_client import SearchClient

# # Replace with your actual Algolia credentials
# ALGOLIA_APP_ID = '8H1FCJWZWP'
# ALGOLIA_API_KEY = '641ca1e39b3a0738fe4378e475599fd7'
# ALGOLIA_INDEX_NAME = 'product_Product'

# def get_index(index_name=ALGOLIA_INDEX_NAME):
#     client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
#     return client.init_index(index_name)

# def perform_search(query, **kwargs):
#     index = get_index()
#     return index.search(query, kwargs)
