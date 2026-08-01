import os
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from mcp.fastapi import mcp_api_router
from tools.check_on_wife import check_on_wife
from tools.bark_alert import bark_alert

# 创建一个应用实例
app = Starlette()

# 包装原始的 mcp_api_router 以捕获异常
@app.route("/mcp", methods=["GET", "POST"])
async def mcp_with_error_handling(request):
    try:
        # 正常调用原始的 MCP 路由器
        return await mcp_api_router(request)
    except Exception as e:
        # 如果发生任何错误，则返回错误的详细信息
        import traceback
        error_details = traceback.format_exc()
        # 在 Vercel 日志中打印错误，方便调试
        print(f"MCP aPI Error: {error_details}")
        # 将详细错误作为纯文本返回给客户端
        return StreamingResponse(iter([f"Server Error:\n{error_details}"]), media_type="text/plain")

# 注册工具
mcp_api_router.tools = {
    "check_on_wife": check_on_wife,
    "bark_alert": bark_alert,
}

# Vercel 会自动处理这个 app
# 如果本地运行，可以取消下面的注释
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

