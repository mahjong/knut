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
    u = unicode
    from dbmodel import *
    import TestBrowserTreeView
    import shutil
except:
    sys.exit(1)

class Knut:
    """ Główne okno programu """
    def __init__(self):

        self.test = None
        self.mainVboxStatus = 0
        wTree = gtk.glade.XML("Knut.glade","mainWindow")

        self.main_vbox = wTree.get_widget("main_vbox")

        dic = {"on_mainWindow_destroy":self.destroy_main_window,
               "on_testEOpen_activate":self.testEOpen,
               "on_test_new_activate":self.test_new,
               "on_test_open_activate":self.test_open,
               "on_test_save_activate":self.test_save,
               "on_test_save_as_activate":self.test_save_as,
               "on_test_quit_activate":self.test_quit}

        wTree.signal_autoconnect(dic)

        self.checkdb()

    def checkdb(self):
        """ Przygotowuje baze danych """
        if os.path.exists("tests.sqlite"):
            setup_all()
        else:
            setup_all(True)# tworzenie bazy

    def testEOpen(self, widget=None, data=0):
        #TODO: zmienic na browse
        self.clearMainVbox()
        self.mainVboxStatus = 2

        self.treeView = TestBrowserTreeView.TestBrowserTreeView(Test.query.offset(data).limit(10).all(), gtk.ListStore(str,str,str,str))
        self.main_vbox.pack_start(self.treeView, False, False)

        self.btnPrevPage = gtk.Button(" << Poprzednie ")
        if data!=0:
            self.btnPrevPage.connect("clicked",self.testEOpen, data-10)
        else:
            self.btnPrevPage.set_sensitive(False)
        self.labPage = gtk.Label(" Testy: %s - %s (%s)  "%((data+1), data+Test.query.offset(data).limit(10).count(), Test.query.count()))
        self.btnNextPage = gtk.Button(" Następne >> ")
        if data+10 < Test.query.count():
            self.btnNextPage.connect("clicked",self.testEOpen, data+10)
        else:
            self.btnNextPage.set_sensitive(False)

        self.browserNavigationHBox = gtk.HBox()
        self.browserNavigationHBox.pack_start(self.btnPrevPage, False, False)
        self.browserNavigationHBox.pack_start(self.labPage, True, False)
        self.browserNavigationHBox.pack_start(self.btnNextPage, False, False)

        self.main_vbox.pack_start(self.browserNavigationHBox, False, False)

        self.btnEditTest = gtk.Button(" Edytuj ")
        self.btnEditTest.connect("clicked", self.openTest)
        self.btnDeleteTest = gtk.Button(" Usuń ")
        self.btnDeleteTest.connect("clicked", self.deleteTest)
        self.btnMakeTest = gtk.Button(" Zrób ")
        self.btnMakeTest.connect("clicked", self.makeTest)
        self.browserActionsHBox = gtk.HBox()
        self.browserActionsHBox.pack_start(self.btnEditTest, False, False)
        self.browserActionsHBox.pack_start(self.btnDeleteTest, False, False)
        self.browserActionsHBox.pack_start(self.btnMakeTest, False, False)
        self.main_vbox.pack_start(self.browserActionsHBox, False, False)

        self.btnSendAll = gtk.Button(" Wyślij cały ")
        self.btnSendAll.connect("clicked", self.sendTest)
        self.btnSendQuestions = gtk.Button(" Wyślij pytania ")
        self.btnSendQuestions.connect("clicked", self.sendQuestions)
        self.browserServerActionsHBox = gtk.HBox()
        self.browserServerActionsHBox.pack_start(self.btnSendAll, False, False)
        self.browserServerActionsHBox.pack_start(self.btnSendQuestions, False, False)
        self.main_vbox.pack_start(self.browserServerActionsHBox, False, False)

        self.main_vbox.show_all()

    def sendQuestions(self, widget=None, data=None):
        print("wysylam pytania")

    def sendTest(self, widget=None, data=None):
        print("wysylam")

    def makeTest(self, widget=None, data=None):
        print("robie test")

    def deleteTest(self, widget=None, data=None):
        iter = self.treeView.get_selection().get_selected()[1]
        index = self.treeView.listStore.get_path(iter)[0]
        self.test = Test.query.offset(index).limit(1).first()
        msg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK_CANCEL)
        msg.set_title(" Usuwanie testu ")
        msg.label.set_text(" Usunąć wybrany test? ")
        if msg.run() == gtk.RESPONSE_OK:
            self.test.delete()
            session.commit()
            self.test = None

        msg.destroy()
        self.testEOpen()

    def openTest(self, widget=None, data=None):
        iter = self.treeView.get_selection().get_selected()[1]
        index = self.treeView.listStore.get_path(iter)[0]
        self.test = Test.query.offset(index).limit(1).first()
        self.current_item = 1
        self.total_items = len(self.test.item)
        if self.total_items !=0:
            self.show_item(self.test.item[0])
        else:
            self.total_items = 1

    def test_new(self, widget=None, data=None):
        print("nowy")
        self.current_item = 1
        self.total_items = 1

        all_tests = Test.query.all()
        if all_tests:
            if self.read_config(Test.query.all()[-1]): #config loaded
                self.show_item(None)
        else:
            if self.read_config(None):
                self.show_item(None)
        #przygotowanie testu
        #self.em = objectify.ElementMaker()
        #self.em._nsmap = {None:"http://mahjong.rootnode.net/kvml", "xsi":"http://www.w3.org/2001/XMLSchema-instance"} #self.test = self.em.test()
        #self.test.set("xsi:schemaLocation","http://mahjong.rootnode.net/kvml kvml.xsd")
        #print etree.tostring(self.test, pretty_print=True)

    def read_config(self, existingConfig, warning=None):
        wTree = gtk.glade.XML("Knut.glade", "configDlg")
        configDlg = wTree.get_widget("configDlg")
        enTitle = wTree.get_widget("enTitle")
        enAuthor = wTree.get_widget("enAuthor")
        txtvInstructions = wTree.get_widget("txtvInstructions")
        txtvInstructionsBuffer = txtvInstructions.get_buffer()
        enTime = wTree.get_widget("enTime")
        combbMode = wTree.get_widget("combbMode")
        combbLanguage = wTree.get_widget("combbLanguage")

        if warning: #show msg with warning
            labWarning = wTree.get_widget("labWarning")
            labWarning.set_markup('<span foreground="red"><b>Wszystkie</b> pola muszą być uzupełnione</span>')

        if existingConfig:
            enTitle.set_text(existingConfig.title)
            enAuthor.set_text(existingConfig.author)
            txtvInstructionsBuffer.set_text(existingConfig.instructions)
            enTime.set_text(str(existingConfig.time))
            combbMode.set_active({"prac":0,"test":1}.get(existingConfig.mode))
            combbLanguage.set_active({"pl":0,"en":2}.get(existingConfig.language))

        if configDlg.run() == 1: #OK
            if len(enTitle.get_text())!=0 and len(enAuthor.get_text())!=0 and txtvInstructionsBuffer.get_char_count()!=0 and len(enTime.get_text())!=0: #form is filled up
                nTitle = u(enTitle.get_text())
                nAuthor = u(enAuthor.get_text())
                insStart, insEnd = txtvInstructionsBuffer.get_bounds()
                nInstructions = u(txtvInstructionsBuffer.get_text(insStart,insEnd))
                nTime = int(enTime.get_text())
                nMode = {0:"prac",1:"test"}.get(combbMode.get_active())
                nLanguage = {0:"pl",1:"en"}.get(combbLanguage.get_active())
                self.test = Test(title=nTitle,author=nAuthor,instructions=nInstructions,time=nTime,mode=nMode,language=nLanguage)
                session.commit()
                os.mkdir("files/%s"%self.test.id)
                configDlg.destroy()
                return True
            else: # form is not filled up
                self.read_config(existingConfig, warning=True)
        else: #Cancel
            configDlg.destroy()
            return False

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

    def clearMainVbox(self):
        #usuwanie poprzednich
        if self.mainVboxStatus == 1:
            self.main_vbox.remove(self.nav_hbox)
            self.main_vbox.remove(self.question_frame)
            self.main_vbox.remove(self.answer_frame)
        if self.mainVboxStatus == 2:
            self.main_vbox.remove(self.treeView)
            self.main_vbox.remove(self.browserNavigationHBox)
            self.main_vbox.remove(self.browserActionsHBox)


    def show_item(self, item=None):
        self.clearMainVbox()
        self.mainVboxStatus = 1

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
                print("ERROR, prev_btn_clicked")

        session.commit()

    def next_btn_clicked(self, widget, data=None):
        self.validate_input()

        if self.validation_error:
            #TODO: okienko z bledem, albo komunikat w statusbarze
            print self.validation_error
        elif self.current_item == self.total_items:
            #old_item = Item.get_by(test_id=self.test.id, order=self.current_item)
            #if old_item:
            #    old_item.delete()
            #self.test.item.append(self.get_current_item())
            self.add_or_update_item()
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
                print("ERROR, next_btn_clicked")

        session.commit()

    def add_or_update_item(self):
        item = Item.get_by(test_id=self.test.id, order=self.current_item)
        type_id = self.answer_frame.answer_type_combo.get_active()
        if item:
            item.question = None
            item.options = []
            item.type = u(self.get_item_type(type_id))
            item.update()
        else:
            item = Item(order=self.current_item, type=unicode(self.get_item_type(type_id)))
            self.test.item.append(item)

        session.commit()
        dir_path = "files/%s/%s"%(self.test.id, item.order)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        start, end = self.question_frame.buffer.get_bounds()
        qtext = unicode(self.question_frame.buffer.get_text(start, end))
        img_filename = ""
        if len(self.question_frame.question_vbox.get_children()) > 2:
            img_filename = self.prepare_img(self.question_frame.img_filename, dir_path, "q")
        item.question = Question(text=qtext, img=u(img_filename))

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
                    img_filename = self.prepare_img(self.answer_frame.img_filename[i], dir_path, "op%s"%i)
                if atext or img_filename:
                    acorrect = self.answer_frame.correct_btn[i].get_active()
                    item.option.append(Option(correct=acorrect, text=unicode(atext), img=unicode(img_filename)))
        elif type_id == 4:
            if self.answer_frame.answer_combo.get_active() == 0:
                acorrect = True
            else:
                acorrect = False
            item.option.append(Option(correct=acorrect, text=u"", img=u""))
        item.update()
        session.commit()

    def prepare_img(self, img_path, dir_path, prefix):
        img_filename = os.path.basename(img_path)
        if os.path.dirname(img_path) == "":
            return img_filename
        else:
            img_filename = prefix + img_filename
            shutil.copy(img_path,os.path.join(dir_path, img_filename))
            return img_filename

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
