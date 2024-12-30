# DocQuery AI

**DocQuery AI** is an AI-powered document querying tool that allows users to interact with PDF documents by asking natural language queries. Using Groq's language model API, this system enables intelligent document analysis, providing accurate responses to users' queries about the document content. The project also includes features for scheduling appointments, validating phone numbers and emails, and parsing dates for appointment scheduling.

## Features

- **PDF Querying**: This feature allows users to upload PDF documents and ask questions about the content of those documents. The system processes the PDF, extracts text, and uses a language model to answer queries based on the document's content. This is particularly useful for extracting key information from large documents such as reports, manuals, and academic papers

- **Appointment Scheduling**: DocQuery AI can process natural language date queries to help users schedule appointments. For example, if a user asks, "What about next Friday?" the system parses the query, understands the date, and helps schedule an appointment accordingly. It supports a wide range of date expressions like "tomorrow", "next Monday", or "in two days".

- **Phone Number & Email Validation**: The system validates whether the provided phone number and email address are in the correct format. It checks whether the phone number follows international standards (e.g., +1 for US, +44 for the UK) and whether the email follows the general email format (e.g., user@example.com). This ensures that users' contact information is correct and ready for use in the system.

- **Date Parsing**: The ability to interpret natural language date expressions is critical for the appointment scheduling feature. Using date parsing libraries, the system can understand various date formats like "the 5th of December", "in 3 days", or "on Monday next week". This allows users to interact with the system in a more intuitive, conversational way.

- **Retry Mechanism**:To improve reliability, the system includes a retry mechanism that automatically attempts to reprocess requests in case of service disruptions or server errors (like a 503 error). This ensures that the user experience remains smooth and minimizes downtime due to temporary issues.

## Tech Stack

- **Python 3.x**: Primary programming language used.
- **FastAPI**: A modern web framework for building APIs.
- **LangChain with Groq API**: Utilized to query and interact with the language model.
- **PyMuPDF**: A library for extracting text content from PDF files.
- **Pydantic**: Used for data validation and management.
- **DateParser**: Parses date strings into actual dates.
- **Uvicorn**: ASGI server for running FastAPI applications.

