# Версия 4.1. 
# Набор функция для работы с аккаунтами телеграмм


# Подключение к базе данных
def connect (connect_info):
    import pymysql 
    db = pymysql.connect(host=connect_info['host'],
                            user=connect_info['user'],
                            password=connect_info['password'],
                            database=connect_info['database'],
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)  
    cursor = db.cursor() 
    return db,cursor
      
# Подлючение телеграмм клиента по имени учетки (телефон)
def telegram_connect (account,api_id,api_hash):
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession  
    connect_info['database'] = 'telegram'    
    answer = 'Отсутствует учетная запись в базе'
    client = ''
    phone_number = account.setdefault('name','')
    session = account.setdefault('session','')    
    if phone_number.find ('+') == -1:
        phone_number = '+'+str(phone_number)
    print ('        [+] Подключение телефоного аккаунта:  , ',phone_number,session)
    client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
    client.connect()    
    if not client.is_user_authorized():
        answer = 'Отсутствует подключение к телеграмм серверу'
        print (c12,'            [+] Результат подключения: {}'.format(answer),c23)
    else:
        answer = 'Подключение к телеграмм серверу успешно'
        print (c3,'            [+] Результат подключения: {}'.format(answer),c23)
    return client,answer
  
### Тестирование работоспособности
def function_test_accound(list_account):
    import time
    nm = 0
    for account in list_account:
        nm = nm + 1
        print ('       [+] № {:0>4d}, аккаунд: {}'.format(nm,account))
        client,answer = telegram_connect (account,api_id,api_hash)
        if answer == 'Подключение к телеграмм серверу успешно':
            me = client.get_me()
            print(me.stringify())
        time.sleep (3)
    print (c3,'               [+] Итого: {} шт.'.format(nm),c23)      
    
### Получить список аккаунтов
def function_list_account():
    setting01 = False  ### База MAIN
    setting02 = False  ### База PING
    setting03 = True  ### База TELEGRAM
    results =[]
    ### --------------------------------------------------------------
    if setting01 == True:
        print (c10,'       [+] База MAIN'.format(),c23)    
        connect_info['database'] = 'main'    
        db,cursor = connect (connect_info)
        sql = "select id,name,session from telegram_session where 1=1;"
        cursor.execute(sql)
        results = cursor.fetchall()    
        nm = 0
        for row in results:
            nm = nm + 1
            print ('            [+] № {:0>4d}, тел: {:^17}'.format(nm,row['name']))
        print (c3,'               [+] Итого: {} шт.'.format(nm),c23)        
    ### --------------------------------------------------------------
    if setting02 == True:
        print (c10,'       [+] База PING'.format(),c23)
        connect_info['database'] = 'ping314_bot'    
        db,cursor = connect (connect_info)
        sql = "select A1.id as id,A1.info as name,A2.info as session from accound as A1,accound as A2 where A1.name = 'Имя' and A1.id = A2.data_id and A2.name = 'Токен'"
        cursor.execute(sql)
        results = cursor.fetchall()    
        nm = 0
        for row in results:
            nm = nm + 1
            print ('            [+] № {:0>4d}, тел: {:^17}'.format(nm,row['info']))
        print (c3,'               [+] Итого: {} шт.'.format(nm),c23)  
    ### --------------------------------------------------------------    
    if setting03 == True:
        print (c10,'       [+] База TELEGRAM'.format(),c23)
        connect_info['database'] = 'telegram'    
        db,cursor = connect (connect_info)
        sql = "select A1.id as id,A1.info as name,A2.info as session from accound as A1,accound as A2 where A1.name = 'Имя' and A1.id = A2.data_id and A2.name = 'Токен' and A1.id = 630"
        cursor.execute(sql)
        results = cursor.fetchall()    
        nm = 0
        for row in results:
            nm = nm + 1
            print ('            [+] № {:0>4d}, тел: {:^17}'.format(nm,row['name']))
        print (c3,'               [+] Итого: {} шт.'.format(nm),c23)    
    return results

