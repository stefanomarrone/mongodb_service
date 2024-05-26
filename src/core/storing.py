import gridfs
from pymongo import MongoClient


class Storage:
    def __init__(self, configuration):
        server_address = configuration.get('mongo_address')
        server_port = configuration.get('mongo_port')
        self.products_collection_name = configuration.get('product')
        self.models_collection_name = configuration.get('model')
        self.client = MongoClient(server_address, server_port)

    def reset(self):
        db = self.client.cosyma_kb
        db[self.products_collection_name].delete_many({})
        db[self.models_collection_name].delete_many({})
        db['fs.files'].delete_many({})

    def _post(self, identifier, version, file, collection):
        retval = False
        exists = self.exists(identifier, version, collection)
        if not exists:
            db = self.client.cosyma_kb
            query = db[collection].insert_one({"identifier": identifier, "version": version})
            filesystem = gridfs.GridFS(db)
            filesystem.put(file.file, filename=file.filename, identifier=query.inserted_id)
            retval = True
        return retval

    def postDDModel(self, identifier, version, file):
        return self._post(identifier, version, file, self.models_collection_name)

    def postMBModel(self, identifier, version, file):
        return self._post(identifier, version, file, self.products_collection_name)

    def getDDModel(self, identifier, version):
        return self._get(identifier, version, self.models_collection_name)

    def getMBModel(self, identifier, version):
        return self._get(identifier, version, self.products_collection_name)

    def _get(self, identifier, version, collection):
        retval = None
        exists = self.exists(identifier, version, collection)
        if exists:
            db = self.client.cosyma_kb
            query = db[collection].find({"identifier": identifier, "version": version})
            filesystem = gridfs.GridFS(db)
            results = query[0]
            file = list(filesystem.find({'identifier': results['_id']}))[0]
            retval = file.read()
        return retval

    def exists(self, identifier, version, collection):
        db = self.client.cosyma_kb
        query = db[collection].find({"identifier": identifier, "version": version})
        return len(list(query)) > 0
