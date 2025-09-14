from conf import app, Request, JSONResponse
import requests

@app.middleware("http")
async def IsAuthenticated(request: Request, call_next) :
        
    response = await call_next(request)
    token_headers = request.headers.get('Authorization', None)

    if not token_headers:
        return JSONResponse({
            'message' : "Unauhtorized"
        }, status_code=401)
    
    token  = token_headers.split(' ')[-1]
    print(f"{token=}")
    req = requests.post(
        'http://web:8000/users/auth/tokens/verify/v1/',
        data={
            'token' : token
        }
    )

    if req.status_code != 200 :
        return JSONResponse({
            'message' : "Unauhtorized"
        }, status_code=401)
    
    
    
    return response