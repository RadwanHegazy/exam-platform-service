from conf import app, redis_client

@app.get('/exam/{exam_id}/qs')
async def exam_qs (exam_id) : 
    key = f'exam_{exam_id}_qs'
    exam_qs = redis_client.get(key)
    return exam_qs or []