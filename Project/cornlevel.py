import urllib.parse, urllib.request, urllib.error, json, cgi
from urllib.request import Request, urlopen


class Product:
    # an object defining a single grocery product, including its corn likely level

    # initializes the object given a dictionary of information
    def __init__(self, dict):
        self.id = dict["id"]
        self.title = dict["title"]
        self.badges = dict["badges"]
        self.ingredients_list = dict["ingredientList"]
        self.ingredients = dict["ingredients"]
        self.corn_level = self.contains_corn()

    # evaluates the corn level based on the given information
    def contains_corn(self):
        corn_level = "Low"
        if check_badges(self.badges):
            for ingredient in self.ingredients:
                if ingredient_contains_corn(ingredient["name"].lower()):
                    corn_level = "Medium"

        else:
            corn_level = "High"

        return corn_level


# retrieves a list of products related to some query
def search_products(query, apikey):
    param = {"query": query, "apiKey": apikey}
    paramstr = urllib.parse.urlencode(param)
    url = 'https://api.spoonacular.com/food/products/search' + "?" + paramstr
    f = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    return json.loads(f.read())


# gets a dictionary of information about one specific product
def get_product_data(query, apikey):
    param = {"apiKey": apikey}
    paramstr = urllib.parse.urlencode(param)
    url = 'https://api.spoonacular.com/food/products/' + str(query) + "?" + paramstr
    f = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    return json.loads(f.read())


# search products while accounting for possible errors
def search_products_safe(query, apikey="4960f06165eb463fb613bbf6a069be73"):
    try:
        return search_products(query, apikey=apikey)["products"]
    except:
        print("An error occurred.")


# gets product information while accounting for possible errors
def get_product_data_safe(product_id, apikey="4960f06165eb463fb613bbf6a069be73"):
    try:
        return get_product_data(product_id, apikey=apikey)
    except:
        print("An error occurred.")


# creates a list of Product objects based on its corresponding dictionary
def get_product_dict(query):
    dict = {}
    product_dict = search_products_safe(query)
    index = 0
    for product in product_dict:
        dict[index] = Product(get_product_data_safe(product["id"]))
        index += 1
    return dict


# checks a product's badges to see if it contains artificial colors, flavors, or ingredients
def check_badges(badges_list):
    no_artificial_colors = False
    no_artificial_flavors = False
    no_artificial_ingredients = False

    for badge in badges_list:
        if badge == "no_artificial_colors":
            no_artificial_colors = True

        if badge == "no_artificial_flavors":
            no_artificial_flavors = True

        if badge == "no_artificial_ingredients":
            no_artificial_ingredients = True

    return no_artificial_colors and no_artificial_flavors and no_artificial_ingredients


# checks to see if a certain ingredient appears in a file listing corn derivatives
def ingredient_contains_corn(ingredient):
    with open("corn_derivatives", encoding='utf-8') as file:
        for line in file:
            if line.lower().rstrip() == ingredient:
                return True
    return False


# generates a dictionary mapping products to their corn likely level
def calculate_corn_level(query):
    product_dict = get_product_dict(query)
    corn_likely_level = {}
    for index in product_dict:
        product = product_dict[index]
        corn_likely_level[product] = product.corn_level

    return corn_likely_level

