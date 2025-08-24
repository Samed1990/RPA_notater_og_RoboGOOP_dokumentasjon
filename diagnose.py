from flask import Flask, request
import socket
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    # Log the request details
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    print(f"[{datetime.now()}] Root accessed by {client_ip} - {user_agent}")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Flask IS Working!</title></head>
    <body>
        <h1 style='color: green;'>✅ Flask is running correctly!</h1>
        <p>Request received at: {datetime.now()}</p>
        <p>Your IP: {client_ip}</p>
        <p>If you see this, Flask is working but OneDrive is intercepting the root path.</p>
        <hr>
        <p>Test these URLs:</p>
        <ul>
            <li><a href='/test'>/test</a> - Should work</li>
            <li><a href='/debug'>/debug</a> - Should work</li>
            <li><a href='http://localhost:5000/'>http://localhost:5000/</a> - Might work</li>
        </ul>
    </body>
    </html>
    """

@app.route("/test")
def test():
    return "🟢 TEST PAGE - Flask is working!"

@app.route("/debug")
def debug():
    return f"""
    Debug info:
    - Time: {datetime.now()}
    - Client IP: {request.remote_addr}
    - User Agent: {request.headers.get('User-Agent')}
    - Flask is running!
    """

@app.route("/check-ports")
def check_ports():
    # Test if ports are available
    ports = [5000, 5001, 5050, 8080, 3000]
    results = []
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        status = "🟢 Available" if result != 0 else "🔴 In use"
        results.append(f"Port {port}: {status}")
    
    return "<br>".join(results)

if __name__ == "__main__":
    print("=" * 60)
    print("FLASK DIAGNOSTIC TOOL")
    print("=" * 60)
    print("Starting server on port 5000...")
    print("If you see a blank page at http://127.0.0.1:5000/")
    print("but other paths work, it's OneDrive interception!")
    print("=" * 60)
    
    app.run(debug=True, port=5000, use_reloader=False)