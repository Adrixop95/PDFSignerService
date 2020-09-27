import datetime
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from starlette.responses import FileResponse

from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms

from fastapi import APIRouter, File, UploadFile, Form

router = APIRouter()


@router.post("/sign")
async def sign_pdf(filecert: UploadFile = File(...),
                   filepdf: UploadFile = File(...),
                   sigflags: str = Form(...),
                   contact: str = Form(...),
                   location: str = Form(...),
                   reason: str = Form(...)):

    try:
        suffix = Path(filecert.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(filecert.file, tmp)
            cert_tmp_path = Path(tmp.name)
    finally:
        filecert.file.close()

    try:
        suffix = Path(filepdf.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(filepdf.file, tmp)
            pdf_tmp_path = Path(tmp.name)
    finally:
        filepdf.file.close()

    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime('%Y%m%d%H%M%S+00\'00\'')

    dct = {
        'sigflags': sigflags,
        'contact': contact,
        'location': location,
        'signingdate': date,
        'reason': reason,
    }

    with open(cert_tmp_path, 'rb') as fp:
        p12 = pkcs12.load_key_and_certificates(fp.read(), b'1234', backends.default_backend())

    datau = open(pdf_tmp_path, 'rb').read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")

    with open(pdf_tmp_path, 'wb') as fp:
        fp.write(datau)
        fp.write(datas)

    return FileResponse(path=pdf_tmp_path, filename=pdf_tmp_path.name)
