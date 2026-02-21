import threading
import camera
#import track
#import hexapod

def START():
    try:
        print("\n adresse => 192.168.1.29:7123/index.html")
        with camera.SignalingHTTPServer(('', 7123), camera.StreamingHandler) as httpd:
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            #hexapod.Start()

    finally:
        camera.picam2.stop_recording()
        httpd.shutdown()

if __name__ == "__main__":
    START()


"""
address = ('', 7123)
server = StreamingServer(address, StreamingHandler)
server.serve_forever() #bloque les autres threads
"""