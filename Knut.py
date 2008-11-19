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
    import QuestionFrame
    import AnswerFrame
    from lxml import etree, objectify
    import os
    from dbmodel import *
except:
    sys.exit(1)

class Knut:
    """ Główne okno programu """
    def __init__(self):

        self.test = None


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

        self.checkdb()

        self.test_new()

    def checkdb(self):
        """ Przygotowuje baze danych """
        if os.path.exists("tests.sqlite"):
            setup_all()
        else:
            setup_all(True)# tworzenie bazy

    def test_new(self, widget=None, data=None):
        print("nowy")
        self.current_item = 1
        self.total_items = 1
        self.show_item(None)#wyswietla niewypelniony pytanie

        #na razie nie tworze nowego, testu, tylko uzywam istniejacego
        self.test = Test.get_by(id=1)

        #przygotowanie testu
        #self.em = objectify.ElementMaker()
        #self.em._nsmap = {None:"http://mahjong.rootnode.net/kvml", "xsi":"http://www.w3.org/2001/XMLSchema-instance"}
        #self.test = self.em.test()
        #self.test.set("xsi:schemaLocation","http://mahjong.rootnode.net/kvml kvml.xsd")
        #print etree.tostring(self.test, pretty_print=True)

    def test_open(self, widget, data=None):
        print("otworz")

    def test_save(self, widget, data=None):
        print("zapisz")
        chooser = gtk.FileChooserDialog(title=" Zapisz...", action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.save_test(chooser.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            print("anulowano")

        dialog.destroy()

    def test_save_as(self, widget, data=None):
        print("zapisuje jako")

    def test_quit(self, widget, data=None):
        print("wychodze")

    def destroy_main_window(self, widget, data=None):
        print("zamykam")
        gtk.main_quit()

    def show_item(self, item=None):
        #usuwanie poprzednich
        try:
            self.main_vbox.remove(self.nav_hbox)
            self.main_vbox.remove(self.question_frame)
            self.main_vbox.remove(self.answer_frame)
        except:
            pass#nie bylo nic do usuniecia
        #nawigacja po pytaniach
        self.prev_btn = gtk.Button(" << Poprzednie ")
        self.prev_btn.connect("clicked", self.prev_btn_clicked)
        self.nav_lbl = gtk.Label(" Pytanie %s/%s "%(self.current_item,self.total_items))
        self.next_btn = gtk.Button(" Następne >> ")
        self.next_btn.connect("clicked", self.next_btn_clicked)
        self.nav_hbox = gtk.HBox()
        self.nav_hbox.pack_start(self.prev_btn, False, False, 0)
        self.nav_hbox.pack_start(self.nav_lbl, True, False, 0)
        self.nav_hbox.pack_start(self.next_btn, False, False, 0)
        self.main_vbox.pack_start(self.nav_hbox, False, False, 0)

        #pytanie
        self.question_frame = QuestionFrame.QuestionFrame(item)
        self.main_vbox.pack_start(self.question_frame, False, False, 0)

        #odpowiedź
        self.answer_frame = AnswerFrame.AnswerFrame(item)
        self.main_vbox.pack_start(self.answer_frame, False, False, 0)

        self.main_vbox.show_all()


    def prev_btn_clicked(self, widget, data=None):
        self.validate_input()

        if self.current_item == 1:#pierwsze pytanie, nie ma poprzedniego
            print("pierwsze")
        elif self.current_item == self.total_items:
            if self.validation_error:
                self.current_item -= 1
                self.total_items -= 1
                self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))
            else:
                old_item = Item.get_by(test_id=self.test.id, order=self.current_item)
                if old_item:
                    old_item.delete()
                self.test.item.append(self.get_current_item())
                self.current_item -= 1
                self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))
        elif self.validation_error:
            print self.validation_error
        else:
            old_item = Item.get_by(test_id=self.test.id, order=self.current_item)
            if old_item:
                old_item.delete()
                self.test.item.append(self.get_current_item())
                self.current_item -= 1
                self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))
            else:
                print("ERROR")

        session.commit()

    def next_btn_clicked(self, widget, data=None):
        self.validate_input()

        if self.validation_error:
            #TODO: okienko z bledem, albo komunikat w statusbarze
            print self.validation_error
        elif self.current_item == self.total_items:

            old_item = Item.get_by(test_id=self.test.id, order=self.current_item)
            if old_item:
                old_item.delete()
            self.test.item.append(self.get_current_item())

            self.current_item += 1
            self.total_items +=1
            self.show_item(None)
        else: # zapisz i wczytaj kolejne
            old_item = Item.get_by(test_id=self.test.id, order=self.current_item)
            if old_item:
                old_item.delete()
                self.test.item.append(self.get_current_item())
                self.current_item += 1
                self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))
            else:
                print("BLAD")

        session.commit()

    def get_current_item(self):

        type_id = self.answer_frame.answer_type_combo.get_active()
        item = Item(order=unicode(self.current_item), type=unicode(self.get_item_type(type_id)))

        start, end = self.question_frame.buffer.get_bounds()
        qtext = unicode(self.question_frame.buffer.get_text(start, end))
        img_filename = u""
        if len(self.question_frame.question_vbox.get_children()) > 2:
            img_filename = unicode(self.question_frame.img_filename)
        item.question = Question(text=qtext, img=img_filename)

        if type_id == 1 and self.answer_frame.buffer.get_char_count() != 0:
            start, end = self.answer_frame.buffer.get_bounds()
            atext = self.answer_frame.buffer.get_text(start,end)
            item.option.append(Option(correct=True, text=unicode(atext), img=u""))
        elif type_id in (2,3):
            for i in range(4):
                atext = img_filename = u""
                if self.answer_frame.buffer[i].get_char_count() !=0:
                    start, end = self.answer_frame.buffer[i].get_bounds()
                    atext = self.answer_frame.buffer[i].get_text(start,end)
                if len(self.answer_frame.option_vbox[i].get_children()) > 2:
                    img_filename = self.answer_frame.img_filename[i]
                if atext or img_filename:
                    acorrect = self.answer_frame.correct_btn[i].get_active()
                    item.option.append(Option(correct=acorrect, text=unicode(atext), img=unicode(img_filename)))
        elif type_id == 4:
            if self.answer_frame.answer_combo.get_active() == 0:
                acorrect = True
            else:
                acorrect = False
            item.option.append(Option(correct=acorrect, text=u"", img=u""))

        return item

    def get_item_type(self, id):
        if id == 1:
            return "txt"
        elif id == 2:
            return "one"
        elif id == 3:
            return "mul"
        elif id == 4:
            return "t/f"

    def validate_input(self):
        self.validation_error = ""

        if (self.question_frame.buffer.get_char_count() == 0) and (len(self.question_frame.question_vbox.get_children()) < 3):
            self.validation_error = "Brak pytania\n"
        elif (self.answer_frame.answer_type_combo.get_active() == 0):
            self.validation_error += "Nie wybrano rodzaju odpowiedzi\n"
        #jesli wybrano txt to nie sprawdzam, pytanie otwarte
        #elif (self.answer_frame.answer_type_combo.get_active() == 1) and (self.answer_frame.buffer.get_char_count() == 0):
        #    self.validation_error += "Brak odpowiedzi"
        elif (self.answer_frame.answer_type_combo.get_active() in (2,3)) and not (self.answer_frame.buffer[0].get_char_count() or self.answer_frame.image.get(0) or
                                                                                  self.answer_frame.buffer[1].get_char_count() or self.answer_frame.image.get(1) or
                                                                                  self.answer_frame.buffer[2].get_char_count() or self.answer_frame.image.get(2) or
                                                                                  self.answer_frame.buffer[3].get_char_count() or self.answer_frame.image.get(3)):
            self.validation_error += "Brak odpowiedzi"

        #print self.validation_error

if __name__ == "__main__":
    k = Knut()
    gtk.main()
