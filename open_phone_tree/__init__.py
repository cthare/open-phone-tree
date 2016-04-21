import os
from flask import Flask

# application start
app = Flask(__name__, instance_path="/instance/")
app.config.from_pyfile('instance/config.py')



import open_phone_tree.views


if __name__ == '__main__':
    app.run()