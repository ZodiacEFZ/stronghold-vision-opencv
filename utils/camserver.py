import cv2
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					__img = self.capture_func()
					if not __img is None:
						success, __encoded = cv2.imencode(".jpg", __img)
						if success:
							self.wfile.write(b"--jpgboundary")
							self.send_header('Content-type', b'image/jpeg')
							self.send_header('Content-length', len(__encoded))
							self.end_headers()
							self.wfile.write(__encoded.tobytes())
						else:
							break
					else:
						break
				except KeyboardInterrupt:
					break

class CamServer(HTTPServer):
	def serve_forever(self, capture_func):
		self.RequestHandlerClass.capture_func = capture_func
		HTTPServer.serve_forever(self)

def serve(config, capture_func, server_class=CamServer, handler_class=CamHandler):
	server = server_class((config["host"], config["port"]), handler_class)
	server.serve_forever(capture_func)
