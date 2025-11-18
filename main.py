"""
Main Application Entry Point
FastAPI server for YouTube Auto Generator
"""
import uvicorn
from config import config

def main():
    """Start the FastAPI server"""
    # Validate configuration
    try:
        config.validate()
        print("✅ Configuration validated")
    except ValueError as e:
        print(f"⚠️  Configuration warning: {e}")
        print("Some features may not work without proper API keys")

    print(f"🚀 Starting server on {config.HOST}:{config.PORT}")

    # Import app after config validation
    from app.web.line_webhook import app

    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level="info"
    )


if __name__ == "__main__":
    main()
