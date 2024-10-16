import os
import MySQLdb
import json
from responses.responseInf import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from sql_operation.user import *
from sql_operation.game import *
from sql_operation.publisher import *
from sql_operation.usergame import *
from sql_operation.comment import *

db_params = {
    "host": settings.DATABASES['default']['HOST'],
    "user": settings.DATABASES['default']['USER'],
    "passwd": settings.DATABASES['default']['PASSWORD'],
    "db": settings.DATABASES['default']['NAME'],
    "charset": "utf8"
}

@csrf_exempt
def register(request):
    '''
    用户注册功能
    body: userserial, username, nickname, password, role, email
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            userserial = body['userserial']
            user = user_select(userserial)
            
            if not user:
                username = body['username']
                nickname = body['nickname']
                password = body['password']
                role = body['role']
                email = body['email']
                user_insert(userserial, username, nickname, password, role, email)
                return JsonResponse(successInf('Register Succeed'))
            else:
                return JsonResponse(failInf('Register Fail: Username Already Have'), status=400)
            
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Register Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Register Fail: Invalid JSON'), status=400) 
    else:
        return JsonResponse(failInf('Register Fail: Invalid Request Method'), status=405)

@csrf_exempt
def login(request):
    '''
    用户登录功能
    body: userserial, password
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            userserial = body['userserial']
            user = user_select(userserial)
            
            if user:
                password = user[2]
                if body['password'] == password:
                    return JsonResponse({
                        'success': True,
                        'message': 'Login Succeed',
                        'data': [{
                            'username': user[0],
                            'nickname': user[1],
                            'role': user[3],
                            'email': user[4],
                            'balance': user[5],
                            'avatar': user[6],
                            'introduction': user[7]
                        }]
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
def alterUser(request):
    '''
    用户修改信息功能
    body: userserial, type, content
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            userserial = body['userserial']
            user = user_select(userserial)
            
            if user:
                alterType = body['type']
                content = body['content']
                if alterType != 'serial' and alterType != 'username'\
                    and alterType != 'role' and alterType != 'balance':
                    user_update(userserial, alterType, content)
                    return JsonResponse(successInf('Alter succeed'))
                else:
                    return JsonResponse(failInf('Alter Fail: No Permission'), status=400)
            else:
                return JsonResponse(failInf('Alter Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Alter Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Alter Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Alter Fail: Invalid Request Method'), status=405)

@csrf_exempt
def addGame(request):
    '''
    管理员用户增加游戏
    body: userserial, gameserial, gamename, gametype, publisherserial, information, price
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            
            userserial = body['userserial']
            user = user_select(userserial)
            publisherserial = body['publisherserial']
            publish = publisher_select(publisherserial)
            
            if user and publish:
                role = user[3]
                if role == 'admin':
                    gameserial = body['gameserial']
                    gamename = body['gamename']
                    gametype = body['gametype']
                    publisher = body['publisher']
                    information = body['information']
                    price = body['price']
                    game_insert(gameserial, gamename, gametype, publisher, information, price)
                    return JsonResponse(successInf('Add Game Succeed'))
                else:
                    return JsonResponse(failInf('Add Game Fail: No Permission'), status=400)
            elif user:
                return JsonResponse(failInf('Add Game Fail: No Such Publisher'), status=400)
            else:
                return JsonResponse(failInf('Add Game Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Add Game Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Add Game Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Add Game Fail: Invalid Request Method'), status=405)

@csrf_exempt
def addPublisher(request):
    '''
    管理员用户增加发行商
    body: userserial, publisherserial, publishername, information
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            userserial = body['userserial']
            user = user_select(userserial)
            
            if user:
                role = user[3]
                if role == 'admin':
                    publisherserial = body['publisherserial']
                    publishername = body['publishername']
                    information = body['information']
                    publisher_insert(publisherserial, publishername, information)
                    return JsonResponse(successInf('Add Publisher Succeed'))
                else:
                    return JsonResponse(failInf('Add Publisher Fail: No Permission'), status=400)
            else:
                return JsonResponse(failInf('Add Publisher Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Add Publisher Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Add Publisher Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Add Publisher Fail: Invalid Request Method'), status=405)

@csrf_exempt
def buyGame(request):
    '''
    用户购买游戏
    body: userserial, gameserial
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            userserial = body['userserial']
            user = user_select(userserial)
            gameserial = body['gameserial']
            game = game_select(gameserial)
            
            if user and game:
                balance = user[6]
                price = game[5]
                if balance >= price:
                    usergame_insert(userserial, gameserial)
                    user_update(userserial, 'balance', balance - price)
                    return JsonResponse(successInf('Buy Game Succeed'))
                else:
                    return JsonResponse(failInf('Buy Game Fail: Money Not Enough'), status=400)
            elif user:
                return JsonResponse(failInf('Buy Game Fail: No Such Game'), status=400)
            else:
                return JsonResponse(failInf('Buy Game Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Buy Game Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Buy Game Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Buy Game Fail: Invalid Request Method'), status=405)

@csrf_exempt
def searchGame(request):
    '''
    游戏的近似搜索
    body: keywords
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            keywords = body['keywords']
            inf1 = game_search('gamename', keywords)
            inf2 = game_search('information', keywords)
            inf = inf1 + inf2
            
            if inf:
                return JsonResponse({
                    'success': True,
                    'message': 'Search Game Succeed',
                    'data': inf
                })
            else:
                return JsonResponse(failInf('Search Game Fail: No Similar Inf'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Search Game Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Search Game Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Search Game Fail: Invalid Request Method'), status=405)

@csrf_exempt
def makeComment(request):
    '''
    用户进行评论
    body: commentserial, userserial, gameserial, commentedserial, content
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            userserial = body['userserial']
            user = user_select(userserial)
            
            gameserial = body['gameserial']
            if gameserial != None:
                game = game_select(gameserial)
                if not game:
                    return JsonResponse(failInf('Make Comment Fail: No Such Game'), status=400)
                
            commentedserial = body['commentedserial']
            if commentedserial != None:
                comment = comment_select(commentedserial)
                if not comment:
                    return JsonResponse(failInf('Make Comment Fail: No Such Comment'), status=400)
            
            if user:
                commentserial = body['commentserial']
                content = body['content']
                comment_insert(commentserial, userserial, gameserial, commentedserial, content)
                return JsonResponse(successInf('Make Comment Succeed'))
            else:
                return JsonResponse(failInf('Make Comment Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Make Comment Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Make Comment Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Make Comment Fail: Invalid Request Method'), status=405)

@csrf_exempt
def agreeComment(request):
    '''
    用户对评论点赞或点踩
    body: commentserial, agreeornot
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            commentserial = body['commentserial']
            comment = comment_select(commentserial)
            
            if comment:
                agreeOrNot = body['agreeornot']
                comment_update(commentserial, agreeOrNot, 1)
                return JsonResponse(successInf('Agree Comment Succeed'))
            else:
                return JsonResponse(failInf('Agree Comment Fail: No Such User'), status=400)
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Agree Comment Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Agree Comment Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Agree Comment Fail: Invalid Request Method'), status=405)

@csrf_exempt
def queryHighAgreeComment(request):
    '''
    用户查询高赞同或高反对评论
    body: agreeornot
    '''
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            agreeOrNot = body['agreeornot']
            comments = comment_select_DESC(agreeOrNot, 100)
            return JsonResponse({
                'success': True,
                'message': 'Query High Comments Succeed',
                'data': comments
            })
        
        except MySQLdb.Error as e:
            return JsonResponse(failInf('Query High Comments Fail: ' + str(e)), status=500)
        except json.JSONDecodeError:
            return JsonResponse(failInf('Query High Comments Fail: Invalid JSON'), status=400) 
    return JsonResponse(failInf('Query High Comments Fail: Invalid Request Method'), status=405)