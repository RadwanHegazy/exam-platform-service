from ..conf import app, redis_client, JSONResponse

# @app.get('/exam/{exam_id}')
# async def exam (exam_id) : 
#     key = f'exam_{exam_id}'
#     exam = redis_client.get(key)
#     return exam or JSONResponse({
#         'message' : "exam not found"
#     }, status_code=404)
