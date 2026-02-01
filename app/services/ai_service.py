import google.generativeai as genai
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from app.schemas.cotizacion import Cotizacion
from app.schemas.servicio import Servicio
from app.schemas.equipo import Equipo

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# model = genai.GenerativeModel('gemini-1.5-flash')
model = genai.GenerativeModel('gemini-pro')

def get_context(db: Session) -> str:
    # Retrieve relevant data for context
    # Limiting to recent items to avoid token limits detailed info
    servicios = db.exec(select(Servicio).limit(10)).all()
    equipos = db.exec(select(Equipo).limit(10)).all()
    
    context_str = "Available Services:\n"
    for s in servicios:
        context_str += f"- {s.nombre}: {s.descripcion} (${s.precio})\n"
        
    context_str += "\nRegistered Equipment Types:\n"
    for e in equipos:
        context_str += f"- {e.marca} {e.modelo} ({e.tipo_equipo_id})\n"
        
    return context_str

async def generate_chat_response(query: str, db: Session) -> str:
    context = get_context(db)
    
    prompt = f"""
    You are a helpful AI assistant for a computer service center.
    Use the following context to answer the user's question.
    If the answer is not in the context, guide the user on how to contact support or visit the center.
    
    Context:
    {context}
    
    User Question: {query}
    
    Answer:
    """
    
    response = model.generate_content(prompt)
    return response.text
