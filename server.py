from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ایمپورت کردن مغز پروژه (فرض می‌کنیم توابع هوش مصنوعی در brain.py هستند)
# از brain import generate_response (یا هر تابعی که برای پردازش متن داری)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    
    # 🧠 اینجا پیام کاربر به «مغز» پایتون فرستاده می‌شود:
    # bot_response = generate_response(user_message)
    
    # فعلاً به عنوان تستِ اتصال واقعی به مغز:
    bot_response = f"مغز پروژه پیام شما را دریافت کرد و پردازش نمود: {user_message}"
    
    return {"response": bot_response}

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)