### Регистрация нового клиента
def function_reg_new_account (phone_number):
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    session_file = 'session_{}.session'.format(phone_number)
    client = TelegramClient(session_file,api_id=api_id,api_hash=api_hash)
    client.connect()
    if not client.is_user_authorized():
        print (c9,'    [+] Регистрация клиента',phone_number,c23)  
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))
    else:
        print (c10,'    [+] У пользователя есть активная session ',c23)  
    string = StringSession.save(client.session)
    print ('        [+] Полученная строковая сесия:',string)
    
    print ('         [+] Проверяем наличее в базе: TELEGRAM')
    connect_info['database'] = 'telegram'    
    db,cursor = connect (connect_info)
    sql = "select A1.id as id,A1.info as name,A2.info as session from accound as A1,accound as A2 where A1.name = 'Имя' and A1.id = A2.data_id and A2.name = 'Токен' and A1.info = '{}'".format (phone_number)
    cursor.execute(sql)
    results = cursor.fetchall()    
    id = 0
    for row in results:
        id,name,session = row.values()
        print ('            [+] № {:0>4d}, тел: {:^17}'.format(1,row['name']))
    if id == 0:
        print (c3,'        [+] Данный аккаунт не найдей в базе TELEGRAM. Записываем данный номер',c23)
        sql = "INSERT INTO accound (`data_id`,`name`,`info`,`status`) VALUES (0,'Имя','{}','')".format (phone_number)
        cursor.execute(sql)
        db.commit()    
        lastid = cursor.lastrowid
        sql = "UPDATE accound SET data_id = {0} WHERE id = {1}".format (lastid,lastid)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO accound (`data_id`,`name`,`info`,`status`) VALUES ({0},'Токен','{1}','')".format (lastid,string)
        cursor.execute(sql)
        db.commit()    
        #lastid = cursor.lastrowid
    else:    
        print (c2,'        [+] Данный аккаунт найдей в базе TELEGRAM. ',c23)
        
    print ('         [+] Проверяем наличее в базе: PING')
    connect_info['database'] = 'ping314_bot'    
    db,cursor = connect (connect_info)
    sql = "select A1.id as id,A1.info as name,A2.info as session from accound as A1,accound as A2 where A1.name = 'Имя' and A1.id = A2.data_id and A2.name = 'Токен' and A1.info = '{}'".format (phone_number)
    cursor.execute(sql)
    results = cursor.fetchall()    
    id = 0
    for row in results:
        id,name,session = row.values()
        print ('            [+] № {:0>4d}, тел: {:^17}'.format(1,row['name']))
    if id == 0:
        print (c3,'        [+] Данный аккаунт не найдей в базе PING. Записываем данный номер',c23)
        sql = "INSERT INTO accound (`data_id`,`name`,`info`,`status`) VALUES (0,'Имя','{}','')".format (phone_number)
        cursor.execute(sql)
        db.commit()    
        lastid = cursor.lastrowid
        sql = "UPDATE accound SET data_id = {0} WHERE id = {1}".format (lastid,lastid)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO accound (`data_id`,`name`,`info`,`status`) VALUES ({0},'Токен','{1}','')".format (lastid,string)
        cursor.execute(sql)
        db.commit()    
        #lastid = cursor.lastrowid
    else:    
        print (c2,'        [+] Данный аккаунт найдей в базе PING. ',c23)        
  
### Регистрация нового контакта
def function_add_contact (list_account,contact_user):
    #from telethon.sync import TelegramClient
    #from telethon import functions, types
    from telethon.tl.functions.contacts import ImportContactsRequest
    from telethon.tl.types import InputPhoneContact
    
    first_name = contact_user.setdefault('first_name','')
    last_name = contact_user.setdefault('last_name','')
    phone = contact_user.setdefault('phone','') 
    add_phone_privacy_exception = contact_user.setdefault('add_phone_privacy_exception',True)
    
    print ('    [+] Данные для отправки:',contact_user)    
    print ('    [+] phone:',phone)
    print ('    [+] first_name:',first_name)
    print ('    [+] last_name:',last_name)
    
    account = {'':'','':''}
    for account in list_account:
        client,answer = telegram_connect (account,api_id,api_hash)        
        contact = InputPhoneContact(client_id=0,phone=phone,first_name=first_name,last_name=last_name) # For new contacts you should use client_id = 0
        result = client(ImportContactsRequest([contact]))                
        print('[+]',result.stringify())
        
