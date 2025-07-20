# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

## Run Locally

### Frontend

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

### Backend

**Prerequisites:** Python 3


1. Install dependencies:
   `pip install numpy`
2. Run the app:
   `python backend/run_studio.py`
