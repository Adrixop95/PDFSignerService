from fastapi import APIRouter, UploadFile, File
from endesive import pdf
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil
import os

router = APIRouter()


@router.post("/upload_cert_pems")
async def upload_cert_pems(filecert: UploadFile = File(...)):
    pass


@router.post("/verify")
async def verify_pdf(filepdf: UploadFile = File(...)):
    try:
        suffix = Path(filepdf.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(filepdf.file, tmp)
            pdf_tmp_path = Path(tmp.name)
            teststr = str(pdf_tmp_path)
    finally:
        filepdf.file.close()

    temp_list = []
    for x in os.listdir("./cert_pems"):
        temp_list.append(open("./cert_pems/"+x).read())
    certs_tuple = tuple(temp_list)

    data = open(teststr, 'rb').read()

    (hashok, signatureok, certok) = pdf.verify(data, certs_tuple)

    return {"Is signature valid": signatureok,
            "Is hash valid": hashok,
            "Is cert valid": certok,
            }
