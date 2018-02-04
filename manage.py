# !/usr/bin/env python
# coding:utf-8
# author bai
from flask_script import Manager

from apps import create_app


app = create_app()

manage = Manager(app)

if __name__ == '__main__':
    app.run(debug=False)


