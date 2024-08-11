from django.db import connection
from rest_framework import status as st
from rest_framework.response import Response
from datetime import datetime
from marcos_server.utils.loggers import log_message

def execute_query(query):
    cur = connection.cursor()
    try:
        cur.execute(query)
        log_message({"function": "execute_query", "query": query})
        customer_lst = cur.fetchall()
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in customer_lst]
        return result

    except Exception as e:
        print("Exception:- {}".format(str(e)))
        result = []

    finally:
        if cur is not None:
            cur.close()


def insert_query(query):
    cur = connection.cursor()
    try:
        cur.execute(query)
        log_message({"function": "insert_query", "query": query})

    except Exception as e:
        print("Exception:- {}".format(str(e)))

    finally:
        if cur is not None:
            cur.close()
