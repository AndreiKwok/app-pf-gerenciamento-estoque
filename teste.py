import requests
from datetime import datetime
def buy():
    url = "http://127.0.0.1:8000/item/buy_item"

    # Dados a serem enviados no corpo da solicitação
    data = {
        "name_product": "Galaxy S100",
        "qtd": 2
    }

    # Realiza a solicitação POST
    response = requests.put(url, json=data)
    print(response.text)
update_product = {"$set": {"product": [{"product_name": "xxx",
                                                        "qtd":"xxxx",
                                                        "price_product": "xxxx",
                                                        "product_type": "xxxx",
                                                        "product_soldout": "xxxx", #AFTER VALID THIS CAMP
                                                        "qtd":"xxxx"}],
                                                    "data_creation":"date",
                                                    "data_modification": datetime.now()
                                                        }}
update_product["$set"]["product"][0]["qtd"] = 10000



def test(field):
    match field:
        case "name_product": update_product["$set"]["product"][0]["name_product"] = "plaaaaaaaaaaa"
test("name_product")
print(update_product)