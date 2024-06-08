import gridfs
from fastapi import UploadFile
from pymongo import MongoClient


class Storage:
    def __init__(self, configuration):
        server_address = configuration.get('mongo_address')
        server_port = configuration.get('mongo_port')
        self.image_collection_name = configuration.get('mat4pat')
        self.products_collection_name = configuration.get('product')
        self.models_collection_name = configuration.get('model')
        self.client = MongoClient(server_address, server_port)


    def reset(self):
        db = self.client.cosyma_kb
        db[self.image_collection_name].delete_many({})
        db[self.products_collection_name].delete_many({})
        db[self.models_collection_name].delete_many({})
        db['fs.files'].delete_many({})


    def postDDModel(self, identifier, version, file):
        return self._post(self.models_collection_name, file, self.exists, identifier, version)

    def postMBModel(self, identifier, version, file):
        return self._post(self.products_collection_name, file, self.exists, identifier, version)

    def getDDModel(self, identifier, version):
        return self._get(self.models_collection_name, identifier, version)

    def getMBModel(self, identifier, version):
        return self._get(self.products_collection_name, identifier, version)

    def postImg(self, identifier, file: UploadFile):
        return self._post(self.image_collection_name, file, self.existignore, identifier)

    def _get(self, collection, identifier, version):
        retval = None
        dictionary = self.preparingquery(identifier, version)
        exists = self.exists(collection, dictionary)
        if exists:
            db = self.client.cosyma_kb
            query = db[collection].find(dictionary)
            filesystem = gridfs.GridFS(db)
            results = query[0]
            file = list(filesystem.find({'identifier': results['_id']}))[0]
            retval = file.read()
        return retval

    def exists(self, collection, dictionary):
        db = self.client.cosyma_kb
        query = db[collection].find(dictionary)
        return len(list(query)) > 0

    def existignore(self, collection, dictionary):
        return False

    def _post(self, collection, files, existing, identifier, version = None):
        retval = False
        dictionary = self.preparingquery(identifier, version)
        exists = existing(collection, dictionary)
        if not exists:
            #todo: to fix it. different projects, different databases
            db = self.client.cosyma_kb
            query = db[collection].insert_one(dictionary)
            filesystem = gridfs.GridFS(db)
            #todo: fix in repo4pat --> one entry for different files
            filesystem.put(files.file, filename=files.filename, identifier=query.inserted_id)
            retval = True
        return retval

    def preparingquery(self, identifier, version = None):
        dictionary = {'identifier': identifier}
        if version is not None:
            dictionary['version'] = version
        return dictionary