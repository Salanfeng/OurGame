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
    body: userserial, username, nickname, password, role, email
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            userserial = body['userserial']
            check_query = 'SELECT * FROM users WHERE serial = %d'
            cursor.execute(check_query, (userserial))
            result = cursor.fetchone()
            
            if not result:
                username = body['username']
                nickname = body['nickname']
                password = body['password']
                role = body['role']
                email = body['email']
                insert_query = '''
                    INSERT INTO 
                    users (serial, username, nickname, password, role, email, balance, avatar, introduction)
                    VALUE (%d, %s, %s, %s, %s, %s, %f, %s, %s);
                '''
                cursor.execute(insert_query, 
                               (userserial, username, nickname, password, role, email, 0.0, '_', '_'))
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
    body: userserial, password
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            userserial = body['userserial']
            check_query = 'SELECT * FROM users WHERE serial = %d'
            cursor.execute(check_query, (userserial))
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
    body: userserial, type, content
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            userserial = body['userserial']
            check_query = 'SELECT * FROM users WHERE serial = %d'
            cursor.execute(check_query, (userserial))
            result = cursor.fetchone()
            
            if result:
                alterType = body['type']
                content = body['content']
                alter_query = '''
                    UPDATE users
                    SET %s = %s
                    WHERE serial = %d
                '''
                cursor.execute(alter_query, (alterType, content, userserial))
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

@csrf_exempt
def userAddGame(request):
    '''
    管理员用户增加游戏
    body: userserial, gameserial, gamename, gametype, publisher, information, price
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            userserial = body['userserial']
            check_query = 'SELECT * FROM users WHERE serial = %d'
            cursor.execute(check_query, (userserial))
            user = cursor.fetchone()
            publisher = body['publisher']
            check_query = 'SELECT * FROM publishers WHERE serial = %d'
            cursor.execute(check_query, (publisher))
            publish = cursor.fetchone()
            
            if user and publish:
                role = user[3]
                if role == 'admin':
                    gameserial = body['gameserial']
                    gamename = body['gamename']
                    gametype = body['gametype']
                    publisher = body['publisher']
                    information = body['information']
                    price = body['price']
                    insert_query = '''
                        INSERT INTO 
                        games(serial, gamename, gametype, publisherSerial, information, price)
                        VALUE (%d, %s, %s, %d, %s, %f)
                    '''
                    cursor.execute(insert_query, 
                                (gameserial, gamename, gametype, publisher, information, price))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return JsonResponse(successInf('Add Game Succeed'))
                else:
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return JsonResponse(failInf('Add Game Fail: No Permission'), status=400)
            elif user:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Add Game Fail: No Such Publisher'), status=400)
            else:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Add Game Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Add Game Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Add Game Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Add Game Fail: Invalid Request Method'), status=405)

@csrf_exempt
def userAddPublisher(request):
    '''
    管理员用户增加发行商
    body: userserial, publisherserial, publishername, information
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            userserial = body['userserial']
            check_query = 'SELECT * FROM users WHERE userserial = %d'
            cursor.execute(check_query, (userserial))
            user = cursor.fetchone()
            
            if user:
                role = user[3]
                if role == 'admin':
                    publisherserial = body['publisherserial']
                    publishername = body['publishername']
                    information = body['information']
                    insert_query = '''
                        INSERT INTO 
                        publishers(serial, publishername, information)
                        VALUE (%d, %s, %s)
                    '''
                    cursor.execute(insert_query, 
                                (publisherserial, publishername, information))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return JsonResponse(successInf('Add Publisher Succeed'))
                else:
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return JsonResponse(failInf('Add Publisher Fail: No Permission'), status=400)
            else:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Add Publisher Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Add Publisher Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Add Publisher Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Add Publisher Fail: Invalid Request Method'), status=405)

@csrf_exempt
def userBuyGame(request):
    '''
    用户购买游戏
    body: userserial, gameserial
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            conn = MySQLdb.connect(**db_params)
            cursor = conn.cursor()
            
            userserial = body['userserial']
            check_query = 'SELECT * FROM users WHERE serial = %d'
            cursor.execute(check_query, (userserial))
            user = cursor.fetchone()
            gameserial = body['gameserial']
            check_query = 'SELECT * FROM games WHERE serial = %d'
            cursor.execute(check_query, (gameserial))
            game = cursor.fetchone()
            
            if user and game:
                balance = user[6]
                price = game[5]
                if balance >= price:
                    insert_query = '''
                        INSERT INTO 
                        usergame(userserial, gameserial)
                        VALUE (%d, %d)
                    '''
                    cursor.execute(insert_query, (userserial, gameserial))
                    alter_query = '''
                        UPDATE users
                        SET balance = %f
                        WHERE serial = %d
                    '''
                    cursor.execute(alter_query, (balance - price, userserial))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return JsonResponse(successInf('Buy Game Succeed'))
                else:
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return JsonResponse(failInf('Buy Game Fail: Money Not Enough'), status=400)
            elif user:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Buy Game Fail: No Such Game'), status=400)
            else:
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(failInf('Buy Game Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Buy Game Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Buy Game Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Buy Game Fail: Invalid Request Method'), status=405)
