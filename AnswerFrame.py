#encoding:utf-8
#!/usr/bin/env python

import gtk, pygtk, os

class AnswerFrame(gtk.Frame):
    """ Klasa ramki w której znajdują się możliwe odpowiedzi """

    def __init__(self, item, data_path):
        """
        __init__(item=None)
        
        Inicjalizuje ramke odpowiedzi, uzupełnia pola danymi ze zmiennej item
    
        Argumenty
            * item - obiekt bierzącego pytania, jeśli brak to wyświetla puste pola do edycji
            * data_path - zmienna tekstowa, ścieżka do katalogu z danymi testu
        """
        gtk.Frame.__init__(self)
        self.item = None
        self.data_path = data_path
        self.set_label(" Odpowiedź ")
        self.answer_type_combo = gtk.combo_box_new_text()
        self.answer_type_combo.insert_text(0, " Wybierz typ odpowiedzi ")
#        self.answer_type_combo.insert_text(1, " Tekstowa ")
        self.answer_type_combo.insert_text(1, " Jednokrotnego wyboru ")
        self.answer_type_combo.insert_text(2, " Wielokrotnego wyboru ")
        self.answer_type_combo.insert_text(3, " Prawda/Fałsz ")
        self.answer_type_combo.connect("changed", self.answer_type_combo_changed)
        self.answer_vbox = gtk.VBox()
        self.answer_vbox.pack_start(self.answer_type_combo, False, False, 0)
        if item and item.type:
            self.item = item
            self.dir_path = os.path.join(self.data_path, "test_files/%s/%s"%(self.item.test_id, self.item.order))
            self.answer_type_combo.set_active(self.get_type_index(item.type))
        else:
            self.answer_type_combo.set_active(0)
        self.add(self.answer_vbox)

    def get_type_index(self, type):
        """
        Zamienia tekst typu odpowiedzi na reprezentację liczbową
        
        Argumenty
            * type - zmienna tekstowa:
        
        Wartości zwracane
            * 'one' -> 1 - pytanie jednokrotnego wyboru
            * 'mul' -> 2 - pytanie wielokrotnego wyboru
            * 't/f' -> 3 - pytanie typu prawda/fałsz
        """
#        if type == "txt":
#            return 1
        if type == "one":
            return 1
        elif type == "mul":
            return 2
        elif type == "t/f":
            return 3

    def answer_type_combo_changed(self, widget=None, data=None):
        """
        Wyświetla pola do edycji dla danego typu odpowiedzi
        
        Argumenty
            * widget - opcjonalnie, widżet, który wywołał metodę
            * data - opcjonalnie, dodatkowe dane zdefiniowane przy łączeniu
        """
        if len(self.answer_vbox.get_children()) > 1:#usuwanie poprzednich
           self.answer_vbox.remove(self.answer_vbox.get_children()[1])


#        if self.answer_type_combo.get_active() == 1:# Tekstowa
#            self.text_view = gtk.TextView()
#            self.text_view.set_size_request(100,100)
#            self.text_view.set_wrap_mode(gtk.WRAP_WORD)
#            self.buffer = self.text_view.get_buffer()
#            if self.item and self.item.option:
#                self.buffer.set_text(self.item.option[0].text)
#            self.answer_vbox.pack_start(self.text_view, False, False, 5)
        if self.answer_type_combo.get_active() in (1,2):
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
                    if self.answer_type_combo.get_active() == 1:# jednokrotnego wyboru
                        if index == 0:
                            self.correct_btn[0] = gtk.RadioButton()
                        else:
                            self.correct_btn[index] = gtk.RadioButton(self.correct_btn[0])
                    elif self.answer_type_combo.get_active() == 2:# wielokrotnego wyboru
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
                    if self.item and len(self.item.option) > index:
                        if self.item.option[index].text:
                            self.buffer[index].set_text(self.item.option[index].text)
                        if self.item.option[index].img:
                            self.img_filename[index] = self.item.option[index].img
                            self.add_img(os.path.join(self.dir_path, self.item.option[index].img), index)
                        if self.item.option[index].correct:
                            self.correct_btn[index].set_active(True)
                        else:
                            self.correct_btn[index].set_active(False)

                    index += 1

            self.answer_vbox.pack_start(self.table, False, False)
        elif self.answer_type_combo.get_active() == 3:
            self.answer_combo = gtk.combo_box_new_text()
            self.answer_combo.insert_text(0, " Prawda ")
            self.answer_combo.insert_text(1, " Fałsz ")
            if self.item:
                if self.item.option[0].correct == True:
                    self.answer_combo.set_active(0)
                else:
                    self.answer_combo.set_active(1)
            else:
                self.answer_combo.set_active(0)
            
            self.answer_vbox.pack_start(self.answer_combo, False, False, 10)
        self.show_all()

    def img_button_clicked(self, widget=None, data=None):
        """
        Otwiera okno wyboru obrazka do danej odpowiedzi
        
        Argumenty
            * widget - opcjonalnie, widżet, który wywołał metodę
            * data - opcjonalnie, dodatkowe dane zdefiniowane przy łączeniu
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
            self.img_filename[data] = dialog.get_filename()
            self.add_img(dialog.get_filename(), data)
        elif response == gtk.RESPONSE_CANCEL:
            print "canceled"
        dialog.destroy()

    def add_img(self, img_filename, index):
        """
        Dodaje lub zamienia obrazek przy danej odpowiedzi
        
        Argumenty
            * img_filename - ścieżka do pliku obrazka
            * index - indeks odpowiedzi, w której zmienia się obrazek
        """
        if len(self.option_vbox[index].get_children()) > 2:
            self.option_vbox[index].remove(self.image[index])
            self.img_button_hbox[index].remove(self.remove_btn[index])
            if os.path.dirname(self.img_filename) == "":
                os.remove(os.path.join(self.dir_path, self.img_filename))

        self.pixbuf[index] = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
        self.image[index] = gtk.image_new_from_pixbuf(self.pixbuf[index])
        self.remove_btn[index] = gtk.Button(" Usuń obrazek ")
        self.remove_btn[index].connect("clicked", self.remove_img, index)
        self.img_button[index].set_label(" Zmień obrazek ")
        self.img_button_hbox[index].pack_start(self.remove_btn[index], False, False, 0)
        self.option_vbox[index].pack_start(self.image[index], False, False , 5)
        self.show_all()

    def remove_img(self, widget, index):
        """
        Usuwa wybrany obrazek
        
        Argumenty
            * widget - widżet, który wywołał metodę
            * index - indeks odpowiedzi, w której usuwa obrazek
        """
        self.img_button_hbox[index].remove(self.remove_btn[index])
        self.option_vbox[index].remove(self.image[index])
        self.img_button[index].set_label(" Dodaj obrazek ")
        if os.path.dirname(self.img_filename[index]) == "":
            os.remove(os.path.join(self.dir_path, self.img_filename[index]))
        self.img_filename[index] = None

if __name__ == "__main__":
    import Knut
    k = Knut.Knut()
    gtk.main()
