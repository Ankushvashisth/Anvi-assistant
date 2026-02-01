import sys
print("Start Debug")
try:
    import flask
    print(f"Flask imported: {flask.__version__}")
except ImportError as e:
    print(f"Flask Error: {e}")

try:
    import flask_socketio
    print(f"SocketIO imported: {flask_socketio.__version__}")
except ImportError as e:
    print(f"SocketIO Error: {e}")

try:
    import eventlet
    print(f"Eventlet imported: {eventlet.__version__}")
except ImportError as e:
    print(f"Eventlet Error: {e}")

try:
    from engineio.async_drivers import threading
    print("Threading async mode available")
except Exception as e:
    print(f"Async Driver Error: {e}")

print("End Debug")
