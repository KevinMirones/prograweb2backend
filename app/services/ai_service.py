import google.generativeai as genai
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from app.schemas.cotizacion import Cotizacion
from app.schemas.servicio import Servicio
from app.schemas.equipo import Equipo

load_dotenv()

from google.ai.generativelanguage_v1beta.types import content
from app.services.tools import (
    create_client_tool, 
    create_service_tool,
    create_tipo_equipo_tool,
    create_tecnico_tool,
    create_equipo_tool,
    create_cotizacion_tool
)
from app.schemas.tipo_equipo import TipoEquipo
from app.schemas.tecnico import Tecnico
from app.schemas.cliente import Cliente

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Define the tools map for execution
available_tools = {
    "create_client": create_client_tool,
    "create_service": create_service_tool,
    "create_tipo_equipo": create_tipo_equipo_tool,
    "create_tecnico": create_tecnico_tool,
    "create_equipo": create_equipo_tool,
    "create_cotizacion": create_cotizacion_tool,
}

# Define the tool definitions for Gemini
tools_schema = [
    {
        "function_declarations": [
            {
                "name": "create_client",
                "description": "Register a new client in the system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {"type": "string", "description": "First name of the client"},
                        "apellido_paterno": {"type": "string", "description": "Paternal last name"},
                        "apellido_materno": {"type": "string", "description": "Maternal last name"},
                        "telefono": {"type": "string", "description": "Phone number (optional)"},
                    },
                    "required": ["nombre", "apellido_paterno", "apellido_materno"]
                }
            },
            {
                "name": "create_service",
                "description": "Register a new service offered by the company.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {"type": "string", "description": "Name of the service"},
                        "descripcion": {"type": "string", "description": "Short description of what the service entails"},
                        "precio": {"type": "number", "description": "Price of the service"},
                    },
                    "required": ["nombre", "descripcion", "precio"]
                }
            },
            {
                "name": "create_tipo_equipo",
                "description": "Create a category of equipment (e.g. Laptop, Printer).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {"type": "string", "description": "Name of the type"},
                        "descripcion": {"type": "string", "description": "Description"},
                    },
                    "required": ["nombre", "descripcion"]
                }
            },
            {
                "name": "create_tecnico",
                "description": "Register a new technician.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {"type": "string", "description": "First name"},
                        "apellido_paterno": {"type": "string", "description": "Paternal last name"},
                        "apellido_materno": {"type": "string", "description": "Maternal last name"},
                        "telefono": {"type": "string", "description": "Phone number"},
                    },
                    "required": ["nombre", "apellido_paterno", "apellido_materno"]
                }
            },
            {
                "name": "create_equipo",
                "description": "Register a specific device for a client.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "marca": {"type": "string", "description": "Brand of the device (e.g. Dell)"},
                        "modelo": {"type": "string", "description": "Model of the device"},
                        "id_tipo_equipo": {"type": "integer", "description": "ID of the Equipment Type"},
                        "id_dueno": {"type": "integer", "description": "ID of the Client (Owner)"},
                    },
                    "required": ["marca", "modelo", "id_tipo_equipo", "id_dueno"]
                }
            },
            {
                "name": "create_cotizacion",
                "description": "Create a new quote request.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id_cliente": {"type": "integer", "description": "ID of the Client"},
                        "id_equipo": {"type": "integer", "description": "ID of the Equipment"},
                        "descripcion_falla": {"type": "string", "description": "Description of the failure"},
                    },
                    "required": ["id_cliente", "id_equipo", "descripcion_falla"]
                }
            }
        ]
    }
]

# model = genai.GenerativeModel('gemini-2.0-flash', tools=tools_schema)
model = genai.GenerativeModel('gemini-flash-latest', tools=tools_schema)
# model = genai.GenerativeModel('gemini-1.5-flash', tools=tools_schema)

def get_context(db: Session) -> str:
    # Retrieve relevant data for context
    servicios = db.exec(select(Servicio).limit(10)).all()
    equipos = db.exec(select(Equipo).limit(10)).all()
    tipos_equipo = db.exec(select(TipoEquipo).limit(10)).all()
    tecnicos = db.exec(select(Tecnico).limit(10)).all()
    clientes = db.exec(select(Cliente).limit(10)).all()
    
    context_str = "--- DATABASE CONTEXT ---\n"
    
    context_str += "Services (ID | Name | Price):\n"
    for s in servicios:
        context_str += f"- {s.id}: {s.nombre} (${s.precio})\n"
        
    context_str += "\nEquipment Categories (ID | Name):\n"
    for te in tipos_equipo:
        context_str += f"- {te.id}: {te.nombre}\n"
        
    context_str += "\nTechnicians (ID | Name):\n"
    for t in tecnicos:
        context_str += f"- {t.id}: {t.nombre} {t.apellido_paterno}\n"
        
    context_str += "\nClients (ID | Name):\n"
    for c in clientes:
        context_str += f"- {c.id}: {c.nombre} {c.apellido_paterno}\n"
        
    context_str += "--- END CONTEXT ---\n"
        
    return context_str

async def generate_chat_response(query: str, db: Session) -> str:
    context = get_context(db)
    
    chat_session = model.start_chat()
    
    prompt = f"""
    You are an intelligent Agent for a computer service center.
    You have access to tools to Create Clients and Create Services in the database.
    
    CONTEXT from Database:
    {context}
    
    USER QUERY: {query}
    
    INSTRUCTIONS:
    1. If the user asks to create something, extracting the necessary parameters and CALL THE APPROPRIATE TOOL.
    2. If the user simply asks for information, answer based on the Context.
    3. Always answer in Spanish.
    """
    
    try:
        response = await chat_session.send_message_async(prompt)
        
        # Check for function call
        if response.parts and response.parts[0].function_call:
            fc = response.parts[0].function_call
            tool_name = fc.name
            args = fc.args
            
            print(f"Agent is calling tool: {tool_name} with args: {args}")
            
            if tool_name in available_tools:
                # Prepare arguments for the tool function
                tool_func = available_tools[tool_name]
                
                # We need to manually inject 'db' session as it's not generated by LLM
                # Convert args to dict and pass to function
                # Note: 'args' is a ProtoMap, safe to convert to dict
                func_args = {k: v for k, v in args.items()}
                
                # Execute tool
                tool_result = tool_func(db=db, **func_args)
                
                # Send result back to model
                response = await chat_session.send_message_async(
                    content.Content(
                        parts=[content.Part(
                            function_response=content.FunctionResponse(
                                name=tool_name,
                                response={"result": tool_result}
                            )
                        )]
                    )
                )
                
        return response.text

    except Exception as e:
        print(f"Error calling Gemini Agent: {e}")
        return "Lo siento, hubo un error al procesar tu solicitud. Por favor intenta de nuevo más tarde."
