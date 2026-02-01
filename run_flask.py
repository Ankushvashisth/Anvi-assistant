import sys
import traceback

print("WRAPPER: Starting...")
try:
    print("WRAPPER: Importing app module...")
    import app
    print("WRAPPER: Import successful.")
except Exception:
    print("WRAPPER: Crashed during import!")
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    print("WRAPPER: Running SocketIO...")
    try:
        app.socketio.run(app.app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except Exception:
        traceback.print_exc()
