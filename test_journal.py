# -*- coding: utf-8 -*-
from contextlib import closing
import pytest
from journal import app
from journal import connect_db
from journal import get_database_connection
from journal import init_db


TEST_DSN = 'dbname=test_learning_journal'


def clear_db():
    with closing(connect_db()) as db:
        db.cursor().execute("DROP TABLE entries")
        db.commit()


@pytest.fixture(scope='session')
def test_app():
    """configure our app for use in testing"""
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True


@pytest.fixture(scope='session')
def db(test_app, request):
    """initialize the entries table and drop it when finished"""
    init_db()

    def cleanup():
        clear_db()

    request.addfinalizer(cleanup)


@pytest.yield_fixture(scope='function')
def req_context(db):
    """run tests within a test request context so that 'g' is present"""
    with app.test_request_context('/'):
        yield
        con = get_database_connection()
        con.rollback()


def run_independent_query(query, params=[]):
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def test_write_entry(req_context):
    from journal import write_entry
    expected = ("My Title", "My Text")
    write_entry(*expected)
    rows = run_independent_query("SELECT * FROM entries")
    assert len(rows) == 1
    for val in expected:
        assert val in rows[0]


def test_get_all_entries_empty(req_context):
    from journal import get_all_entries
    entries = get_all_entries()
    assert len(entries) == 0


def test_get_all_entries(req_context):
    from journal import write_entry, get_all_entries
    expected = ("My Title", "My Text")
    write_entry(*expected)
    entries = get_all_entries()
    assert len(entries) == 1
    for entry in entries:
        assert expected[0] == entry['title']
        assert expected[1] == entry['text']
        assert 'created' in entry
