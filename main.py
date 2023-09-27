from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import sqlite3
app = FastAPI()
server = sqlite3.connect('db.db', check_same_thread=False)
cursor = server.cursor()


@app.get('/items')
async def items_get():
    # 컬럼명 불러오기
    server.row_factory = sqlite3.Row
    # 현재 커서의 위치 업데이트
    cursor = server.cursor()

    # 모든 쿼리 데이터 가져오기
    main_push = cursor.execute(f"""
                          SELECT * FROM items
                          """).fetchall()
    return JSONResponse(jsonable_encoder(dict(push) for push in main_push))    
# ex) main_push를 컬럼명 없이 그냥 가져왔을시 [1, 시후급처, 시후급처합니다] 이런식으로 배열로 올텐데
#     로우팩토리를 포함해서 가져올경우 [[id:1], [title:시후급처], [description:시후급처합니다]]
#     이런식으로 각각의 배열로 올수있게된다 거기에 dict(push) for push in main_push로 
#     각각의 main_push의 배열들을 돌면서 dict 객체화 시켜준다 그러면
#     {id:1, title:'시후' ...}  이런식으로 변경되서 올것이다 

@app.post('/items')
async def create_item(image:UploadFile, title:Annotated[str,Form()], price:Annotated[int,Form()], 
                description:Annotated[str,Form()], place:Annotated[str,Form()],
                insertAT:Annotated[int,Form()]
                ):
    image_big = await image.read()
    server.execute(f"""
                   INSERT INTO items(title,image,price,description,place,insertAT)
                   VALUES ('{title}','{image_big.hex()}',{price},
                   '{description}','{place}','{insertAT}')
                   """)
    server.commit()
    # print(image,title,price,description,place)
    return '200'

@app.post('/itemss')
async def eng(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAT:Annotated[int,Form()]
                ):
    image_big = await image.read()
    server.execute(f"""
                   INSERT INTO items(title,image,price,description,place,insertAT)
                   VALUES ('{title}','{image_big.hex()}',{price},'{description}','{place}','{insertAT}')
                   """)
    server.id
    server.commit()
    return '시후'

@app.get('/images/{}')

#  ('/image/{id}') id부분에 쓴건 아래쪽 같은 단어인 id로 전달됏다 다르게쓰면 안댐
@app.get('/image/{id}')
async def get_img(id):
     cursor = server.cursor()
     img_chan = cursor.execute(f"""
                   SELECT image FROM items WHERE id={id}
                   """).fetchone()[0]
     
     return Response(content=bytes.fromhex(img_chan))
    
    
    
    
# @app.get('/users')
# async def users_get():
#     # 컬럼명 불러오기
#     server.row_factory = sqlite3.Row
#     # 현재 커서의 위치 업데이트
#     cursor = server.cursor()

#     # 모든 쿼리 데이터 가져오기
#     main = cursor.execute(f"""
#                           SELECT id FROM users
#                           """).fetchall()
#     print(main)
#     return main
# cursor.execute(f"SELECT * FROM users WHERE id = 'sihusdee'")
# existing_user = cursor.fetchone()  # 존재하는 경우, 사용자 레코드를 가져옵니다.

# if existing_user:
#     # 이미 있는 아이디인 경우
#     print('이미 존재하는 아이디입니다.')
#     # 다른 처리를 수행하거나 에러 메시지를 반환할 수 있습니다.
# else:
#     # 아이디가 존재하지 않는 경우, 새로운 사용자를 추가합니다.
#     # cursor.execute(f'''
#     #                INSERT INTO users(id, password, name, email)
#     #                VALUES ('{id}', '{password}', '{name}', '{email}')
#     #                ''')
#     # server.commit()
#     print('회원 가입이 완료되었습니다.')


@app.post('/signup')
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           password_hagin:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cursor.execute(f"SELECT * FROM users WHERE id = '{id}'")
    existing_user = cursor.fetchone() 
    if existing_user:
        return '아이디'
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    existing_user2 = cursor.fetchone() 
    if existing_user2:
        return '이메일'
    cursor.execute(f'''
                   INSERT INTO users(id,password,name,email)
                   VALUES ('{id}','{password}','{name}','{email}')
                   ''')
    # print(id,password_hagin)
    server.commit()
    return '싸인업'
# @app.get('/items')
# async def items_get():
#     # 컬럼명 불러오기
#     server.row_factory = sqlite3.Row
#     # 현재 커서의 위치 업데이트
#     cursor = server.cursor()

#     # 모든 쿼리 데이터 가져오기
#     main_push = cursor.execute(f"""
#                           SELECT * FROM items
#                           """).fetchall()
#     return JSONResponse(dict(push) for push in main_push)



app.mount("/", StaticFiles(directory="frontend",html=True), name="dangggn")
