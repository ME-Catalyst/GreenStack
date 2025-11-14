"""
Ticket/Bug Tracking System API Routes
Handles ticket CRUD operations, comments, and CSV export
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3
import csv
import io

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

DB_PATH = "iodd_manager.db"


# Pydantic models for request/response
class TicketCreate(BaseModel):
    device_type: str  # 'EDS' or 'IODD'
    device_id: Optional[int] = None
    device_name: Optional[str] = None
    vendor_name: Optional[str] = None
    product_code: Optional[int] = None
    title: str
    description: Optional[str] = None
    eds_reference: Optional[str] = None
    priority: str = "medium"  # low, medium, high, critical
    category: Optional[str] = None


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    eds_reference: Optional[str] = None
    status: Optional[str] = None  # open, in_progress, resolved, closed, wont_fix
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[str] = None


class CommentCreate(BaseModel):
    comment_text: str
    created_by: Optional[str] = None


def generate_ticket_number(conn):
    """Generate a unique ticket number like TICKET-0001"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets")
    count = cursor.fetchone()[0]
    return f"TICKET-{str(count + 1).zfill(4)}"


def get_ticket_with_details(conn, ticket_id: int):
    """Get ticket with all comments"""
    cursor = conn.cursor()

    # Get ticket
    cursor.execute("""
        SELECT id, ticket_number, device_type, device_id, device_name, vendor_name,
               product_code, title, description, eds_reference, status, priority,
               category, created_at, updated_at, resolved_at, created_by, assigned_to
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()
    if not ticket:
        return None

    # Get comments
    cursor.execute("""
        SELECT id, comment_text, created_at, created_by
        FROM ticket_comments
        WHERE ticket_id = ?
        ORDER BY created_at ASC
    """, (ticket_id,))

    comments = cursor.fetchall()

    return {
        'id': ticket[0],
        'ticket_number': ticket[1],
        'device_type': ticket[2],
        'device_id': ticket[3],
        'device_name': ticket[4],
        'vendor_name': ticket[5],
        'product_code': ticket[6],
        'title': ticket[7],
        'description': ticket[8],
        'eds_reference': ticket[9],
        'status': ticket[10],
        'priority': ticket[11],
        'category': ticket[12],
        'created_at': ticket[13],
        'updated_at': ticket[14],
        'resolved_at': ticket[15],
        'created_by': ticket[16],
        'assigned_to': ticket[17],
        'comments': [
            {
                'id': c[0],
                'comment_text': c[1],
                'created_at': c[2],
                'created_by': c[3]
            } for c in comments
        ]
    }


@router.get("")
async def list_tickets(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    device_type: Optional[str] = Query(None, description="Filter by device type (EDS/IODD)"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    """List all tickets with optional filters"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    query = """
        SELECT id, ticket_number, device_type, device_id, device_name, vendor_name,
               product_code, title, description, eds_reference, status, priority,
               category, created_at, updated_at, resolved_at, created_by, assigned_to
        FROM tickets
        WHERE 1=1
    """
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    if device_type:
        query += " AND device_type = ?"
        params.append(device_type)

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    tickets = cursor.fetchall()
    conn.close()

    return [
        {
            'id': t[0],
            'ticket_number': t[1],
            'device_type': t[2],
            'device_id': t[3],
            'device_name': t[4],
            'vendor_name': t[5],
            'product_code': t[6],
            'title': t[7],
            'description': t[8],
            'eds_reference': t[9],
            'status': t[10],
            'priority': t[11],
            'category': t[12],
            'created_at': t[13],
            'updated_at': t[14],
            'resolved_at': t[15],
            'created_by': t[16],
            'assigned_to': t[17],
        } for t in tickets
    ]


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int):
    """Get a single ticket with all comments"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    ticket = get_ticket_with_details(conn, ticket_id)
    conn.close()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.post("")
async def create_ticket(ticket: TicketCreate):
    """Create a new ticket"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    now = datetime.now().isoformat()
    ticket_number = generate_ticket_number(conn)

    cursor.execute("""
        INSERT INTO tickets (
            ticket_number, device_type, device_id, device_name, vendor_name,
            product_code, title, description, eds_reference, status, priority,
            category, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_number,
        ticket.device_type,
        ticket.device_id,
        ticket.device_name,
        ticket.vendor_name,
        ticket.product_code,
        ticket.title,
        ticket.description,
        ticket.eds_reference,
        'open',
        ticket.priority,
        ticket.category,
        now,
        now
    ))

    ticket_id = cursor.lastrowid
    conn.commit()

    result = get_ticket_with_details(conn, ticket_id)
    conn.close()

    return result


