#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# main.py
# v1.0.1
#

DATABASE = 'sample.db'

import sqlite3
import string
import random
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    """ Present the user with route options. """
    return render_template('index.html')


@app.route('/get')
def get_statement(q_string=None):
    """ Fetch a random statement or a list of synonyms.

    A GET request will return a random statement.
    A POST request will retrieve a list of synonyms for q_string.

    """

    # A POST request will retrieve a list of synonyms for q_string.
    if q_string:
        query = '''SELECT word_text FROM word WHERE word_text=%s''' \
                % q_string

    # A GET request will return a random statement.
    else:
        rand_i = ''.join(random.choice(string.ascii_letters + '0123456789')
                         for i in range(10))
        query = ''' SELECT state_text FROM statements ''' \
                ''' WHERE state_key <= \'%s\'''' % rand_i

    # query DB and return
    with sqlite3.connect('sample.db') as con:
        cur = con.cursor()
        print("Query: " + query)
        cur.execute(query)
        data = cur.fetchone()
    if not data:
        return "Nothing found."
    else:
        return data


@app.route('/define')
def define():
    """ Tag a word or phrase with synonyms. """
    pass


@app.route('/submit')
def submit():
    """ This function accepts a POSTed statement or synonym. """
    pass


def init_db(db_file, schema_file, ow=False):
    # if exists(db_files) and not ow:
    # else:
    open(db_file, 'w').close
    with sqlite3.connect(db_file) as db:
        with open(schema_file, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    app.run(debug=True)
