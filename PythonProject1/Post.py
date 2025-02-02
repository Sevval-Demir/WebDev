from fastapi import FastAPI,Body

app=FastAPI()

courses_db=[
    {'id':1,'instructor':'Atil','title':'Python','category':'Development'},
    {'id':2,'instructor':'Ahmet','title':'Java','category':'Development'},
    {'id':3,'instructor':'Zeynep','title':'Jenkins','category':'Devops'},
    {'id':4,'instructor':'Fatma','title':'Kubernetes','category':'Devops'},
    {'id':5,'instructor':'Sevval','title':'Machine Learning','category':'AI'},
    {'id':6,'instructor':'Atlas','title':'Deep Learning','category':'AI'},
]

@app.post("/courses/create_course")
async def create_course(new_course=Body()):
    courses_db.append(new_course)