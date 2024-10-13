import requests
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Any

class PDFReaderArgs(BaseModel):
    pdf_url: str = Field(..., description="URL of the PDF to read")

class PDFReader(BaseTool):
    """Tool that reads a PDF from a URL and returns its content as text."""

    name = "pdf_reader"
    description = "Reads a PDF from a given URL and returns the extracted text."

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, pdf_url: str) -> str:
        response = requests.get(pdf_url)
        response.raise_for_status()


        with open("/tmp/temp.pdf", "wb") as f:
            f.write(response.content)


        reader = PdfReader("/tmp/temp.pdf")
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    async def _arun(self, *args: Any, **kwargs: Any):
        raise NotImplementedError

if __name__ == "__main__":
    pdf_reader = PDFReader()
    result = pdf_reader._run("https://arxiv.org/pdf/2407.02067")
    print(result)
