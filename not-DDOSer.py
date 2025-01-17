from bottle import request, response, run, route, hook
import time

rate_limits = {}
BLOCK_TIME = 60  # زمان بلاک در ثانیه
MAX_REQUESTS = 7  # حداکثر درخواست‌ها در 30 ثانیه
TIME_FRAME = 30  # بازه زمانی در ثانیه

#for ever request
@hook('before_request')
def check_rate_limit():
    client_ip = request.remote_addr
    current_time = time.time()
    if client_ip not in rate_limits:
        rate_limits[client_ip] = {
            'count': 0,
            'first_request_time': current_time,
            'blocked_until': 0
        }
    user_info = rate_limits[client_ip]
    if user_info['blocked_until'] > current_time:
        response.status = 403
        response.body = "شما به مدت 60 ثانیه مسدود شده‌اید."
        return
    if current_time - user_info['first_request_time'] < TIME_FRAME:
        user_info['count'] += 1
    else:
        user_info['count'] = 1
        user_info['first_request_time'] = current_time
    if user_info['count'] > MAX_REQUESTS:
        user_info['blocked_until'] = current_time + BLOCK_TIME
        response.status = 403
        response.body = "شما به مدت 60 ثانیه مسدود شده‌اید."
        return
@route('/')
def my_route():
    return "<h1>TEST</h1>"

run(host='localhost', port=8080)