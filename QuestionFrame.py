#encoding:utf-8
#!/usr/bin/env python

import gtk, pygtk, os

class QuestionFrame(gtk.Frame):
    """ 
    Klasa ramki pytania
    """

    def __init__(self, item, data_path):
        """
        __init__(item)
        
        Inicjalizuje okno pytania, uzupełnia pytanie danymi ze zmiennej item
    
        Argumenty
            * item - obiekt bierzącego pytania, jeśli brak to wyświetla puste pola do edycji
        """
        gtk.Frame.__init__(self)
        self.data_path = data_path
        self.set_label(" Pytanie ")
        self.text_view = gtk.TextView()
        self.text_view.set_size_request(100, 100)
        self.text_view.set_wrap_mode(gtk.WRAP_WORD)
        self.buffer = self.text_view.get_buffer()
        self.item = item
        if self.item and self.item.question.text:
            self.buffer.set_text(self.item.question.text)
        self.img_button_hbox = gtk.HBox()
        self.question_vbox = gtk.VBox()
        if self.item and self.item.question.img:
            self.img_filename = self.item.question.img
            dir_path = os.path.join(self.data_path, "test_files/%s/%s"%(self.item.test_id, self.item.order))
            self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(dir_path,self.img_filename), 200, 100)
            self.image = gtk.image_new_from_pixbuf(self.pixbuf)
            self.img_button = gtk.Button(" Zmień obrazek ")
            self.img_button.connect("clicked", self.img_button_clicked)
            self.remove_btn = gtk.Button(" Usuń obrazek ")
            self.remove_btn.connect("clicked", self.remove_img)
            self.img_button_hbox.pack_start(self.img_button, False, False, 0)
            self.img_button_hbox.pack_start(self.remove_btn, False, False, 0)
            self.question_vbox.pack_start(self.text_view, False, False, 0)
            self.question_vbox.pack_start(self.img_button_hbox, False, False, 5)
            self.question_vbox.pack_start(self.image, False, False , 5)
        else:
            self.img_button = gtk.Button(" Dodaj obrazek ")
            self.img_button.connect("clicked", self.img_button_clicked)
            self.img_button_hbox.pack_start(self.img_button, False, False, 0)
            self.question_vbox.pack_start(self.text_view, False, False, 0)
            self.question_vbox.pack_start(self.img_button_hbox, False, False, 5)
        self.add(self.question_vbox)

    def img_button_clicked(self, widget=None, data=None):
        """
        Otwiera okno wyboru pliku i wyświetla wybrany obrazek w sekcji pytania
        
        Argumenty
            * widget - opcjonalnie, widżet, który wywołał metodę
            * data  - opcjonalnie, dodatkowe dane zdefiniowane przy łączeniu 
        """

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
            self.add_img(dialog.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            print "canceled"
        dialog.destroy()

    def add_img(self, img_filename):
        """
        Zmienia lub wyświetla nowy obrazek
        
        Argumenty
            * img_filename - ścieżka do obrazka
        """
        if len(self.question_vbox.get_children()) > 2:
            self.question_vbox.remove(self.image)
            self.img_button_hbox.remove(self.remove_btn)
            if os.path.dirname(self.img_filename) == "":
                os.remove("test_files/%s/%s/%s"%(self.item.test_id, self.item.order, self.img_filename))


        self.img_filename = img_filename
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
        self.image = gtk.image_new_from_pixbuf(self.pixbuf)
        self.img_button.set_label(" Zmień obrazek ")
        self.remove_btn = gtk.Button(" Usuń obrazek ")
        self.remove_btn.connect("clicked", self.remove_img)
        self.img_button_hbox.pack_start(self.remove_btn, False, False, 0)
        self.question_vbox.pack_start(self.image, False, False , 5)
        self.show_all()

    def remove_img(self, widget=None):
        """
        Usuwa obrazek z pytania
        
        Argumenty
            * widget - opcjonalnie, widżet, który wywołał metodę
        """
        self.img_button_hbox.remove(self.remove_btn)
        self.question_vbox.remove(self.image)
        self.img_button.set_label(" Dodaj obrazek ")
        if os.path.dirname(self.img_filename) == "":
            os.remove("test_files/%s/%s/%s"%(self.item.test_id, self.item.order, self.img_filename))
        self.img_filename = None

if __name__ == "__main__":
    import Knut
    k = Knut.Knut()
    gtk.main()
