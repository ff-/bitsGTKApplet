import websocket
import thread
import json
import time

class BitsWS(object):
    """Interacting with BITS through websockets"""
    def __init__(self, opened_callback, closed_callback):
        super(BitsWS, self).__init__()
        self.opened_callback = opened_callback
        self.closed_callback = closed_callback
        self.prev_status = ""
        self.ws = websocket.WebSocketApp("wss://bits.poul.org/ws",
                                    on_message = self.ws_on_message,
                                    on_error = self.ws_on_error,
                                    on_close = self.ws_on_close,
                                    on_open = self.ws_on_open)

    def ws_on_message(self, ws, message):
        prev_status = self.prev_status
        try:
            cur_status = json.loads(message)["status"]["value"]
            if cur_status != prev_status:
                prev_status = cur_status
                if cur_status == "open":
                    self.opened_callback()
                elif cur_status == "closed":
                    self.closed_callback()
                else:
                    print "WTF?" # Se entra qui, non va bene
        except:
            pass

    def ws_on_error(self, ws, error):
        print "Error: " + error.message
        print "Reconnecting..."    
        self.start_websocket()

    def ws_on_close(self, ws):
        print "Connection closed"

    def ws_on_open(self, ws):
        def ping(*args):
            while 1:
                #print "Keep-alive"
                self.ws.send("Hi")
                time.sleep(15)
        thread.start_new_thread(ping, ())    

    def start_websocket(self):
        #websocket.enableTrace(True)
        self.ws.run_forever()