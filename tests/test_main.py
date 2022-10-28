import pytest
import pygame_menu
import mapMenu as mapMenu
from mapMenu import loadPNG, changeShip, saveMap, getShipMenu 
from game import socketConnected, downloadMap, closeConnected


# Модульный тест!
def test_loadPNG():
    pngMap = []
    pngMap = loadPNG(pngMap)
    assert len(pngMap) != 0

@pytest.mark.parametrize("exception, argument", [(AttributeError, 2),
                                                 (AttributeError, '2'),
                                                 (AttributeError, ' ')])
def test_loadPNG_error(exception, argument):
    with pytest.raises(exception):
        loadPNG(argument)      

def test_loadPNG_error_2():
    with pytest.raises(TypeError):
        loadPNG()       

def test_socketConnected():
    port = open('port.txt', 'r', encoding = "utf-8").read()
    res = socketConnected(port)
    res[0] == 'connected'

def test_image():
    image = pygame_menu.baseimage.BaseImage('map/ultima.png')
    widgetImage = pygame_menu.widgets.Image(image)
    changeShip('map/ultima.png', widgetImage)
    assert widgetImage.get_image().get_path() == image.get_path()
    
# Интеграционный тест
# проверка того, что выбрав картинку в меню map она же загрузится в окне game
def test_saveMap_downloadMap():   
    assert saveMap("ultraTestoWesto.svg") == downloadMap()

def test_saveMap_downloadMap_error():
    with pytest.raises(AssertionError):
        assert saveMap("ul.jpg") == downloadMap()
        
# проверка того, что порт после закрытия изменился
def test_closeConnected():
    port = open('port.txt', 'r', encoding = "utf-8").read()
    assert  socketConnected(port)[1] != closeConnected(port)[0] - 1 and closeConnected(port)[1] == 'Сервер закрыт'
    


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

     


