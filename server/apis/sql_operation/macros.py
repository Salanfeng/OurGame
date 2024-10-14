import os
import MySQLdb
import json
from responses.responseInf import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings

db_params = {
    "host": settings.DATABASES['default']['HOST'],
    "user": settings.DATABASES['default']['USER'],
    "passwd": settings.DATABASES['default']['PASSWORD'],
    "db": settings.DATABASES['default']['NAME'],
    "charset": "utf8"
}

def connectSQL():
    conn = MySQLdb.connect(**db_params)
    cursor = conn.cursor()
    return conn, cursor

def closeSQL(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()