### Отправить сообщение клиенту
def function_send_message (list_account,contact_user,message):
    account = {'':'','':''}
    message_out = message.setdefault ('message','')
    picture     = message.setdefault ('picture','')
    for account in list_account:
        client,answer = telegram_connect (account,api_id,api_hash)
        for contact in contact_user:
            phone = contact.setdefault ('Телефон','')
            if message_out != '':
                result = client.send_message(phone, message_out)
                print('[+]',result.stringify())
            if picture != '':    
                result = client.send_file(phone, picture)
                print('[+]',result.stringify())
  
if __name__ == '__main__':
    print ('[+] Программа для работы с телеграмм аккаунтами')
    import configparser
    config = configparser.ConfigParser()
    config.read('settings.ini') 
    database = config.get('Settings', "database")
    host     = config.get('Settings', "host")
    user     = config.get('Settings', "user")
    password = config.get('Settings', "password")
    connect_info = {'host':host,'user':user,'password':password,'database':database}
    api_id       = config.get('Settings', "api_id")
    api_hash     = config.get('Settings', "api_hash")
    
    ### настройка цвета для вывода на экран
    c0  =  "\033[0;37m"  ## Белый
    c1  =  "\033[1;30m"  ## Черный
    c2  =  "\033[0;31m"  ## Красный
    c3  =  "\033[0;32m"  ## Зеленый
    c4  =  "\033[1;35m"  ## Magenta like Mimosa\033[1;m
    c5  =  "\033[1;33m"  ## Yellow like Yolk\033[1;m'
    c7  =  "\033[1;37m"  ## White
    c8  =  "\033[1;33m"  ## Yellow
    c9  =  "\033[1;32m"  ## Green
    c10 =  "\033[1;34m"  ## Blue
    c11 =  "\033[1;36m"  ## Cyan
    c12 =  "\033[1;31m"  ## Red
    c13 =  "\033[1;35m"  ## Magenta
    c14 =  "\033[1;30m"  ## Black
    c15 =  "\033[0;37m"  ## Darkwhite
    c16 =  "\033[0;33m"  ## Darkyellow
    c17 =  "\033[0;32m"  ## Darkgreen
    c18 =  "\033[0;34m"  ## Darkblue
    c19 =  "\033[0;36m"  ## Darkcyan
    c20 =  "\033[0;31m"  ## Darkred
    c21 =  "\033[0;35m"  ## Darkmagenta
    c22 =  "\033[0;30m"  ## Darkblack
    c23 =  "\033[0;0m"   ## Off

    #print (c8,'[+] Регистрация нового клиента',c23)
    #phone_number = '+79198670550'
    #function_reg_new_account (phone_number)
    
    print (c8,'   [+] Загружаем все аккаунты системы',c23) 
    list_account = function_list_account()
    print ('[+] list_account:',list_account)
    
    #print (c8,'   [+] Тестирование списка аккаунтов',c23) 
    #function_test_accound(list_account)

    print (c8,'[+] Добавление нового контакта в телеграмм',c23)
    first_name = 'Vadim11117'
    last_name = 'Kupinov777'
    phone = '+447435012955'
    add_phone_privacy_exception = True    
    contact_user = {'id':id,'first_name':first_name,'last_name':last_name,'phone':phone,'add_phone_privacy_exception':add_phone_privacy_exception} 
    function_add_contact (list_account,contact_user)
    
    print (c8,'   [+] Отправить сообщение по телефону',c23)     
    contact_user = [{'Телефон':phone}]
    message = {'message':'Проверка связи','picture':'test.jpg'}
    function_send_message (list_account,contact_user,message)





