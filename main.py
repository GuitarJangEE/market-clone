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
