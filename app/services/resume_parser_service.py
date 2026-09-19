from pathlib import Path

from fastapi import status, HTTPException
from pypdf import PdfReader
from docx import Document


def extract_pdf_text(
        file_path : str
):
    try :
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text :
                pages.append(text)

        return "\n".join(pages).strip()


    except Exception as exc: 
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unable to extract PDF text: {str(exc)}", )




def extract_docx_text( file_path: str, ) -> str: 
    try: 
        document = Document(file_path) 
        paragraphs = [ paragraph.text for paragraph in document.paragraphs if paragraph.text.strip() ] 
        return "\n".join(paragraphs).strip() 
    except Exception as exc: 
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unable to extract DOCX text: {str(exc)}", )



def extract_doc_text( file_path: str, ) -> str: 
    """ Basic .doc support is intentionally not implemented. Old .doc files require a separate conversion strategy. """ 
    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=( "Legacy .doc files are not supported yet. " "Please upload PDF or DOCX." ), )



def extract_resume_text( file_path: str, ) -> str: 
    extension = ( Path(file_path) .suffix .lower() ) 
    if extension == ".pdf": 
        text = extract_pdf_text(file_path) 
    elif extension == ".docx": 
        text = extract_docx_text(file_path) 
    elif extension == ".doc": 
        text = extract_doc_text(file_path) 
    else: 
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported resume format", ) 
    if not text.strip(): 
        raise HTTPException( status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=( "Could not extract readable text from the resume." ), ) 
    return text