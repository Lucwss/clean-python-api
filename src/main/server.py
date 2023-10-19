import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        'config.app:app',
        host='0.0.0.0',
        port=8002,
        reload=True,
        access_log=True
    )