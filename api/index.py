from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/mcp")
async def handle_mcp_test():
    return PlainTextResponse("成功了！/mcp 地址通了！现在可以进行下一步了！")

@app.get("/")
async def handle_root_test():
    return PlainTextResponse("服务器在运行，但请访问 /mcp 地址。")

