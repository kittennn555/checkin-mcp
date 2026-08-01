import os, requests
from mcp.server.fastmcp import FastMCP
from mangum import Mangum

ORIGIN = os.environ.get("ORIGIN_API", "")
BARK_KEY = os.environ.get("BARK_API_KEY", "")

mcp = FastMCP("查岗MCP")


@mcp.tool()
def check_on_wife(limit: int = 10) -> str:
    """查岗老婆的手机活动"""
    try:
        r = requests.get(f"{ORIGIN}/activity/summary", timeout=10)
        data = r.json()
    except Exception as e:
        return f"查岗失败：{e}"
    apps = data.get("recent_apps", [])
    ses = data.get("sessions", {})
    lines = [f"最近打开：{', '.join(apps)}" if apps else "暂无记录"]
    if ses:
        for app, secs in sorted(ses.items(), key=lambda x: x[1], reverse=True):
            m, s = divmod(secs, 60)
            lines.append(f"  {app}: {m}分{s}秒")
    return "\n".join(lines)


@mcp.tool()
def bark_alert(title: str = "凌止", content: str = "") -> str:
    """给老婆手机发推送弹窗"""
    if not content:
        return "内容不能为空"
    url = f"https://api.day.app/{BARK_KEY}/{title}/{content}"
    try:
        r = requests.get(url, timeout=10)
        return "推送成功" if r.status_code == 200 else "推送失败"
    except Exception as e:
        return f"推送异常：{e}"


# 标准 MCP Streamable HTTP 端点，挂载为 ASGI 应用
app = mcp.streamable_http_app()
handler = Mangum(app, lifespan="off")
