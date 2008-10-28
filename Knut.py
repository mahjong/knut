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
        
        self.test_new()

    def test_new(self, widget=None, data=None):
        print("nowy")
        self.current_item = 0
        self.total_items = 1
        self.show_item(None)#wyswietla niewypelniony pytanie

        #przygotowanie testu
        self.em = objectify.ElementMaker()
        self.em._nsmap = {None:"http://mahjong.rootnode.net/kvml", "xsi":"http://www.w3.org/2001/XMLSchema-instance"}
        self.test = self.em.test()
        self.test.set("xsi:schemaLocation","http://mahjong.rootnode.net/kvml kvml.xsd")
        print etree.tostring(self.test, pretty_print=True)
        
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
        self.nav_lbl = gtk.Label(" Pytanie %s/%s "%(self.current_item+1,self.total_items))
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
        print("Poprzednie pytanie")

    def next_btn_clicked(self, widget, data=None):
        self.validate_input()
        if self.validation_error:
            # okienko z bledem, albo komunikat w statusbarze
            pass 
        elif (self.current_item+1) == self.total_items:
            self.test.append(self.get_current_item())
            self.current_item += 1
            self.total_items +=1
            self.show_item(None) 
            # dodaj kolejne pytanie
        else: # zapisz i wczytaj nastepne
            pass

        print etree.tostring(self.test, pretty_print=True)

    def get_current_item(self):
        item = self.em.item()
        item.set("id",str(self.current_item))
        type_id = self.answer_frame.answer_type_combo.get_active()
        item.set("type",self.get_item_type(type_id))
        start, end = self.question_frame.buffer.get_bounds()
        qtext = self.question_frame.buffer.get_text(start, end)
        if qtext:
            question = self.em.question(qtext)
            if len(self.question_frame.question_vbox.get_children()) > 2:
                question.set("img",self.question_frame.img_filename)
        else:
            question = self.em.question()
            question.set("img",self.question_frame.img_filename)
        item.append(question)

        if type_id == 1 and self.answer_frame.buffer.get_char_count() != 0:
            start, end = self.answer_frame.buffer.get_bounds()
            atext = self.answer_frame.buffer.get_text(start,end)
            item.append(self.em.option(atext,correct="true"))
        elif type_id in (2,3):
            for i in range(4):
                if self.answer_frame.buffer[i].get_char_count() !=0:
                    start, end = self.answer_frame.buffer[i].get_bounds()
                    option = self.em.option(self.answer_frame.buffer[i].get_text(start,end))
                    if len(self.answer_frame.option_vbox[i].get_children()) > 2:
                        option.set("img",self.answer_frame.img_filename[i])
                    option.set("correct",str(self.answer_frame.correct_btn[i].get_active()).lower())
                    item.append(option)
                elif len(self.answer_frame.option_vbox[i].get_children()) > 2:
                    option = self.em.option()
                    option.set("img",self.answer_frame.img_filename[i])
                    option.set("correct",str(self.answer_frame.correct_btn[i].get_active()).lower())
                    item.append(option)
        elif type_id == 4:
            option = self.em.option()
            if self.answer_frame.answer_combo.get_active() == 0:
                option.set("correct", "true")
            else:
                option.set("correct", "false")
            item.append(option)
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
