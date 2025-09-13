from redis import Redis
from fastapi import Request, FastAPI

app = FastAPI()
redis_client = Redis(host='redis', port=6379, db=0)


# TODO:
# 1. create custom middleware for authentication
# 2. add validation for check the exam is belongs to the current student
# 3. create login for student
# 4. create get all exam for current student 

@app.middleware("http")
async def IsAuthenticated(request: Request, call_next) -> bool:
    response = await call_next(request)
    token_headers = request.headers.get('Authorization', None)
    if not token_headers:
        response.status_code = 401
        response.body = b'Unauthorized'
        return response
    
    # Complete the full logic here
    
    return response

@app.get('/exam/{exam_id}')
async def exam (exam_id) : 
    key = f'exam_{exam_id}'
    exam = redis_client.get(key)
    return exam or {}

@app.get('/exam/{exam_id}/qs')
async def exam_qs (exam_id) : 
    key = f'exam_{exam_id}_qs'
    exam_qs = redis_client.get(key)
    return exam_qs or []

