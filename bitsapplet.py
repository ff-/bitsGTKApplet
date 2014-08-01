#!/usr/bin/env python

import websocket
import json
import time
import thread
import gtk
import appindicator
import sys
import subprocess
import time
import gobject
gobject.threads_init()

##### Websocket things

def ws_on_message(ws, message):
    global prev_status
    try:
        cur_status = json.loads(message)["status"]["value"]
        if cur_status != prev_status:
            prev_status = cur_status
            if cur_status == "open":
                opened_callback()
            elif cur_status == "closed":
                closed_callback()
            else:
                print "WTF?" # Se entra qui, non va bene
    except:
        pass

def ws_on_error(ws, error):
    print "Error: " + error.message
    print "Reconnecting..."    
    start_websocket()

def ws_on_close(ws):
    print "Connection closed"

def ws_on_open(ws):
    def ping(*args):
        while 1:
            #print "Keep-alive"
            ws.send("Hi")
            time.sleep(15)
    thread.start_new_thread(ping, ())    

def start_websocket():
    ws = websocket.WebSocketApp("wss://bits.poul.org/ws",
                                on_message = ws_on_message,
                                on_error = ws_on_error,
                                on_close = ws_on_close,
                                on_open = ws_on_open)
    ws.run_forever()

##### GTK things

def applet_status(w, buf):
    subprocess.call(["xdg-open", "https://bits.poul.org"])

def applet_exit(w):
    sys.exit(0)

def item_print_status(status):
    return "Bits Status: %s" % status

##### Callbacks

def opened_callback():
    global ind
    ind.set_icon("object-select-symbolic")
    menuitem_status.set_label(item_print_status("Open"))

def closed_callback():
    global ind
    ind.set_icon("window-close-symbolic")
    menuitem_status.set_label(item_print_status("Closed"))

##### Main here

prev_status = ""
status_string = "Closed"
menuitem_status = gtk.MenuItem(item_print_status(status_string))
ind = appindicator.Indicator ("example-simple-client",
                                "window-close-symbolic", #was indicator-messages
                                #object-select-symbolic
                                appindicator.CATEGORY_APPLICATION_STATUS)

if __name__== "__main__":
    thread.start_new_thread(start_websocket, ())
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_attention_icon ("indicator-messages-new")

    #create all the items
    #menuitem_status is global
    menuitem_status.connect("activate", applet_status, "lol")
    menuitem_status.show()

    separator = gtk.SeparatorMenuItem()
    separator.show()

    menuitem_exit = gtk.MenuItem("Exit")
    menuitem_exit.connect("activate", applet_exit)
    menuitem_exit.show()

    #pay attention to the appending order
    menu = gtk.Menu()
    menu.append(menuitem_status)
    menu.append(separator)
    menu.append(menuitem_exit)

    ind.set_menu(menu)

    gtk.main()
