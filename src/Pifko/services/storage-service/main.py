from fastapi import FastAPI
import os
import uvicorn

app = FastAPI(title="Storage Service", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Hello from  Storage Service"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "storage-service"}


@app.get("/inventory")
async def get_inventory():
    return {"message": "Inventory endpoint - coming soon"}


@app.get("/allocation")
async def get_allocation():
    return {"message": "Allocation endpoint - coming soon"}


if __name__ == "__main__":

    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
