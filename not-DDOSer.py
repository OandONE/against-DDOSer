from bottle import request, abort, run, route, hook
import time

rate_limits = {}
BLOCK_TIME = 60  
MAX_REQUESTS = 7  
TIME_FRAME = 30  

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
        abort(403, "شما به مدت 60 ثانیه مسدود شده‌اید.")
        
    if current_time - user_info['first_request_time'] < TIME_FRAME:
        user_info['count'] += 1
    else:
        user_info['count'] = 1
        user_info['first_request_time'] = current_time
        
    if user_info['count'] > MAX_REQUESTS:
        user_info['blocked_until'] = current_time + BLOCK_TIME
        abort(403, "شما به مدت 60 ثانیه مسدود شده‌اید.")

@route('/')
def my_route():
    return "<h1>TEST</h1>"

run(host='localhost', port=8080)
