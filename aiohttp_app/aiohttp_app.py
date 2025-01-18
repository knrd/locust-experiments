from aiohttp import web
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_request(request):
    if "ctest" in request.cookies:
        try:
            json_data = await request.json()
            logger.info(f"Received JSON (aiohttp): {json_data}")
        except Exception as e:
            logger.error(f"Error processing JSON: {e}")
    
    return web.Response(text="OK", status=200)

app = web.Application()
app.router.add_post('/', handle_request)

if __name__ == '__main__':
    web.run_app(app, port=8080)
