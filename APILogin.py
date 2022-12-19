import json
from aiohttp import web, ClientSession, BasicAuth
import socket
import aiohttp
import aiohttp_cors
import routeros_api



def ConnectToRouter():
    global routerAPI
    connection = routeros_api.RouterOsApiPool(
    '192.168.88.1',
    username='wifiapi',
    password='wifilogin',
    port = '',
    use_ssl=True,
    ssl_verify=False,
    ssl_verify_hostname=False,
    plaintext_login= True)
    routerAPI = connection.get_api()

async def hello(request):
    reqs = await request.json()
    text = "Hello, this is a test " + reqs['Ten']
    return web.Response(text=text)


async def getip(request):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return web.Response(text=ip)


# async def LogToServer(request):
#     reqs = await request.json()
#     print('vao duoc ham')
#     try:
       

async def Create_API_Login(request, username="", password = ""):
    try:
        global routerAPI
        url = 'https://tapi.lhu.edu.vn/nema/auth/CLB_Select_ThanhVien_byMSSV'
        auth = BasicAuth(username, password)

        async with ClientSession(auth= auth) as session:
            async with session.post(url,  json={'username': auth(username), 'password' : auth(password)}) as resp:
                print (resp)
                if resp.status == 200:
                    print('chay ra true')
                    data = await resp.json()
                    return web.Response(text=str(data))
                else:
                    print('chay ra false')
                    return False
    except Exception as err:
        print(str(err))
        return False



# async def LogToServer(request):
#     reqs = await request.json()
#     async with ClientSession() as session:
#         async with session.get('https://tapi.lhu.edu.vn/nema/auth/CLB_Select_ThanhVien_byMSSV', json = {"MSSV": reqs['MSSV'] }) as resp:
#             print(resp)
#             if resp.status == 200:
#                 print('chay dc nay')
#                 data = await resp.json()
#                 return web.Application(text = str(data))
#             else:
#                 print('Chay ra loi nay')
#                 return False 
#             pass
#         async with session.post('/post', data=b'data'):
#             pass
#         async with session.put('/put', data=b'data'):
#             pass


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
app.add_routes([web.post('/test', Create_API_Login), web.get('/hello', hello)
                ])
                

if __name__ == '__main__':
    web.run_app(app)