@router.patch("/{ticket_id}")
async def update_ticket(ticket_id: int, update: TicketUpdate):
    """Update a ticket"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Check if ticket exists
    cursor.execute("SELECT id, status FROM tickets WHERE id = ?", (ticket_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    now = datetime.now().isoformat()
    updates = []
    params = []

    if update.title is not None:
        updates.append("title = ?")
        params.append(update.title)

    if update.description is not None:
        updates.append("description = ?")
        params.append(update.description)

    if update.eds_reference is not None:
        updates.append("eds_reference = ?")
        params.append(update.eds_reference)

    if update.status is not None:
        updates.append("status = ?")
        params.append(update.status)

        # If status is resolved or closed, set resolved_at
        if update.status in ('resolved', 'closed'):
            updates.append("resolved_at = ?")
            params.append(now)

    if update.priority is not None:
        updates.append("priority = ?")
        params.append(update.priority)

    if update.category is not None:
        updates.append("category = ?")
        params.append(update.category)

    if update.assigned_to is not None:
        updates.append("assigned_to = ?")
        params.append(update.assigned_to)

    if not updates:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")

    updates.append("updated_at = ?")
    params.append(now)
    params.append(ticket_id)

    query = f"UPDATE tickets SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()

    result = get_ticket_with_details(conn, ticket_id)
    conn.close()

    return result


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int):
    """Delete a ticket"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    conn.commit()
    conn.close()

    return {"message": "Ticket deleted successfully"}


@router.post("/{ticket_id}/comments")
async def add_comment(ticket_id: int, comment: CommentCreate):
    """Add a comment to a ticket"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Check if ticket exists
    cursor.execute("SELECT id FROM tickets WHERE id = ?", (ticket_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO ticket_comments (ticket_id, comment_text, created_at, created_by)
        VALUES (?, ?, ?, ?)
    """, (ticket_id, comment.comment_text, now, comment.created_by))

    # Update ticket's updated_at
    cursor.execute("UPDATE tickets SET updated_at = ? WHERE id = ?", (now, ticket_id))

    conn.commit()

    result = get_ticket_with_details(conn, ticket_id)
    conn.close()

    return result


@router.get("/export/csv", response_class=None)
async def export_tickets_csv(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    device_type: Optional[str] = Query(None, description="Filter by device type"),
):
    """Export tickets to CSV"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build query
    query = """
        SELECT t.ticket_number, t.device_type, t.device_name, t.vendor_name, t.product_code,
               t.title, t.description, t.eds_reference, t.status, t.priority, t.category,
               t.created_at, t.updated_at, t.resolved_at, t.id
        FROM tickets t
        WHERE 1=1
    """
    params = []

    if status:
        query += " AND t.status = ?"
        params.append(status)

    if priority:
        query += " AND t.priority = ?"
        params.append(priority)

    if device_type:
        query += " AND t.device_type = ?"
        params.append(device_type)

    query += " ORDER BY t.created_at DESC"

    cursor.execute(query, params)
    tickets = cursor.fetchall()

    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'Ticket Number', 'Device Type', 'Device Name', 'Vendor', 'Product Code',
        'Title', 'Description', 'EDS Reference', 'Status', 'Priority', 'Category',
        'Created At', 'Updated At', 'Resolved At', 'All Comments'
    ])

    # Write tickets with comments
    for ticket in tickets:
        ticket_id = ticket[14]

        # Get all comments for this ticket
        cursor.execute("""
            SELECT comment_text FROM ticket_comments
            WHERE ticket_id = ?
            ORDER BY created_at ASC
        """, (ticket_id,))

        comments = cursor.fetchall()
        all_comments = " | ".join([c[0] for c in comments])

        writer.writerow([
            ticket[0],  # ticket_number
            ticket[1],  # device_type
            ticket[2],  # device_name
            ticket[3],  # vendor_name
            ticket[4],  # product_code
            ticket[5],  # title
            ticket[6],  # description
            ticket[7],  # eds_reference
            ticket[8],  # status
            ticket[9],  # priority
            ticket[10], # category
            ticket[11], # created_at
            ticket[12], # updated_at
            ticket[13], # resolved_at
            all_comments
        ])

    conn.close()

    # Return CSV as response
    from fastapi.responses import StreamingResponse
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets.csv"}
    )
