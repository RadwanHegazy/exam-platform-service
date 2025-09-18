from .conf import app, JSONResponse, Request, Form
from .models import StudentAnswer


@app.post('/solver')
def save_student_answer(
    request : Request,
    question_id: int = Form(...),
    answer: str = Form(...),
    exam_id: int = Form(...),
) : 
    
    try : 
        headers = request.headers.get('Authorization', None)

        model =  StudentAnswer(
            question_id=question_id,
            answer=answer,
            student_jwt=headers.split(' ')[-1],
            exam_id=exam_id
        )

        model.save_to_cassandra()

        return JSONResponse({
            'messaage' : "Answer saved successfully",
        }, status_code=201)
    except Exception as e :
        print('exception : ', e)
        return JSONResponse({
            'message' : "An error occurred, Please try again, error : " + str(e)
        }, status_code=400)