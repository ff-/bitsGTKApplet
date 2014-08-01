#!/usr/bin/env python

from bitsws import BitsWS
import thread
import gtk
import appindicator
import sys
import subprocess
import gobject
gobject.threads_init()

##### Callbacks

def opened_callback():
    ind.set_icon("object-select-symbolic")
    menuitem_status.set_label(item_print_status("Open"))

def closed_callback():
    ind.set_icon("window-close-symbolic")
    menuitem_status.set_label(item_print_status("Closed"))

def applet_status(w):
    subprocess.call(["xdg-open", "https://bits.poul.org"])

def applet_exit(w):
    sys.exit(0)

def item_print_status(status):
    return "BITS Status: %s" % status

##### Main here

status_string = "Reaching server..."
menuitem_status = gtk.MenuItem(item_print_status(status_string))
ind = appindicator.Indicator ("bits-gtk-client",
                                "window-close-symbolic",
                                appindicator.CATEGORY_APPLICATION_STATUS)

if __name__== "__main__":
    #initialize and start websocket in a different thread
    ws = BitsWS(opened_callback, closed_callback)
    thread.start_new_thread(ws.start_websocket, ())

    #necessary to display the icon on the status bar
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_attention_icon ("indicator-messages-new")

    #create all the items
    #menuitem_status is global
    # TODO: make an object
    menuitem_status.connect("activate", applet_status)
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