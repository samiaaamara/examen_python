from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq  # Assure-toi que ce package est installé

from pydantic import BaseModel

from app import models, schemas, database  # IMPORTS ABSOLUS

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise RuntimeError("La clé API Groq est manquante dans le fichier .env")

llm = ChatGroq(api_key=groq_api_key, model="mixtral-8x7b-32768", temperature=0.7)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Création automatique des tables
models.Base.metadata.create_all(bind=database.engine)

@app.post("/movies/", response_model=schemas.Movie)
def create_movie_with_actors(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(title=movie.title, year=movie.year, director=movie.director)
    db.add(db_movie)
    db.flush()

    for actor_data in movie.actors:
        db_actor = models.Actor(actor_name=actor_data.actor_name, movie_id=db_movie.id)
        db.add(db_actor)

    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/random/", response_model=schemas.Movie)
def get_random_movie(db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .options(joinedload(models.Movie.actors))
        .order_by(func.random())
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found")
    return movie

class SummaryRequest(BaseModel):
    movie_id: int

class SummaryResponse(BaseModel):
    summary_text: str

@app.post("/generate_summary/", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .options(joinedload(models.Movie.actors))
        .filter(models.Movie.id == request.movie_id)
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    actor_names = ", ".join(actor.actor_name for actor in movie.actors)

    prompt_template = PromptTemplate(
        input_variables=["title", "year", "director", "actor_list"],
        template=(
            "Generate a short, engaging summary for the movie '{title}' ({year}), "
            "directed by {director} and starring {actor_list}."
        )
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    summary = chain.run(
        title=movie.title,
        year=movie.year,
        director=movie.director,
        actor_list=actor_names
    )

    return SummaryResponse(summary_text=summary)
