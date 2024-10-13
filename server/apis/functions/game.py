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

@csrf_exempt
def gameSearch(request):
    '''
    游戏的近似搜索
    body: keywords
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            keywords = body['keywords']
            check_query = 'SELECT * FROM games WHERE gamename LIKE "%%s%"'
            cursor.execute(check_query, (keywords))
            inf1 = cursor.fetchall()
            check_query = 'SELECT * FROM games WHERE information LIKE "%%s%"'
            cursor.execute(check_query, (keywords))
            inf2 = cursor.fetchall()
            inf = inf1 + inf2
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if inf:
                return JsonResponse({
                    'success': True,
                    'data': inf
                })
            else:
                return JsonResponse(failInf('Search Fail: No Similar Inf'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Search Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Search Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Search Fail: Invalid Request Method'), status=405)
