from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import base64
import os

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    streaming=True,
)

search_tool = TavilySearch(
    max_results=5,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

agent = create_react_agent(
    model=llm,
    tools=[search_tool],
    prompt="""You are an advanced AI research assistant with vision and web search capabilities.

CRITICAL LANGUAGE RULE — This is your most important instruction:
- Detect the language/style of the user's message
- If they write in pure Bengali → respond in pure Bengali
- If they write in pure English → respond in pure English  
- If they write in Banglish (mixed Bengali + English) → respond in Banglish exactly like them
- Mirror their exact tone: casual hলে casual, formal হলে formal
- NEVER switch language on your own

CAPABILITIES:
1. Answer questions from your knowledge
2. Search web for current/realtime information
3. Analyze images and search web based on what you see
4. Remember conversation context

BEHAVIOR:
- For realtime info (news, prices, weather, recent events) → always use web search
- For image analysis → describe first, then search web for related info
- Be conversational, not robotic
- Keep responses concise unless asked for detail"""
)

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_mime_type(image_path: str) -> str:
    ext = image_path.lower().split(".")[-1]
    return {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "gif": "image/gif",
            "webp": "image/webp"}.get(ext, "image/jpeg")

def print_banner():
    print("=" * 50)
    print("🤖 Advanced AI Research Agent")
    print("=" * 50)
    print("✅ Web search  ✅ Image analysis  ✅ Memory")
    print("📌 'image: /path/to/file' to analyze image")
    print("📌 'clear' to reset conversation")
    print("📌 'exit' to quit")
    print("=" * 50 + "\n")

chat_history = []

print_banner()

while True:
    try:
        user_input = input("You: ").strip()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if user_input.lower() == "clear":
        chat_history = []
        print("✅ Conversation cleared!\n")
        continue

    print("\nAI: ", end="", flush=True)

    try:
        if user_input.lower().startswith("image:"):
            image_path = user_input[6:].strip()

            if not os.path.exists(image_path):
                print(f"❌ File not found: '{image_path}'\n")
                continue

            file_size = os.path.getsize(image_path) / (1024 * 1024)
            if file_size > 10:
                print(f"❌ File too large ({file_size:.1f}MB). Max 10MB.\n")
                continue

            print(f"📸 Analyzing image: {os.path.basename(image_path)}...")

            image_data = encode_image(image_path)
            mime_type = get_mime_type(image_path)

            message = {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_data}"}
                    },
                    {
                        "type": "text",
                        "text": "Analyze this image. Identify what you see, then search the web for current relevant information about it."
                    }
                ]
            }

            response = agent.invoke({
                "messages": chat_history + [message]
            })

            final_answer = response["messages"][-1].content
            print(final_answer + "\n")

            chat_history.append({
                "role": "user",
                "content": f"[Image: {os.path.basename(image_path)}]"
            })
            chat_history.append({"role": "assistant", "content": final_answer})

        else:
            response = agent.invoke({
                "messages": chat_history + [{"role": "user", "content": user_input}]
            })

            final_answer = response["messages"][-1].content
            print(final_answer + "\n")

            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": final_answer})

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        