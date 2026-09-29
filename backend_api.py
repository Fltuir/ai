import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
)

from agent import FlowchAgent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from memory import MemoryManager
from pydantic import BaseModel

app = FastAPI(title="Flowch AI Agent API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = FlowchAgent()


class ChatRequest(BaseModel):
  message: str  # از این به بعد فقط پیام جدید کاربر را می‌گیریم و تاریخچه از فایل خوانده می‌شود!


@app.get("/")
def home():
  return {"status": "Flowch FastAPI Backend is running smoothly 🚀"}


@app.get("/api/history")
def get_history():
  """بارگذاری تاریخچه اولیه برای نمایش در فرانت‌اند"""
  history = MemoryManager.load_memory()
  if not history:
    history = [{
        "role": "assistant",
        "content": (
            "سلام آتاباک! حافظه فلوچ روی سیستم فعال شد. هرچی بگی رو سیستم"
            " ذخیره میکنم!"
        ),
    }]
  return {"history": history}


@app.post("/api/chat")
def chat_with_agent(request: ChatRequest):
  try:
    # ۱. خواندن حافظه قبلی از فایل
    history = MemoryManager.load_memory()

    # ۲. افزودن پیام جدید کاربر به تاریخچه
    history.append({"role": "user", "content": request.message})

    # ۳. اجرای ایجنت با کل تاریخچه
    response_text = agent.run(history)

    # ۴. افزودن پاسخ ایجنت به تاریخچه
    history.append({"role": "assistant", "content": response_text})

    # ۵. ذخیره نهایی در فایل مموری محلی
    MemoryManager.save_memory(history)

    return {"response": response_text}
  except Exception as e:
    return {"response": f"خطا در پردازش سرور: {str(e)}"}


@app.post("/api/clear")
def clear_chat():
  MemoryManager.clear_memory()
  return {"status": "Memory cleared"}


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("backend_api:app", host="127.0.0.1", port=8000, reload=True)