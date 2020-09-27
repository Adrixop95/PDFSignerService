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
            teststr = str(pdf_tmp_path)
    finally:
        filepdf.file.close()

    mylist = []
    for x in os.listdir("./cert_pems"):
        mylist.append(open("./cert_pems/"+x).read())
    mytuple = tuple(mylist)

    print(type(teststr))
    print(teststr)

    data = open(teststr, 'rb').read()
    #print(data)

    (hashok, signatureok, certok) = pdf.verify(data, mytuple)
    print('signature ok?', signatureok)
    print('hash ok?', hashok)
    print('cert ok?', certok)
