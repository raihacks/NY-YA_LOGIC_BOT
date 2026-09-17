from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Analysis
from schemas import ArgumentRequest, NyayaResult
from ai import analyze_argument


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Nyaya Logic Bot API",
    description="AI-powered Nyaya reasoning assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message": "Nyaya Logic Bot API is running"
    }


@app.post("/analyze", response_model=NyayaResult)
def analyze(
    argument: ArgumentRequest,
    db: Session = Depends(get_db)
):

    if not argument.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Argument cannot be empty."
        )

    try:
        result = analyze_argument(argument.text)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

    analysis = Analysis(
        user_input=argument.text,

        pratijna=result["pratijna"],
        hetu=result["hetu"],
        udaharana=result["udaharana"],
        upanaya=result["upanaya"],
        nigamana=result["nigamana"],

        explanation=result["explanation"],
        validity=result["validity"]
    )

    db.add(analysis)
    db.commit()

    return result


@app.get("/history")
def history(
    db: Session = Depends(get_db)
):

    analyses = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .limit(20)
        .all()
    )

    return [
        {
            "id": item.id,
            "input": item.user_input,
            "validity": item.validity,
            "created_at": item.created_at
        }
        for item in analyses
    ]