import json
from aiohttp import web, ClientSession
import socket
import aiohttp
import aiohttp_cors
import routeros_api



def ConnectToRouter():
    global routerAPI
    connection = routeros_api.RouterOsApiPool(
    host='192.168.88.1',
    username='wifiapi',
    password='wifilogin',
    plaintext_login=True)
    routerAPI = connection.get_api()


async def getip(request):
    ip, mac = request.remote
    return web.Response(text=f"IP: {ip}, MAC: {mac}")


async def Create_API_Login(request):
    try:
        global routerAPI
        print(request)
        # Trích xuất dữ liệu của request từ json thành dict
        dataRequest = await request.json()
        # Tách dữ liệu thành các biến
        username = dataRequest["user"]
        password = dataRequest["password"]
        mac = dataRequest["mac-address"]
        ip = dataRequest["ip"]  

        login = routerAPI.get_resource('/ip/hotspot/active')
        params = {
            'user': str(username),
            'password': str(password),
            'mac-address': str(mac),
            'ip': str(ip),
        }
        # Gọi lệnh đăng nhập vào router
        login.call('login', params)
        print("Login thành công\n\n\n")
        # Thông báo nếu đăng nhập thành công
        return web.HTTPOk(text="Login thành công")
    except Exception as ex:
        print(ex)
        # Kiểm tra lý do gây lỗi
        return web.HTTPInternalServerError(text=str(ex))


def login_wifi_app():
    try:
        global app
        ConnectToRouter()
        app = web.Application()
        app.add_routes([web.get('/ip', getip),
                        web.post('/login', Create_API_Login)])
        addCorsToServer(app)
        web.run_app(app,port=8000)
    except Exception as ex:
        print(ex)

app = web.Application()
app.add_routes([
    web.get('/ip', getip),
    web.post('/login', Create_API_Login),
])

def addCorsToServer(app: web.Application):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)


ConnectToRouter()
                

if __name__ == '__main__':
    web.run_app(app)
