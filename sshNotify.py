#!/usr/bin/env python 

import sys
import os
import gtk
import warnings

#############################################
#                                           #
#   Just put hosts.txt in the same          #
#   folder as this script and execute it !  #
#   (hosts.txt should be like :             #
#    servname:host:port                     #
#    ie : 'mydev:192.168.0.10:2200')        #
#                                           #
#############################################

#term = "xterm"
#term = "urxvt"
term = "terminator"

try:
    import egg.trayicon
except:
    print "Install eggtrayicon please :-)"
 
class EggTrayIcon:
    def __init__(self):
        self.tray = egg.trayicon.TrayIcon("SSH connections")
 
        eventbox = gtk.EventBox()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_SMALL_TOOLBAR)
 
        eventbox.connect("button-press-event", self.icon_clicked)
 
        eventbox.add(image)
        self.tray.add(eventbox)
        self.tray.show_all()
 
    def icon_clicked(self, widget, event):
        if event.button == 3:
            menu = gtk.Menu()
            sub = gtk.Menu()
            menuitem_about = gtk.MenuItem("Connect to...")
            menu.append(menuitem_about)
            menuitem_about.connect("activate", self.openTerminator)
            menu.show_all()
            menu.popup(None, None, None, event.button, event.time, self.tray)
 
    def openTerminator(self, widget):
            servers = ServerList()


class ServerList:
    def __init__(self):
        #GTK Stuff
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("SSH Servers")
        self.window.set_size_request(400, 800)
        self.window.set_border_width(10)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.connect("destroy", self.destroy)

        vbox = gtk.VBox(False, 8)
        hbox = gtk.HButtonBox()
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)
        vbox.pack_start(hbox, False)
        self.b0 = gtk.Button("Test")
        self.b1 = gtk.CheckButton("Use password")
        hbox.pack_start(self.b0)
        hbox.pack_start(self.b1)
        store = self.create_model()
        self.status = self.b1.get_active()
        treeView = gtk.TreeView(store)
        treeView.set_rules_hint(True) 
        sw.add(treeView)
        self.create_columns(treeView)
        self.window.add(vbox)
        self.window.show_all()
 
    def create_model(self):
        with open("hosts.txt") as infh:
            testdata = [tuple(line.strip().split(':')) for line in infh]
        store = gtk.ListStore(str, str, str)
        for item in testdata:
            store.append([item[0], item[1], item[2]])
        return store

    def create_columns(self, treeView):
        #The title says it all
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Server name", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Server IP", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Server port", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)

        treeView.connect('cursor-changed', self.connectTo)
 
    def connectTo(self, widget):
        #Get info from rows and launch terminator (or xterm, or whatever you want)
        model = widget.get_model()
        selec = widget.get_selection()
        itern = selec.get_selected()
        ip = model.get_value(itern[1], 1)
        port = model.get_value(itern[1], 2)
        cmd = "\"ssh -p " + port +  " root@" + ip + "\" &"
        print "Connecting to : root@" + ip + ":" + port
        os.system(term + " -e " + cmd)

    def destroy(self, widget, data=None):
        gtk.main_quit()
        return False

warnings.simplefilter('ignore') 
EggTrayIcon()
gtk.main()
