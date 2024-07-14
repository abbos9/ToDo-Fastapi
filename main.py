# imports
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from config import Tashkent_tz
from models import AssignmentTable, Users
from database import engine, SessionLocal
import models, schemas, crud
from sqlalchemy.orm import Session
import auth
from auth import get_current_user

# views
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Todo Project")
app.include_router(auth.router)

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

user_depency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]



@app.get("/", response_model=list[schemas.ResponseAssignmentSchema], status_code=status.HTTP_200_OK)
async def get_assignments(db: Session = Depends(get_db)):
    db_assignments = crud.get_assignment(db=db)
    return db_assignments


@app.post("/", response_model=schemas.CrudAssignmentSchema,status_code=status.HTTP_201_CREATED)
async def create_assignment(assignment:schemas.CrudAssignmentSchema,db:db_dependency,current_user: Annotated[Users, Depends(get_current_user)]):
    if current_user["role"] != "PM":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")
    return crud.create_assignment(db=db, assignment=assignment, owner_id=current_user["id"])


@app.delete("/assignment/{assignment_id}", response_model=schemas.CrudAssignmentSchema, status_code=status.HTTP_404_NOT_FOUND)
def delete_assignment(assignment_id: int, db: db_dependency,current_user: Annotated[Users, Depends(get_current_user)]):
    if current_user["role"] != "PM":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")
    db_assignment = db.query(AssignmentTable).filter(AssignmentTable.id == assignment_id).first()
    print(db_assignment)
    if db_assignment:
        db.delete(db_assignment)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Assignment successfully delete"}


@app.put("/assignment/{assignment_id}", response_model=schemas.UpdateAssignmentSchema,status_code=status.HTTP_201_CREATED)
def update_assignment(assignment_id: int, assignment: schemas.UpdateAssignmentSchema, db: db_dependency,current_user: Annotated[Users, Depends(get_current_user)]):
    if current_user["role"] not in ["employee", "developer", "PM"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")
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