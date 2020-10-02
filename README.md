# PDFSignerService
This microservice is designed to sign and verify PDF files.

The application mainly uses the [endesive](https://pypi.org/project/endesive/) library.
## DEMO
> https://pdfsignerservice.adrox.xyz/api/v1/  
> https://pdfsignerservice.adrox.xyz/api/v1/docs

## Installation
By default, the application is served on port 8000.

### Local
To run the application locally, install the dependencies from the `requirements.txt` 

```
pip install -r requirements.txt
```

file and then execute the command 

```
uvicorn main:app --reload
```

in the application's root directory.

### Docker
Run the container from the available registry.

```
docker run -p 8000:8000 adrixop95/pdfsignerservice:latest
```

The service does not have any environment variables.

### docker-compose example
To run the application on localhost from docker-compose, go to the `deployment/docker-compose` folder and execute the command:

Windows:
```
$env:URL="localhost"; docker-compose -f docker-compose.yml up
```

Linux, macOS:
```
URL="localhost" docker-compose -f .\docker-compose.yml up
```

Traefik automatically manages the SSL certificate generating the let's encrypt certificate. The certificate is generated for `example@example.com`, please change if necessary.  

After launch, it will be available at https://localhost/api/v1/

## Known issues
I noticed that sometimes there is a problem with verifying the signed document, I haven't been able to diagnose it yet.  
The files signed by this microservice have been verified correctly so I think it is a file/library (?) problem.