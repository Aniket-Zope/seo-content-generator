import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting API server...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", "api.main:app",
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])

def start_streamlit_app():
    """Start the Streamlit frontend"""
    print("🌐 Starting Streamlit frontend...")
    time.sleep(3)  # Wait for API to start
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "frontend/streamlit_app.py",
        "--server.port", "8501"
    ])

def main():
    print("🎯 SEO Content Generator - Starting Application")
    print("=" * 50)

    # ✅ Add this line to fix ModuleNotFoundError
    sys.path.append(str(Path(__file__).resolve().parent))

    # Check if .env file exists
    if not Path(".env").exists():
        print("⚠️  .env file not found!")
        print("Please create a .env file with your API keys:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("SERP_API_KEY=your_serp_api_key_here")
        return
    
    try:
        install_requirements()

        print("\n🎯 Choose how to run the application:")
        print("1. Full application (API + Frontend)")
        print("2. API only")
        print("3. Frontend only")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            api_thread = threading.Thread(target=start_api_server, daemon=True)
            api_thread.start()

            time.sleep(5)
            start_streamlit_app()

        elif choice == "2":
            start_api_server()

        elif choice == "3":
            start_streamlit_app()

        else:
            print("❌ Invalid choice!")

    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
