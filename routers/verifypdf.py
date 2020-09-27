from fastapi import APIRouter, UploadFile, File
from endesive import pdf
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil
import os

router = APIRouter()


@router.post("/upload_cert_pems")
async def upload_cert_pems():
    pass


@router.post("/verify")
async def verify_pdf(filepdf: UploadFile = File(...)):
    try:
        suffix = Path(filepdf.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(filepdf.file, tmp)
            pdf_tmp_path = Path(tmp.name)
    finally:
        filepdf.file.close()

    files_path = os.listdir("./cert_pems/")

    print(files_path)

    for i in files_path:
        print(i)
        trusted = open("./cert_pems/"+i, 'rt').read()

    data = open(pdf_tmp_path, 'rb').read()

    #print(pdf.verify(data, trusted))
    print(pdf.verify(pdf_tmp_path, "./cert_pems/ca-actalis.pem"))
