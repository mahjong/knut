#encoding:utf-8
#!/usr/bin/env python

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade 
except:
    sys.exit(1)

class Knut:
    """ Główne okno programu """
    def __init__(self):
        self.gladefile = "MainWindow.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
    
        self.main_vbox = self.wTree.get_widget("main_vbox")

        dic = {"on_mainWindow_destroy":self.destroy_main_window,
               "on_test_new_activate":self.test_new,
               "on_test_open_activate":self.test_open,
               "on_test_save_activate":self.test_save,
               "on_test_save_as_activate":self.test_save_as,
               "on_test_quit_activate":self.test_quit}
                    
        self.wTree.signal_autoconnect(dic)

    def test_new(self, widget, data=None):
        print("nowy")
        self.current_item = 0
        self.total_items = 1
        self.show_empty_item()
        
    def test_open(self, widget, data=None):
        print("otwórz")

    def test_save(self, widget, data=None):
        print("zapisz")

    def test_save_as(self, widget, data=None):
        print("zapisuje jako")

    def test_quit(self, widget, data=None):
        print("wychodze")

    def destroy_main_window(self, widget, data=None):
        print("zamykam")
        gtk.main_quit()

    def show_empty_item(self):
        self.prev_btn = gtk.Button(" << Poprzednie ")
        self.prev_btn.connect("clicked", self.prev_btn_clicked)
        self.nav_lbl = gtk.Label(" Pytanie %s/%s "%(self.current_item+1,self.total_items))
        self.next_btn = gtk.Button(" Następne >> ")
        self.next_btn.connect("clicked", self.next_btn_clicked)
        self.nav_hbox = gtk.HBox()
        self.nav_hbox.pack_start(self.prev_btn, False, False, 0)
        self.nav_hbox.pack_start(self.nav_lbl, True, False, 0)
        self.nav_hbox.pack_start(self.next_btn, False, False, 0)
        self.main_vbox.pack_start(self.nav_hbox, False, False, 0)
        

        self.main_vbox.show_all()

    def prev_btn_clicked(self, widget, data=None):
        print("Poprzednie pytanie")

    def next_btn_clicked(self, widget, data=None):
        print("Następne pytanie")
        


if __name__ == "__main__":
    k = Knut()
    gtk.main()
