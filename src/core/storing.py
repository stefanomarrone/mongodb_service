import gridfs
from pymongo import MongoClient


class Storage:
    def __init__(self, configuration):
        server_address = configuration.get('mongo_address')
        server_port = configuration.get('mongo_port')
        self.client = MongoClient(server_address, server_port)

    def postDDModel(self, identifier, version, file):
        retval = False
        exists = self.existsDDModel(identifier, version)
        if not exists:
            db = self.client.cosyma_kb
            query = db.models.insert_one({"identifier": identifier, "version": version})
            filesystem = gridfs.GridFS(db)
            filesystem.put(file.file, filename=file.filename, identifier = query.inserted_id)
            retval = True
        return retval

    def getDDModel(self, identifier, version, file):
        retval = False
        exists = self.existsDDModel(identifier, version)
        if exists:
            db = self.client.cosyma_kb
            query = db.models.find({"identifier": identifier, "version": version})
            filesystem = gridfs.GridFS(db)
            #todo: continuare


            filesystem.get(file.file, filename=file.filename, identifier = query.inserted_id)
            retval = True
        return retval

    def existsDDModel(self, identifier, version):
        db = self.client.cosyma_kb
        fs = gridfs.GridFS(db)
        query = db.models.find({"identifier": identifier, "version": version})
        return len(list(query)) > 0