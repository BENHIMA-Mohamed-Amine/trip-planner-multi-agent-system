from src.core.config import GROQ_API_KEY
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:openai/gpt-oss-120b", api_key=GROQ_API_KEY)
