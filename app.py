from ObjectDetection.pipeline.training_pipeline import TrainPipeline
from ObjectDetection.utils.main_utils import decodeImage, encodeImageIntoBase64
from ObjectDetection.constants.application import APP_HOST, APP_PORT
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from fastapi.templating import Jinja2Templates


app = FastAPI()

origins = [APP_HOST,
   f"http://{APP_HOST}:{APP_PORT}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

clApp = ClientApp()

# Define the schema for incoming JSON requests
class ImageRequest(BaseModel):
    image: str


@app.get("/train")
async def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()

    return "Training Successfully Completed"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predictRoute(request: Request):
    try:
        body = await request.json()
        image = body["image"]
        decodeImage(image, clApp.filename)

        os.system("cd yolov5 && python3 detect.py --weights best.pt --imgsz 640 --conf 0.4 --source ../data/inputImage.jpg")

        opencodebase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputImage.jpg").decode('utf-8')
        result = {"image": opencodebase64}

        os.system("rm -rf yolov5/runs")

    except ValueError as val:
        return JSONResponse(content={"error": "Value not found inside json data"}, status_code=400)
    except KeyError:
        return JSONResponse(content={"error": "Incorrect key passed"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

    return JSONResponse(content=result)


@app.get("/live")
async def predictLive():
    try:
        os.system("cd yolov5 && python3 detect.py --weights yolov5s.pt --imgsz 640 --conf 0.4 --source 0")
        os.system("rm -rf yolov5/runs")

        return 'camera is live'
    
    except ValueError as val:
        print(val)
        return JSONResponse("value not found inside json data")
    
if __name__ == "__main__":
    clApp = ClientApp()
    import uvicorn
    uvicorn.run(app, host= APP_HOST, port = APP_PORT)