import uvicorn

if __name__ == "__main__":
    # "main:app"-ի փոխարեն գրիր "app.main:app"
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)