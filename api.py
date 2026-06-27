from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

from video_analyser import VideoAnalyzer

app = FastAPI()

# ---------------- CORS FIX ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows your frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {"status": "AI Football Coach API running"}

# ---------------- MAIN ANALYSIS ENDPOINT ----------------
@app.post("/analyse")
async def analyse_video(file: UploadFile = File(...)):

    temp_path = "temp.mp4"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analyzer = VideoAnalyzer(temp_path)
    result = analyzer.analyse()

    return result