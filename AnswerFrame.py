#encoding:utf-8
#!/usr/bin/env python

import gtk, pygtk

class AnswerFrame(gtk.Frame):
    """ Klasa zawierająca elementy odpowiedzi """

    def __init__(self, item=None):
        gtk.Frame.__init__(self)
        self.set_label(" Odpowiedź ")
        self.answer_type_combo = gtk.combo_box_new_text()
        self.answer_type_combo.insert_text(0, " Wybierz typ odpowiedzi ")
        self.answer_type_combo.insert_text(1, " Tekstowa ")
        self.answer_type_combo.insert_text(2, " Jednokrotnego wyboru ")
        self.answer_type_combo.insert_text(3, " Wielokrotnego wyboru ")
        self.answer_type_combo.insert_text(4, " Prawda/Fałsz ")
        self.answer_type_combo.set_active(0)
        self.answer_type_combo.connect("changed", self.answer_type_combo_changed)
        self.answer_vbox = gtk.VBox()
        self.answer_vbox.pack_start(self.answer_type_combo, False, False, 0)
        self.add(self.answer_vbox)

    def answer_type_combo_changed(self, widget=None, data=None):
        
        if len(self.answer_vbox.get_children()) > 1:#usuwanie poprzednich
           self.answer_vbox.remove(self.answer_vbox.get_children()[1])


        if self.answer_type_combo.get_active() == 1:# Tekstowa
           self.text_view = gtk.TextView()
           self.text_view.set_size_request(100,100)
           self.text_view.set_wrap_mode(gtk.WRAP_WORD)
           self.buffer = self.text_view.get_buffer()
           self.answer_vbox.pack_start(self.text_view, False, False, 5)
        elif self.answer_type_combo.get_active() in (2,3):
            self.text_view  = {}
            self.buffer = {}
            self.option_vbox = {} 
            self.img_button = {}
            self.img_button_hbox = {}
            self.text_view_hbox = {}
            self.pixbuf = {}
            self.image = {}
            self.img_filename = {}
            self.remove_btn = {}
            self.correct_btn = {}
            index = 0
            self.table = gtk.Table(2,2,False)   
            self.table.set_row_spacings(10)
            self.table.set_col_spacings(10)
            for i in range(2):
                for j in range(2):
                    self.text_view[index] = gtk.TextView()
                    self.text_view[index].set_size_request(250,100)
                    self.text_view[index].set_wrap_mode(gtk.WRAP_WORD)
                    self.buffer[index] = self.text_view[index].get_buffer()
                    if self.answer_type_combo.get_active() == 2:# jednokrotnego wyboru
                        if index == 0:
                            self.correct_btn[0] = gtk.RadioButton()
                        else:
                            self.correct_btn[index] = gtk.RadioButton(self.correct_btn[0])
                    elif self.answer_type_combo.get_active() == 3:# wielokrotnego wyboru
                        self.correct_btn[index] = gtk.CheckButton()
                    self.text_view_hbox[index] = gtk.HBox(False, 0)
                    self.text_view_hbox[index].pack_start(self.text_view[index], False, False, 5)
                    self.text_view_hbox[index].pack_start(self.correct_btn[index], False, False, 0)
                    self.img_button[index] = gtk.Button(" Dodaj obrazek ")
                    self.img_button[index].connect("clicked", self.img_button_clicked, index)
                    self.img_button_hbox[index] = gtk.HBox(False, 0)
                    self.img_button_hbox[index].pack_start(self.img_button[index], False, False, 0)
                    self.option_vbox[index] = gtk.VBox(False, 0)
                    self.option_vbox[index].pack_start(self.text_view_hbox[index], False, False, 0)
                    self.option_vbox[index].pack_start(self.img_button_hbox[index], False, False, 0)
                    self.table.attach(self.option_vbox[index],i,i+1,j,j+1)
                    index += 1 
            
            self.answer_vbox.pack_start(self.table, False, False, 10) 
        elif self.answer_type_combo.get_active() == 4:
            self.answer_combo = gtk.combo_box_new_text()
            self.answer_combo.insert_text(0, " Prawda ")
            self.answer_combo.insert_text(1, " Fałsz ")
            self.answer_combo.set_active(0)
            self.answer_vbox.pack_start(self.answer_combo, False, False, 10)

        self.show_all()

    def img_button_clicked(self, widget=None, data=None):
        print("dodaje obrazek")

        dialog = gtk.FileChooserDialog(" Dodaj obrazek... ",
                                 None,
                                 gtk.FILE_CHOOSER_ACTION_OPEN, 
                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                  gtk.STOCK_OPEN, gtk.RESPONSE_OK ))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Wszystkie pliki")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("Obrazki")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.add_img(dialog.get_filename(), data)
        elif response == gtk.RESPONSE_CANCEL:
            print "canceled"
        dialog.destroy()
        
    def add_img(self, img_filename, index):
        if len(self.option_vbox[index].get_children()) > 2:
            self.option_vbox[index].remove(self.image[index])
            self.img_button_hbox[index].remove(self.remove_btn[index])

        self.img_filename[index] = img_filename
        self.pixbuf[index] = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
        self.image[index] = gtk.image_new_from_pixbuf(self.pixbuf[index])
        self.remove_btn[index] = gtk.Button(" Usuń obrazek ")
        self.remove_btn[index].connect("clicked", self.remove_img, index)
        self.img_button[index].set_label(" Zmień obrazek ")
        self.img_button_hbox[index].pack_start(self.remove_btn[index], False, False, 0)
        self.option_vbox[index].pack_start(self.image[index], False, False , 5)
        self.show_all() 

    def remove_img(self, widge, index):
        self.img_button_hbox[index].remove(self.remove_btn[index])
        self.option_vbox[index].remove(self.image[index])
        self.img_button[index].set_label(" Dodaj obrazek ")

import Knut
if __name__ == "__main__":
    k = Knut.Knut()
    gtk.main()
