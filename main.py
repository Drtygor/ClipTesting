from fastapi import FastAPI

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)