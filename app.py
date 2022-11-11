import os

from flask import Flask
from config import config

# flask app
app = Flask(__name__)
app.config.from_pyfile(os.path.abspath(config.__file__))

import router.route 

if __name__ == '__main__':
    app.run()
