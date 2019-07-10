from flask import Flask

from apis import API
import settings

APP = Flask(settings.APP_NAME)
API.init_app(APP)

if __name__ == "__main__":
    APP.run(host=settings.API_HOST,
            port=settings.API_PORT,
            debug=settings.DEBUG,
           )