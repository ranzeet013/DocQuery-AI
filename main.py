import re
import time
import fitz 
from langchain_groq import ChatGroq
import dateparser  
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from io import BytesIO

llm = ChatGroq(
    temperature=0,
    groq_api_key="enter your key",
    model_name="llama-3.1-70b-versatile"
)

app = FastAPI()

class AppointmentRequest(BaseModel):
    user_name: str
    phone_number: str
    email: str
    appointment_date_query: str

class PDFQueryRequest(BaseModel):
    query: str

def extract_text_from_pdf(pdf_file: BytesIO):
    """Extract text from an uploaded PDF file."""
    doc = fitz.open(stream=pdf_file, filetype="pdf") 
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text() 
    return text

def chunk_text(text: str, max_chunk_size: int = 2000):
    """Split text into smaller chunks of specified size."""
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    return chunks

def retry_request(request_func, retries=3, delay=5):
    """Retry the request in case of service unavailability (503)."""
    for attempt in range(retries):
        try:
            return request_func() 
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise Exception("Max retries reached. Unable to complete request.")

def answer_query_from_pdf(query: str, pdf_file: BytesIO):
    """Answer a user's query by processing text from a PDF."""
    # extract text from the PDF document
    document_content = extract_text_from_pdf(pdf_file)
    document_chunks = chunk_text(document_content)
    response = ""
    for chunk in document_chunks:
        response_chunk = retry_request(lambda: llm.invoke(f"{chunk} {query}"))
        response += response_chunk.content
    
    return response

def validate_phone_number(phone_number: str):
    return bool(re.match(r"^\+?[1-9]\d{1,14}$", phone_number)) 

def validate_email(email: str):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))  

def extract_date(date_query: str):
    parsed_date = dateparser.parse(date_query)
    if parsed_date:
        return parsed_date.strftime('%Y-%m-%d')  
    else:
        return None

@app.post("/schedule_appointment/")
async def schedule_appointment(request: AppointmentRequest):
    user_name = request.user_name
    phone_number = request.phone_number
    email = request.email
    appointment_date_query = request.appointment_date_query
    
    # validate phone number
    if not validate_phone_number(phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format.")
    
    # validate email
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email address format.")
    
    # extract appointment date
    appointment_date = extract_date(appointment_date_query)
    if not appointment_date:
        raise HTTPException(status_code=400, detail="Could not understand the appointment date.")
    
    # return the appointment confirmation
    return {
        "message": "Appointment scheduled successfully",
        "details": {
            "user_name": user_name,
            "phone_number": phone_number,
            "email": email,
            "appointment_date": appointment_date
        }
    }

@app.post("/query_pdf/")
async def query_pdf(query: str, pdf_file: UploadFile = File(...)):
    """Handle the PDF query with file upload and query input."""
    pdf_bytes = await pdf_file.read()
    pdf_file_io = BytesIO(pdf_bytes)
    
    try:
        response = answer_query_from_pdf(query, pdf_file_io)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the PDF: {str(e)}")
    
    return {"response": response}
