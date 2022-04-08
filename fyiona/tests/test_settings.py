import pytest

from django.db import connections
from django.db.utils import OperationalError


@pytest.mark.django_db
class TestDatabase:
    def test_db_connection(self):
        connected = True
        db_conn = connections["default"]
        try:
            db_conn.cursor()
        except OperationalError:
            connected = False

        assert connected
        assert db_conn.connection.closed == False

    def test_db_disconnection(self):
        db_connection = connections["default"]
        db_connection.close()
        assert db_connection.connection.closed == True
