[![Coverage Status](https://coveralls.io/repos/github/DenisKnaub/RageOfTeleshka/badge.svg?branch=main)](https://coveralls.io/github/DenisKnaub/RageOfTeleshka?branch=main)
#Тестирование приложения "Робот тележка" с помощью библиотеки pytest
Приложение эмулирует работу робота тележки. На робот есть возможность установить датчик столкновения, дальномер и т.д. Добавить карту в формате __.svg__

__Pytest__ - это платформа тестирования программного обеспечения, основанная на языке программирования Python. Он может быть использован для написания различных типов тестов программного обеспечения, включая модульные тесты, интеграционные тесты, сквозные тесты и функциональные тесты.

##Было реализовано 14 тестов:
___Тест 1.___
```python
def test_loadPNG():
    pngMap = []
    pngMap = loadPNG(pngMap)
    assert len(pngMap) != 0
```
Тест вызывает функцию __loadPNG__ и проверяет, что массив с картами будет не пустой, для скрола карт.
```python
def loadPNG(pngMap): # загружаем автоматически все картинки для отображения в меню Карт
    i = 1 # номер элемента картинки
    for filename in glob.glob('map\*.png'): 
        pngMap.append((filename[4:] ,filename[:3] + "/" +  filename[4:])) # заносим все картинки в массив
        i+=1
    return pngMap
```

___Тест 2-5.___
```python
@pytest.mark.parametrize("exception, argument", [(AttributeError, 2),
                                                 (AttributeError, '2'),
                                                 (AttributeError, ' ')])
def test_loadPNG_error(exception, argument):
    with pytest.raises(exception):
        loadPNG(argument)

def test_loadPNG_error_2():
    with pytest.raises(TypeError):
        loadPNG() 
```
Тест вызывает функцию __loadPNG__ и принимает в качестве параметров неверный тип переменных, в результате работы ловит ошибку.
```python
def loadPNG(pngMap): # загружаем автоматически все картинки для отображения в меню Карт
    i = 1 # номер элемента картинки
    for filename in glob.glob('map\*.png'): 
        pngMap.append((filename[4:] ,filename[:3] + "/" +  filename[4:])) # заносим все картинки в массив
        i+=1
    return pngMap
```
___Тест 6.___
```python
def test_socketConnected():
    port = open('port.txt', 'r', encoding = "utf-8").read()
    res = socketConnected(port)
    res[0] == 'connected' 
```
Тест вызывает функцию __socketConnected(port)__ передвая параметр номер порта для подключения сокета. В случае успешного подключения выводит сообщение о подключении.
```python
def socketConnected(port):
    ############### Подключение Сокет Сервер 
    os.system("start python client.py") # запускаем клиента в отдельном окне
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет
    sock.bind(('', int(port))) # свяжем наш сокет с данными хостом и портом (9090) с помощью метода bind
    sock.listen(1) # С помощью метода listen мы запустим для данного сокета режим прослушивания, очередь
    global conn
    global cl
    conn, addr = sock.accept() # принять подключение с помощью метода accept, который возвращает кортеж с двумя элементами: новый сокет и адрес клиента    
    print ('connected:', addr)
    cl = 'Close'
    return 'connected', port, conn
```
___Тест 7.___
```python
def test_image():
    image = pygame_menu.baseimage.BaseImage('map/ultima.png')
    widgetImage = pygame_menu.widgets.Image(image)
    changeShip('map/ultima.png', widgetImage)
    assert widgetImage.get_image().get_path() == image.get_path() 
```
Тест вызывает функцию __changeShip('map/ultima.png', widgetImage)__ передавая в качестве параметров путь до карты и виджет. Результат теста, правильность выбора карт в скроле.
```python
def changeShip(path, widget):
    print(path)
    global shipFile
    shipFile = path
    widget.set_image(pygame_menu.baseimage.BaseImage(path))
```
___Тест 8-9.___
```python
def test_saveMap_downloadMap():   
    assert saveMap("ultraTestoWesto.svg") == downloadMap()

def test_saveMap_downloadMap_error():
    with pytest.raises(AssertionError):
        assert saveMap("ul.jpg") == downloadMap()
```
Тест вызывает функции __saveMap("ultraTestoWesto.svg")__ и __downloadMap()__ передавая в качестве параметра имя выбранной карты. Результат теста, сохраненная карта загружается в окне эмуляции.
Отрицательный тест вызывает функцию __saveMap("ul.jpg")__ сохраняя не существующую карту. Результат AssertionError
```python
def saveMap(shipFile):
    settings = shipFile
    with open('settings.txt', 'w') as f: # заносим в файл с выбранной картой
      f.write(settings)
    f.close()
    return settings

def downloadMap():
    # загружаем сохранённую карту
    global file
    file = open('settings.txt', 'r', encoding = "Windows-1251").read().split('.')
    file = file[0] +'.svg'
    print(file)
    return file
```
___Тест 10.___
```python
# проверка того, что порт после закрытия изменился
def test_closeConnected():
    port = open('port.txt', 'r', encoding = "utf-8").read()
    assert  socketConnected(port)[1] != closeConnected(port)[0] - 1 and closeConnected(port)[1] == 'Сервер закрыт'
```
Тест вызывает функции __socketConnected(port)__ и __closeConnected(port))__ передавая в качестве параметра порт. Результат, порт после закрытия должен отличаться. Оповещение о закрытие сокета.
```python
def socketConnected(port):
    os.system("start python client.py") # запускаем клиента в отдельном окне
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет
    sock.bind(('', int(port)))
    sock.listen(1) 
    global conn
    global cl
    conn, addr = sock.accept()   
    print ('connected:', addr)
    cl = 'Close'
    return 'connected', port, conn

def closeConnected(port):
    # обновляем порт для следующего запуска    
    port1 = int(port) - 1 # удаляю по 1 чтобы был новый порт в следующий раз
    with open('port.txt', 'w') as f:
          f.write(str(port1))
    f.close()
    conn.close() # закрываем сервер
    print ('Сервер закрыт')
    return port1, "Сервер закрыт"
```
___Тест 11-14.___
```python
@pytest.mark.parametrize("i, inp, out", [(1, "True", "0000"),
                                                 (2, "True", "1111"),
                                                 (2, "False", "1100"),
                                                 (2, "Close", "Close")])

def test_client(i, inp, out):
    port = open('port.txt', 'r', encoding = "utf-8").read()
    conn = socketConnected(port)[2]
    for i in range(i):
        conn.send(inp.encode())
        data = conn.recv(1024)
    closeConnected(port)
    assert data.decode() == out
```
Тест эмулирует показания с датчиков и получением команд для передвижения и закрытие сокета.
```python
while True:
         
    if data.decode().split(',')[0] == 'Close': # если пришло сообщение о закртии окна эмуляции, выходим из цикла
        break
    
    if (data.decode().split(',')[0] == 'True'): # проезд свободен
        sock.send(forward.encode()) # отправляем сообщение

    if (data.decode().split(',')[0] == 'False'): # ударились в стену
        sock.send(right.encode()) # отправляем сообщение    
    
    if (data.decode() == 'Stop'): 
        sock.send(stop.encode()) # отправляем сообщение
        
    data = sock.recv(1024) # получаем сообщение от сервера
    print(f'Получил client ' + str(data))
```
