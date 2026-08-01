import os
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from mcp.fastapi import mcp_api_router
from tools.check_on_wife import check_on_wife
from tools.bark_alert import bark_alert

# 创建 FastAPI 应用
app = FastAPI()

# 添加一个全局异常处理器，这样任何错误都会被我们捕获并显示出来
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_details = traceback.format_exc()
    # 在 Vercel 日志中打印，方便我们自己看
    print(f"Caught an exception: {error_details}")
    # 将完整的错误信息作为纯文本返回给浏览器
    return PlainTextResponse(f"Server Error:\n{error_details}", status_code=500)

# 注册 MCP 路由
app.include_router(mcp_api_router, prefix="")

# 注册工具
mcp_api_router.tools = {
    "check_on_wife": check_on_wife,
    "bark_alert": bark_alert,
}

# Vercel 会自动处理这个 app
