import os
import MySQLdb
import json
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
def login(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if body.get('username') == 'admin':
            return JsonResponse({
                'success': True,
                'data': {
                    'avatar': 'https://avatars.githubusercontent.com/u/44761321',
                    'username': 'admin',
                    'nickname': '小铭',
                    'roles': ['admin'],
                    'permissions': ['*:*:*'],
                    'accessToken': 'eyJhbGciOiJIUzUxMiJ9.admin',
                    'refreshToken': 'eyJhbGciOiJIUzUxMiJ9.adminRefresh',
                    'expires': '2030/10/30 00:00:00'
                }
            })
        else:
            return JsonResponse({
                'success': True,
                'data': {
                    'avatar': 'https://avatars.githubusercontent.com/u/52823142',
                    'username': 'common',
                    'nickname': '小林',
                    'roles': ['common'],
                    'permissions': ['permission:btn:add', 'permission:btn:edit'],
                    'accessToken': 'eyJhbGciOiJIUzUxMiJ9.common',
                    'refreshToken': 'eyJhbGciOiJIUzUxMiJ9.commonRefresh',
                    'expires': '2030/10/30 00:00:00'
                }
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def get_async_routes(request):
    try:
        with open('apis\permission_router.json', 'r', encoding='utf-8') as file:
            permission_router = json.load(file)
    except FileNotFoundError:
        return JsonResponse({"success": False, "message": "File not found"}, status=404)
    return JsonResponse({"success": True, "data": [permission_router]})

@csrf_exempt
@require_POST
def refresh_token(request):
    try:
        body = json.loads(request.body)
        if 'refreshToken' in body:
            response = {
                "success": True,
                "data": {
                    "accessToken": "eyJhbGciOiJIUzUxMiJ9.newAdmin",
                    "refreshToken": "eyJhbGciOiJIUzUxMiJ9.newAdminRefresh",
                    "expires": "2030/10/30 23:59:59"
                }
            }
        else:
            response = {
                "success": False,
                "data": {}
            }
        return JsonResponse(response)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_POST
def modify(request):
    try:
        body = json.loads(request.body)
        conn = MySQLdb.connect(**db_params)
        cursor = conn.cursor()
        # 检查是否有 name 为 'xiaoming' 的记录
        check_query = "SELECT * FROM test WHERE name = 'xiaoming'"
        cursor.execute(check_query)
        result = cursor.fetchone()
        
        if not result:
            # 如果没有符合条件的数据，插入新数据
            insert_query = "INSERT INTO test (name, value) VALUES (%s, %s)"
            cursor.execute(insert_query, ('xiaoming', body['value']))
        else:
            # 如果有符合条件的数据，更新数据
            update_query = "UPDATE test SET value = %s WHERE name = 'xiaoming'"
            cursor.execute(update_query, (body['value'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({"success": True, "message": "Modification successful"})
    except MySQLdb.Error as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    
@csrf_exempt
@require_GET
def query(request):
    try:
        conn = MySQLdb.connect(**db_params)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        # 查询 name 为 'xiaoming' 的记录
        query = "SELECT * FROM test WHERE name = 'xiaoming'"
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            # 如果没有数据，插入默认值
            insert_query = "INSERT INTO test (name, value) VALUES (%s, %s)"
            cursor.execute(insert_query, ('xiaoming', 'default value'))
            conn.commit()
            # 再次查询以返回插入的默认值
            cursor.execute(query)
            result = cursor.fetchone()

        cursor.close()
        conn.close()
        print(result)
        return JsonResponse({"success": True, "data": result})
    except MySQLdb.Error as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
