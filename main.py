from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gigs in Nairobi.\nAdmission Number: C027-01-0863/2024",
    version="1.0.0"
)

gigs_db = [
    {
        "id": 1,
        "title": "Social Media Marketing Campaign",
        "description": "Create and manage a one-month social media marketing campaign for a Nairobi clothing brand.",
        "category": "Marketing",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Alec Benjamin"
    },
    {
        "id": 2,
        "title": "Sales Data Analysis",
        "description": "Analyze monthly sales data and prepare a dashboard with key performance indicators.",
        "category": "Data",
        "budget": 22000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Birdy Astrid"
    },
    {
        "id": 3,
        "title": "Business Strategy Consultation",
        "description": "Provide business consulting services for a startup looking to expand into new markets.",
        "category": "Consulting",
        "budget": 30000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Irene Wanja"
    },
    {
        "id": 4,
        "title": "SEO Marketing Audit",
        "description": "Review website SEO performance and recommend strategies to improve search rankings.",
        "category": "Marketing",
        "budget": 18000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Ken Kimani"
    },
    {
        "id": 5,
        "title": "Customer Data Cleaning",
        "description": "Clean and organize customer records for better reporting and analysis.",
        "category": "Data",
        "budget": 12000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Samuel Gichuki"
    },
    {
        "id": 6,
        "title": "Financial Consulting",
        "description": "Advise a small business on budgeting and financial planning for the next financial year.",
        "category": "Consulting",
        "budget": 27000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jessicah Mwende"
    },
    {
        "id": 7,
        "title": "Email Marketing Setup",
        "description": "Create automated email marketing campaigns using Mailchimp for an online store.",
        "category": "Marketing",
        "budget": 14000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "John Wambua"
    },
    {
        "id": 8,
        "title": "Market Research Analysis",
        "description": "Collect and analyze competitor market data to support business decision-making.",
        "category": "Data",
        "budget": 25000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Peter Mike"
    }
]
class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: Literal["Marketing", "Data", "Consulting"]
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None



@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):
    """
    Retrieve all gigs with optional filtering.
    """

    results = gigs_db

    if category:
        results = [
            gig for gig in results
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] <= max_budget
        ]

    return results



@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Return a single gig by ID.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search gigs by title.
    """
    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results



@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig.
    """

    new_id = max([g["id"] for g in gigs_db]) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """

    # Find the gig
    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            # Update budget if provided
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            # Update status if provided
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig by its ID.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """

    # Find the gig
    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            # Update the budget if provided
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            # Update the status if provided
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")