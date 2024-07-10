# imports
from ctypes import ArgumentError
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from config import Tashkent_tz
from models import AssignmentTable
from database import engine, SessionLocal
import models, schemas, crud
from sqlalchemy.orm import Session
from sqlalchemy.exc import ArgumentError


# views
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Todo Project")

@app.middleware("http")
async def db_session_middleware(request:Request, call_next):
    response = Response("Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db(request:Request):
    return request.state.db


@app.get("/", response_model=list[schemas.ResponseAssignmentSchema])
async def get_assignment(db:Session=Depends(get_db)):
    db_assignment = crud.get_assignment(db=db)
    return db_assignment

@app.post("/", response_model=schemas.CrudAssignmentSchema)
async def create_assignment(assignment:schemas.CrudAssignmentSchema,db:Session=Depends(get_db)):
    return crud.create_assignment(db=db, assignment=assignment)

@app.delete("/assignment/{assignment_id}", response_model=schemas.CrudAssignmentSchema)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(AssignmentTable).filter(AssignmentTable.id == assignment_id).first()
    print(db_assignment)
    if db_assignment:
        db.delete(db_assignment)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Assignment successfully delete"}


@app.put("/assignment/{assignment_id}", response_model=schemas.UpdateAssignmentSchema)
def update_assignment(assignment_id: int, assignment: schemas.UpdateAssignmentSchema, db: Session = Depends(get_db)):
    db_assignment = db.query(AssignmentTable).filter(AssignmentTable.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Item not found")
    db_assignment.title = assignment.title
    db_assignment.description = assignment.description
    db_assignment.priority = assignment.priority
    db_assignment.the_nadir = assignment.the_nadir
    db_assignment.is_complete = assignment.is_complete
    db_assignment.updated_at = datetime.now(tz=Tashkent_tz)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment