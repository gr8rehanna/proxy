import time
import os
import json
import platform
from starlette.responses import JSONResponse
import logging
from threading import Thread
from fetch import fetch_proxies
from filter import filter_proxies
from check import check_proxies
from contextlib import asynccontextmanager

start_time = time.time()

logging.basicConfig(level=logging.ERROR)

RAW_ALL = os.path.join(os.path.dirname(__file__), 'raw', 'all.json')
PROXY_JSON = os.path.join(os.path.dirname(__file__), 'proxy.json')

def get_status():
    uptime = int(time.time() - start_time)
    cpu_total = psutil.cpu_count(logical=True)
    cpu_used = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    return {
        'status': 'ok',
        'uptime_seconds': uptime,
        'cpu_total': cpu_total,
        'cpu_used_percent': cpu_used,
        'memory_total_mb': int(mem.total / 1024 / 1024),
        'memory_used_mb': int(mem.used / 1024 / 1024),
        'platform': platform.platform(),
        'python_version': platform.python_version()
    }

@app.get('/')
def root():
    return get_status()

@app.get('/api')
def get_api():
    try:
        with open(PROXY_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JSONResponse(data)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

@app.get('/all')
def get_all():
    try:
        with open(RAW_ALL, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JSONResponse(data)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

def update_proxies():
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Update started {now}")
    fetch_proxies()
    filter_proxies()
    check_proxies()

def schedule_updates():
    def cron_loop():
        time.sleep(10)  # Initial delay on app start
        while True:
            update_proxies()
            time.sleep(3600)  # 1 hour
    Thread(target=cron_loop, daemon=True).start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    schedule_updates()
    yield

app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=False, log_level='error')
