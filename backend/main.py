from fastapi import FastAPI

app = FastAPI(
    title="VaultIQ API",
    description="AI-Powered Smart Bookmark Manager",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project": "VaultIQ",
        "message": "Welcome to VaultIQ",
        "status": "Backend Running Successfully"
    }