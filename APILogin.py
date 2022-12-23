from aiohttp import web
import socket
import aiohttp_cors
import routeros_api
import logging

ROUTER = '192.168.88.1'
USERNAME = 'wifilogin'
PASSWORD = 'wifiapi'
def ConnectToRouter(host: str, username: str, password: str):
    # Tạo global var
    global routerAPI
    # Tạo kết nối đến router với các parameter lấy được khi hàm được gọi
    connection = routeros_api.RouterOsApiPool(
        host=host,
        username=username,
        password=password,
        plaintext_login=True)
    # Kết nối
    routerAPI = connection.get_api()


async def getip(request):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return web.Response(text=ip)

async def Create_API_Login(request):
    try:
        global routerAPI
        dataRequest = await request.json()
        print(dataRequest)

        username = dataRequest["user"]
        password = dataRequest["password"]
        mac = dataRequest["mac-address"]
        ip = dataRequest["ip"]
        
        print("User: {username}\nIP: {ip}\nMAC: {mac}\nPasswd: {passwd}".format(username=username, ip=ip, mac=mac, passwd=password))
        print("Đang login vào router")
        login = routerAPI.get_resource('/ip/hotspot/active')
        params = {
            'user': str(username),
            'password': str(password),
            'mac-address': str(mac),
            'ip': str(ip),
        }
        # Gọi lệnh đăng nhập vào router
        login.call('login', params)

        logging.info('Login thành công!')
        return web.HTTPOk()
    except Exception as ex:
        print(ex)
        return web.HTTPNonAuthoritativeInformation(text=str(ex))


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

app = web.Application()
app.add_routes([
    web.get('/ip', getip),
    web.post('/login', Create_API_Login),
])

ConnectToRouter(host=ROUTER, username=USERNAME, password=PASSWORD)

if __name__ == '__main__':
    web.run_app(app)
