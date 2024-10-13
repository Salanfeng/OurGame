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
def userRegister(request):
    '''
    用户注册功能
    body: username, nickname, password, role, email
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            username = body['username']
            check_query = 'SELECT * FROM users WHERE username = %s'
            cursor.execute(check_query, (username))
            result = cursor.fetchone()
            
            if not result:
                nickname = body['nickname']
                password = body['password']
                role = body['role']
                email = body['email']
                insert_query = '''
                    INSERT INTO 
                    users (username, nickname, password, role, email, balance, avatar, introduction)
                    VALUE (%s, %s, %s, %s, %s, %f, %s, %s);
                '''
                cursor.execute(insert_query, 
                               (username, nickname, password, role, email, 0.0, '_', '_'))
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(successInf('Register Succeed'))
            else:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Register Fail: Username Already Have'), status=400)
            
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Register Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Register Fail: Invalid JSON'), status=400) 
    else:
        return JsonResponse(failInf('Register Fail: Invalid Request Method'), status=405)


@csrf_exempt
def userLogin(request):
    '''
    用户登录功能
    body: username, password
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            username = body['username']
            check_query = 'SELECT * FROM users WHERE username = %s'
            cursor.execute(check_query, (username))
            result = cursor.fetchone()
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if result:
                password = result[2]
                if body['password'] == password:
                    return JsonResponse({
                        'success': True,
                        'data': {
                            'username': result[0],
                            'nickname': result[1],
                            'role': result[3],
                            'email': result[4],
                            'balance': result[5],
                            'avatar': result[6],
                            'introduction': result[7]
                        }
                    })
                else:
                    return JsonResponse(failInf('Login Fail: Password Incorrect'), status = 400)
            else:
                return JsonResponse(failInf('Login Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Login Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Login Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Login Fail: Invalid Request Method'), status=405)

@csrf_exempt
def userAlter(request):
    '''
    用户修改信息功能
    body: username, type, content
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            username = body['username']
            check_query = 'SELECT * FROM users WHERE username = %s'
            cursor.execute(check_query, (username))
            result = cursor.fetchone()
            
            if result:
                alterType = body['type']
                content = body['content']
                alter_query = '''
                    UPDATE users
                    SET %s = %s
                    WHERE username = %s
                '''
                cursor.execute(alter_query, (alterType, content, username))
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(successInf('Alter succeed'))
            else:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Alter Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Alter Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Alter Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Alter Fail: Invalid Request Method'), status=405)