from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.schemas.ticket import TicketCreate, TicketResponse
from api.dependencies import get_current_user
from api.models.user import User
from api.models.ticket import Ticket


router = APIRouter(prefix="/tickets", tags=["Tickets"])

# Creating a support ticket
@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_data:TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Logic to create a ticket
    new_ticket=Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        status="OPEN",
        created_by=current_user.id 
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

# Getting all tickets submitted by the authenticated user
@router.get("/my-tickets", response_model=list[TicketResponse])
def get_my_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tickets = (db.query(Ticket).filter(Ticket.created_by==current_user.id).all())
    return tickets

# Getting all tickets submitted by all users
@router.get("/all", response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db), current_user:dict=Depends(get_current_user)):
    tickets = db.query(Ticket).order_by(Ticket.id.desc()).all()
    return tickets

# Getting a single ticket submitted by specific user
@router.get("/{ticket_id}", response_model=TicketResponse)
def get_single_ticket(ticket_id:int, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    single_ticket=db.query(Ticket).filter(Ticket.id==ticket_id, Ticket.created_by==current_user.id).first()
    if not single_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return single_ticket

