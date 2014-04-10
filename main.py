#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# main.py
# v1.0.2
#

DATABASE = 'sample.db'

import sqlite3
import string
import random
from flask import Flask, render_template, request
app = Flask(__name__)


class Word():
    def __init__(self, text, key=None, node_list=None):
        self.text = text
        if not key:
            key = ''.join(random.choice(string.ascii_letters + '0123456789')
                          for i in range(8))
        self.key = key
        self.node_list = node_list

class Statement():
    def __init__(self, text, key=None):
        self.text = text
        if not key:
            key = ''.join(random.choice(string.ascii_letters + '0123456789')
                          for i in range(8))
        self.key = key


class Node():
    def __init__(self, key=None, word_list=None):
        if not key:
            key = ''.join(random.choice(string.ascii_letters + '0123456789')
                          for i in range(8))
        self.key = key
        self.word_list = word_list



@app.route('/')
def index():
    """ Present the user with route options. """
    return render_template('index.html')


@app.route('/get', methods=['GET', 'POST'])
def get_statement():
    """ Fetch a random statement or a list of synonyms.

    A GET request will return a random statement.
    A POST request will retrieve a list of synonyms for q_string.

    """
    # A POST request will retrieve a list of synonyms for q_string.
    q_string = request.form.get('phrase')
    if q_string:
        query = '''SELECT node_list FROM words WHERE word_text=\'%s\'''' \
                % q_string
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            print("Query: " + query)
            cur.execute(query)
            data = cur.fetchone()
        if not data:
            return "Word not found."
        else:
            pass

    # A GET request will return a random statement.
    else:
        rand_i = ''.join(random.choice(string.ascii_letters + '0123456789')
                         for i in range(8))
        query = ''' SELECT state_text FROM statements
                    WHERE state_key <= \'%s\'''' % rand_i

    # query DB and return
    with sqlite3.connect(DATABASE) as con:
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
    """ Add and/or tag a word or phrase with synonyms. """
    pass


@app.route('/rebucket')
def define():
    """ View a word's nodes and rebucket to define meanings. """
    pass


@app.route('/submit', methods=['POST'])
def submit():
    """ This function accepts a POSTed statement or synonym. """
    data = request.form.get('data')
    if not data:
        raise Exception("POST error: no value for key 'data'.")
    elif type(data) is not list:
        raise Exception("POST error: value for key 'data' is not a list.")
    else:
        for el in data:
            Words = []
            Word_keys = []
            for word in el:
                # query DB for word
                query = 'SELECT node_list FROM words WHERE word_text=\'%s\'' \
                        % word
                with sqlite3.connect(DATABASE) as con:
                    cur = con.cursor()
                    print("Query: " + query)
                    cur.execute(query)
                    data = cur.fetchone()
                if not data:
                    tmp = Word(word)
                    Words.append(tmp)
                    Word_keys.append(tmp.key)
                else:
                    raise Exception("TODO!!!")
            tmp = Node(word_list=str(Word_keys))  # new node for this word list
            query = '''INSERT INTO nodes(node_key, word_list)
                       VALUES({}, {})'''.format(tmp.key, tmp.word_list)
            node_list = str([tmp.key])
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                print("Query: " + query)
                cur.execute(query)
            print("Node inserted.")
            for word in Words:
                # still assuming there will be no duplication
                query = '''INSERT INTO words(word_key, word_text, node_list)
                           VALUES({}, {})'''.format(word.key, word.text,
                                                    node_list)
                with sqlite3.connect(DATABASE) as con:
                    cur = con.cursor()
                    print("Query: " + query)
                    cur.execute(query)
                print("Added word: " % word.text)


def init_db(db_file, schema_file, ow=False):
    import os
    if os.path.isfile(db_file) and not ow:
        raise Exception("ERROR: DB exists but overwrite was not indicated.")
    else:
        open(db_file, 'w').close  # create or overwrite
    with sqlite3.connect(db_file) as db:
        with open(schema_file, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    app.run(debug=True)
