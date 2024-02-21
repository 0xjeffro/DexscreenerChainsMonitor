import requests
import json
import pymongo
import os
import time


def main():
    HOST = os.environ.get('MONGO_HOST', 'mongodb.railway.internal')
    PORT = int(os.environ.get('MONGO_PORT', 27017))
    UserName = os.environ.get('MONGO_USERNAME', None)
    Password = os.environ.get('MONGO_PASSWORD', None)

    client = pymongo.MongoClient(host=HOST, port=PORT, username=UserName, password=Password)
    db = client.dexscreener

    req = requests.get('https://dd.dexscreener.com/ds-data/chains/')
    data = json.loads(req.text)
    for chain in data:
        name = chain['name']
        print(name)
        doc = {
            "name": name,
            "data": chain,
            "timestamp": time.time()
        }
        result = db.chains.find_one(
            {"name": name}
        )
        if result is None:
            db.chains.insert_one(
                doc
            )


if __name__ == '__main__':
    main()
