import uvicorn
import sys
from fastapi import FastAPI
from src.core.routers import router
from src.utils.configuration import Configuration

def main(inifilename):
    conf = Configuration(inifilename)
    applicationport = conf.get('applicationport')
    app = FastAPI()
    app.include_router(router)
    router.configuration = conf
    uvicorn.run(app, host='193.206.101.14', port=applicationport) #todo: put in configuration


if __name__ == "__main__":
    main(sys.argv[1])
