#encoding:utf-8
#!/usr/bin/env python

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

import gtk
import gtk.glade
import QuestionFrame
import AnswerFrame
from lxml import etree, objectify
import os
u = unicode
from dbmodel import *
import TreeViewTestBrowser
import shutil
import tarfile
import httplib
import mimetools

class Knut:
    """ Główne okno programu """
    def __init__(self):
 
        self.test = None
        self.mainVboxStatus = 0
        self.program_mode = None
        self.load_server_conf()
        wTree = gtk.glade.XML("Knut.glade","mainWindow")
 
        self.vbox_main = wTree.get_widget("vbox_main")
 
        dic = {"on_mainWindow_destroy":self.destroy_main_window,
               "on_test_new_activate":self.test_new,
               "on_test_browse_activate":self.test_browse,
               "on_test_list_download_activate":self.test_list_download,
               "on_test_quit_activate":self.destroy_main_window,
               "on_server_settings_activate":self.show_server_config_window}
 
        wTree.signal_autoconnect(dic)
 
        self.checkdb()
        
    def test_new(self, widget=None, data=None):
        """ Tworzenie nowego testu """

        self.current_item = 1
        self.total_items = 1

        all_tests = Test.query.all()
        self.test = None
        if all_tests:
            if self.read_config(existingConfig=all_tests[-1]): #config loaded
                self.show_item(None)
        else:
            if self.read_config(existingConfig=None):
                self.show_item(None)

    def test_browse(self, widget=None, data=0):
        """ Przeglądanie testów z bazy danych """

        self.clearMainVbox()
        self.program_mode = 2

        self.treeView = TreeViewTestBrowser.TreeViewTestBrowser(Test.query.offset(data).limit(10).all(), gtk.ListStore(str,str,str))
        self.vbox_main.pack_start(self.treeView, False, False)

        self.btn_prev_page = gtk.Button(" << Poprzednie ")
        if data!=0:
            self.btn_prev_page.connect("clicked",self.test_browse, data-10)
        else:
            self.btn_prev_page.set_sensitive(False)
        self.labPage = gtk.Label(" Testy: %s - %s (%s)  "%((data+1), data+Test.query.offset(data).limit(10).count(), Test.query.count()))
        self.btn_next_page = gtk.Button(" Następne >> ")
        if data+10 < Test.query.count():
            self.btn_next_page.connect("clicked",self.test_browse, data+10)
        else:
            self.btn_next_page.set_sensitive(False)

        self.hbox_browser_navigation = gtk.HBox()
        self.hbox_browser_navigation.pack_start(self.btn_prev_page, False, False)
        self.hbox_browser_navigation.pack_start(self.labPage, True, False)
        self.hbox_browser_navigation.pack_start(self.btn_next_page, False, False)

        self.vbox_main.pack_start(self.hbox_browser_navigation, False, False)

        self.btn_test_open = gtk.Button(" Edytuj pytania ")
        self.btn_test_open.connect("clicked", self.test_open, data)
        self.btn_test_edit_settings = gtk.Button(" Edytuj właściwości")
        self.btn_test_edit_settings.connect("clicked", self.test_edit_settings, data)
        self.btn_test_delete = gtk.Button(" Usuń ")
        self.btn_test_delete.connect("clicked", self.test_delete, data)
        self.btn_upload = gtk.Button(" Wyślij na serwer ")
        self.btn_upload.connect("clicked", self.test_upload, data)
        self.hbox_browser_actions = gtk.HBox()
        self.hbox_browser_actions.pack_start(self.btn_test_open, False, False)
        self.hbox_browser_actions.pack_start(self.btn_test_edit_settings, False, False)        
        self.hbox_browser_actions.pack_start(self.btn_test_delete, False, False)
        self.hbox_browser_actions.pack_start(self.btn_upload, False, False)
        self.vbox_main.pack_start(self.hbox_browser_actions, False, False)

        self.vbox_main.show_all()

    def test_list_download(self, widget=None, data=None, get_config=True):
        """ Przeglądanie testów z serwera """

        if (not self.server_conf) or self.server_conf==['']:
            self.show_msg(" Brak ustawień serwera ")
            return None
        
        boundary = mimetools.choose_boundary()
        body_list = []
        body_list = ["--%s--"%boundary, "Content-Disposition: form-data; name=login", "", self.server_conf[1], "--%s--"%boundary, "Content-Disposition: form-data; name=password", "", self.server_conf[2], "--%s--"%boundary]
        body = "\r\n".join(body_list)
        headers = {"Content-Type": "multipart/form-data; boundary=%s"%boundary, "Content-Length": str(len(body))}
        connection = httplib.HTTPConnection(self.server_conf[0])
        connection.request("POST","/test_list/", body, headers)
        response = connection.getresponse()
        re = response.read()
        try:
            self.tests = objectify.fromstring(re)
            if self.tests.countchildren() > 0:
                self.test_browse_from_server()
            else:
                msg = gtk.MessageDialog(message_format=" Na serwerze nie ma testów ",flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
                msg.set_title(" Błąd ")
                msg.run()
                msg.destroy()
        except:
            self.show_msg(" Nie udało się pobrać listy testów ")
            return None

    def show_msg(self, msg):
        msg = gtk.MessageDialog(message_format=msg,flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
        msg.set_title(" Błąd ")
        msg.run()
        msg.destroy()
        self.program_mode = 0

    def test_browse_from_server(self, widget=None, data=0):
        self.clearMainVbox()
        self.program_mode = 3
        self.treeView = TreeViewTestBrowser.TreeViewTestBrowser(self.tests.test[data:data+10], gtk.ListStore(str,str,str))
        self.vbox_main.pack_start(self.treeView, False, False)

        self.btn_prev_page = gtk.Button(" << Poprzednie ")
        if data!=0:
            self.btn_prev_page.connect("clicked",self.test_browse_from_server, data-10)
        else:
            self.btn_prev_page.set_sensitive(False)
        self.labPage = gtk.Label(" Testy: %s - %s (%s)  "%((data+1), data+len(self.tests.test[data:data+10]), self.tests.countchildren()))
        self.btn_next_page = gtk.Button(" Następne >> ")
        if data+10 < Test.query.count():
            self.btn_next_page.connect("clicked",self.test_browse_from_server, data+10)
        else:
            self.btn_next_page.set_sensitive(False)

        self.hbox_browser_navigation = gtk.HBox()
        self.hbox_browser_navigation.pack_start(self.btn_prev_page, False, False)
        self.hbox_browser_navigation.pack_start(self.labPage, True, False)
        self.hbox_browser_navigation.pack_start(self.btn_next_page, False, False)

        self.vbox_main.pack_start(self.hbox_browser_navigation, False, False)

        self.btn_test_delete_from_server = gtk.Button(" Usuń z serwera ")
        self.btn_test_delete_from_server.connect("clicked", self.test_delete_from_server, data)
        self.btn_test_download = gtk.Button(" Pobierz z serwera ")
        self.btn_test_download.connect("clicked", self.test_download, data)
        self.hbox_browser_actions = gtk.HBox()
        self.hbox_browser_actions.pack_start(self.btn_test_delete_from_server, False, False)
        self.hbox_browser_actions.pack_start(self.btn_test_download, False, False)
        self.vbox_main.pack_start(self.hbox_browser_actions, False, False)

        self.vbox_main.show_all()

    def test_delete_from_server(self, widget, data):
        self.get_current_test(data)
        boundary = mimetools.choose_boundary()
        body_list = []
        body_list = ["--%s--"%boundary, "Content-Disposition: form-data; name=login", "", self.server_conf[1], "--%s--"%boundary, "Content-Disposition: form-data; name=password", "", self.server_conf[2], "--%s--"%boundary]
        body = "\r\n".join(body_list)
        headers = {"Content-Type": "multipart/form-data; boundary=%s"%boundary, "Content-Length": str(len(body))}
        connection = httplib.HTTPConnection(self.server_conf[0])
        connection.request("POST","/test_delete/%s/"%self.test_id, body, headers)
        response = connection.getresponse()
        re = response.read()
        if re == "OK":
            text = " Test usunięto "
        else:
            f = open("error.html", "w")
            f.write(re)
            f.close()
            text = " Nie usunięto testu "

        msg = gtk.MessageDialog(message_format=text,flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        msg.set_title(" Usuwanie testu ")
        msg.run()
        msg.destroy()

        self.clearMainVbox()
        self.test_list_download(get_config=False)

    def test_download(self, widget, data):
        self.get_current_test(data)

        self.test = Test()
        session.commit()
        os.mkdir("files/%s"%self.test.id)

        boundary = mimetools.choose_boundary()
        body_list = []
        body_list = ["--%s--"%boundary, "Content-Disposition: form-data; name=login", "", self.server_conf[1], "--%s--"%boundary, "Content-Disposition: form-data; name=test-password", "", str(self.server_conf[2]), "--%s--"%boundary, "Content-Disposition: form-data; name=test-title", "", str(self.test_title), "--%s--"%boundary]
        body = "\r\n".join(body_list)
        headers = {"Content-Type": "multipart/form-data; boundary=%s"%boundary, "Content-Length": str(len(body))}
        connection = httplib.HTTPConnection(self.server_conf[0])
        connection.request("POST","/questions_download/", body, headers)
        response = connection.getresponse()
        if response.reason != "OK":
            f = open("error.html", "w")
            f.write(response.read())
            f.close()
            self.test.delete()
            os.rmdir("files/%s/"%self.test.id)
            return ""

        questions_file = open("files/%s/questions.tar.bz2"%self.test.id, "w")
        questions_file.write(response.fp.read())
        questions_file.close()

        body_list = []
        body_list = ["--%s--"%boundary, "Content-Disposition: form-data; name=login", "", self.server_conf[1], "--%s--"%boundary, "Content-Disposition: form-data; name=test-password", "", str(self.server_conf[2]), "--%s--"%boundary, "Content-Disposition: form-data; name=test-title", "", str(self.test_title), "--%s--"%boundary]
        body = "\r\n".join(body_list)
        headers = {"Content-Type": "multipart/form-data; boundary=%s"%boundary, "Content-Length": str(len(body))}
        connection = httplib.HTTPConnection(self.server_conf[0])
        connection.request("POST","/answers_download/", body, headers)
        response = connection.getresponse()
        if response.reason != "OK":
            f = open("error.html", "w")
            f.write(response.read())
            f.close()
            self.test.delete()
            os.rmdir("files/%s/"%self.test.id)
            return ""

        answers_file = open("files/%s/answers.xml"%self.test.id, "w")
        answers_file.write(response.fp.read())
        answers_file.close()
        
        #zapisanie testu
        questions_file = tarfile.open("files/%s/questions.tar.bz2"%self.test.id,"r")
        questions_file.extractall(path="files/%s/"%self.test.id)
        os.remove("files/%s/questions.tar.bz2"%self.test.id)

        test_xml = objectify.parse("files/%s/test.xml"%self.test.id).getroot()
        answers_xml = objectify.parse("files/%s/answers.xml"%self.test.id).getroot()
        
        self.test.title = u(test_xml.config.title)
        self.test.author = u(test_xml.config.author)
        self.test.instructions = u(test_xml.config.instructions)
        self.test.time = int(test_xml.config.time)
        self.test.password = u(test_xml.config.password)
        self.test.version = int(test_xml.config.version)
        session.commit()
        
        test_xml.remove(test_xml.config)
        
        
        for item_xml, answer_xml in zip(test_xml.getchildren(), answers_xml.getchildren()):
            item_type = u(item_xml.get("type"))
            item = Item(order=int(item_xml.get("id")), type=item_type)
            self.test.item.append(item)
            session.commit()
            
            if item_xml.question.text == None:
                question_text = u''
            else:
                question_text = u(item_xml.question.text)
                
            if item_xml.question.get("img") == None:
                question_img = u''
            else:
                question_img = u(item_xml.question.get("img"))
            
            item.question = Question(text = question_text, img = question_img)
            item_xml.remove(item_xml.question)
            
            if item_type == "txt":
                item.option.append(Option(correct=True, text=u(answer_xml.option[0].text), img=u''))
            elif item_type == "t/f":
                item.option.append(Option(correct={'true':True, 'false':False}[answer_xml.option[0].get("correct")], text=u'', img=u''))
            else:
                for option_xml, answer_option_xml in zip(item_xml.getchildren(), answer_xml.getchildren()):
                    if option_xml.text == None:
                        option_text = u''
                    else:
                        option_text = u(option_xml.text)
                        
                    if option_xml.get("img") == None:
                        option_img = u''
                    else:
                        option_img = u(option_xml.get("img"))
                        
                    option_correct = {'true':True, 'false':False}[answer_option_xml.get("correct")]
                    item.option.append(Option(correct=option_correct, text=option_text, img=option_img ))
            
            item.update()
            session.commit()

        

    def test_delete(self, widget=None, data=None):
        self.get_current_test(data)
        msg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK_CANCEL)
        msg.set_title(" Usuwanie testu ")
        msg.label.set_text(" Usunąć wybrany test? ")
        if msg.run() == gtk.RESPONSE_OK:
            shutil.rmtree("files/%s/"%self.test.id)
            self.test.delete()
            session.commit()
            self.test = None

        msg.destroy()
        self.test_browse()

    def test_open(self, widget=None, data=None):
        self.get_current_test(data)
        self.test.version += 1
        session.commit()
        self.current_item = 1
        self.total_items = len(self.test.item)
        if self.total_items !=0:
            self.show_item(self.test.item[0])
        else:
            self.total_items = 1
            self.show_item(None)

    def test_edit_settings(self, widget=None, data=None):
        self.get_current_test(data)
        self.read_config(self.test)
        self.test_browse()


    def read_config(self, existingConfig, warning=None):
        wTree = gtk.glade.XML("Knut.glade", "testConfigDlg")
        configDlg = wTree.get_widget("testConfigDlg")
        enTitle = wTree.get_widget("enTitle")
        enAuthor = wTree.get_widget("enAuthor")
        txtvInstructions = wTree.get_widget("txtvInstructions")
        txtvInstructionsBuffer = txtvInstructions.get_buffer()
        enTime = wTree.get_widget("enTime")
        enPassword = wTree.get_widget("enPasswd")

        if warning: #show msg with warning
            labWarning = wTree.get_widget("labWarning")
            labWarning.set_markup('<span foreground="red"><b>Wszystkie</b> pola muszą być uzupełnione</span>')

        if existingConfig:
            try:
                enTitle.set_text(existingConfig.title)
                enAuthor.set_text(existingConfig.author)
                txtvInstructionsBuffer.set_text(existingConfig.instructions)
                enTime.set_text(str(existingConfig.time))
                enPassword.set_text(existingConfig.password)
            except:
                print("ERROR: incorrect config data")

        if configDlg.run() == 1: #OK
            if (not self.test) and len(enTitle.get_text())!=0 and len(enAuthor.get_text())!=0 and txtvInstructionsBuffer.get_char_count()!=0 and len(enTime.get_text())!=0 and len(enPassword.get_text())!=0: #form is filled up
                nTitle = u(enTitle.get_text())
                nAuthor = u(enAuthor.get_text())
                insStart, insEnd = txtvInstructionsBuffer.get_bounds()
                nInstructions = u(txtvInstructionsBuffer.get_text(insStart,insEnd))
                nTime = int(enTime.get_text())
                nPassword = u(enPassword.get_text())
                self.test = Test(title=nTitle,author=nAuthor,instructions=nInstructions,time=nTime,password=nPassword, version=1)
                session.commit()
                os.mkdir("files/%s"%self.test.id)
                configDlg.destroy()
                return True
            elif len(enTitle.get_text())!=0 and len(enAuthor.get_text())!=0 and txtvInstructionsBuffer.get_char_count()!=0 and len(enTime.get_text())!=0 and len(enPassword.get_text())!=0:
                self.test.title = u(enTitle.get_text())
                self.test.author = u(enAuthor.get_text())
                insStart, insEnd = txtvInstructionsBuffer.get_bounds()
                self.test.instructions = u(txtvInstructionsBuffer.get_text(insStart,insEnd))
                self.test.time = int(enTime.get_text())
                self.test.password = u(enPassword.get_text())
                self.test.update()
                session.commit()
                configDlg.destroy()
                return True
            else: # form is not filled up
                configDlg.destroy()
                return self.read_config(existingConfig, warning=True)
        else: #Cancel
            configDlg.destroy()
            return False
       
    def load_server_conf(self):
        
        if os.path.exists("settings.txt"):
            settings_file = file("settings.txt","rb")
            self.server_conf = settings_file.read().split(';')
        else:
            self.server_conf = None  
        
    def show_server_config_window(self, warning=None):

        wTree = gtk.glade.XML("Knut.glade", "serverConfigDlg")
        serverConfigDlg = wTree.get_widget("serverConfigDlg")
        enAddress = wTree.get_widget("enAddress")
        enLogin = wTree.get_widget("enLogin")
        enPassword = wTree.get_widget("enPassword")
        
        if self.server_conf and self.server_conf!=['']:
            enAddress.set_text(self.server_conf[0])
            enLogin.set_text(self.server_conf[1])
            enPassword.set_text(self.server_conf[2])
                       

        if warning == True:
            labWarning = wTree.get_widget("labWarning2")
            labWarning.set_markup('<span foreground="red"><b>Wszystkie</b> pola muszą być uzupełnione</span>')

        if serverConfigDlg.run() == 1: #OK
            if len(enAddress.get_text())!=0 and len(enLogin.get_text())!=0 and len(enPassword.get_text())!=0:
                serverConfigDlg.destroy()
                self.server_conf = [enAddress.get_text(), enLogin.get_text(), enPassword.get_text()]
            else:
                serverConfigDlg.destroy()
                self.show_server_config_window(warning=True)
        else:
            serverConfigDlg.destroy()

    def test_upload(self, widget=None, data=None):
        self.get_current_test(data)
        self.show_server_config_window()
        #przygotowanie testu
        em = objectify.ElementMaker()
        em._nsmap = {None:"http://mahjong.rootnode.net/kvml"}
        xml_test = em.test()
        config = em.config()
        config.append(em.title(self.test.title))
        config.append(em.author(self.test.author))
        config.append(em.instructions(self.test.instructions))
        config.append(em.time(self.test.time))
        config.append(em.version(self.test.version))
        config.append(em.password(self.test.password))
        xml_test.append(config)

        xml_answers = em.answers()

        for db_item in Item.query.filter_by(test_id=self.test.id).all():
            xml_item = em.item()
            xml_item_answer = em.item()
            xml_item.set("id",str(db_item.order))
            xml_item_answer.set("id", str(db_item.order))
            xml_item.set("type",db_item.type)
            db_question = Question.get_by(item_id=db_item.id)
            if db_question.text:
                xml_question = em.question(db_question.text)
                if db_question.img:
                    xml_question.set("img",db_question.img)
            elif db_question.img:
                xml_question = em.question()
                xml_question.set("img",db_question.img)
            else:
                print("BLAD: question")
            xml_item.append(xml_question)

            for db_option in Option.query.filter_by(item_id=db_item.id).all():
                if db_option.text:
                    xml_option = em.option(db_option.text)
                    if db_item.type == "txt":
                        xml_option_answer = em.option(db_option.text)
                    else:
                        xml_option_answer = em.option()
                        if db_option.img:
                            xml_option.set("img",db_option.img)
                        xml_item.append(xml_option)
                elif db_option.img:# tylko obrazek
                    xml_option = em.option()
                    xml_option.set("img",db_option.img)
                    xml_option_answer = em.option()
                    xml_item.append(xml_option)
                else:# prawda/fałsz
                    xml_option_answer = em.option()

                xml_option_answer.set("correct",str(db_option.correct).lower())
                xml_item_answer.append(xml_option_answer)

            xml_test.append(xml_item)
            xml_answers.append(xml_item_answer)
        print etree.tostring(xml_test, pretty_print=True)
        print("-"*20)
        print(etree.tostring(xml_answers, pretty_print=True))
        xml_file_path = "files/%s/test.xml"%self.test.id
        xml_file = open(xml_file_path,"w")
        xml_file.write(etree.tostring(xml_test, pretty_print=True, encoding="utf-8", xml_declaration=True))
        xml_file.close()

        os.chdir("files/%s"%self.test.id)
        tar_file_name = "questions.tar.bz2"
        tar_file_path = "files/%s/%s"%(self.test.id, tar_file_name)
        tar_file = tarfile.open(tar_file_name ,"w:bz2")
        for file in os.listdir("."):
            tar_file.add(file)
        tar_file.close()
        os.chdir("../..")

        os.remove("files/%s/test.xml"%self.test.id)
        xml_file_answers_path = "files/%s/answers.xml"%self.test.id
        xml_file_answers = open(xml_file_answers_path, "w")
        xml_file_answers.write(etree.tostring(xml_answers, pretty_print=True, encoding="utf-8", xml_declaration=True))
        xml_file_answers.close()

        self.post_files(tar_file_path, xml_file_answers_path)

        os.remove(xml_file_answers_path)
        os.remove(tar_file_path)

    def post_files(self, tar_file_path, answers_file_path):
        """ wysyła archiwum z testem i odpowiedzi na serwer """
        tar_file_name = os.path.basename(tar_file_path)
        answers_file_name = os.path.basename(answers_file_path)
        print(tar_file_name,answers_file_name)
        boundary = mimetools.choose_boundary()
        tar_file = open(tar_file_path, "rb")
        answers_file = open(answers_file_path, "rb")
        body_list = []
        body_list = ["--%s--"%boundary, "content-disposition: form-data; name=tarfile; filename=%s"%tar_file_name.encode('utf8'), "content-type: application/x-gtar","", tar_file.read(), "--%s--"%boundary, "","--%s--"%boundary, "content-disposition: form-data; name=answers_xml; filename=%s"%answers_file_name.encode("utf8"), "content-type: application/xml", "", answers_file.read(), "--%s--"%boundary, "", "--%s--"%boundary, 'Content-Disposition: form-data; name="login"', "", self.server_conf[1], "--%s--"%boundary, 'Content-Disposition: from-data; name="password"', "", self.server_conf[2], "--%s--"%boundary, 'Content-Disposition: from-data; name="title"', "", self.test.title.encode('utf8'), "--%s--"%boundary, 'Content-Disposition: from-data; name="instructions"', "", self.test.instructions.encode('utf8'), "--%s--"%boundary, 'Content-Disposition: from-data; name="version"', "", str(self.test.version), '--%s--'%boundary, 'Content-Disposition: from-data; name="test-password"', "", self.test.password.encode('utf8'), '--%s--'%boundary]
        tar_file.close()
        answers_file.close()
        body = "\r\n".join(body_list)
        headers = {"content-type":"multipart/form-data; boundary=%s"%boundary, "content-length":str(len(body))}
        connection = httplib.HTTPConnection(self.server_conf[0])
        connection.request("POST","/test_upload/", body, headers)
        response = connection.getresponse()
        re = response.read()
        if re == "OK":
            text = " Test wysłany "
        else:
            text = " Nie wysłano testu "

        msg = gtk.MessageDialog(message_format=text,flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        msg.set_title(" Wysyłanie testu ")
        msg.run()
        msg.destroy()

    def get_current_test(self, data):
        """ zapisuje test w zmiennej self.test """
        if self.program_mode == 1: #zapisz jesli nie ma bledow
            self.validate_input()
            if not self.validation_error:
                self.add_or_update_item()
        elif self.program_mode == 2: #wybierz zaznaczony test
            iter = self.treeView.get_selection().get_selected()[1]
            index = self.treeView.listStore.get_path(iter)[0]
            self.test = Test.query.offset(data+index).limit(1).first()
        elif self.program_mode == 3:
            iter = self.treeView.get_selection().get_selected()[1]
            index = self.treeView.listStore.get_path(iter)[0]
            self.test_id = self.tests.test[data+index].id
            self.test_password = self.tests.test[data+index].password
            self.test_title = self.tests.test[data+index].title

    def destroy_main_window(self, widget, data=None):
        
        if self.server_conf and self.server_conf!=['']:
            settings_file = file("settings.txt","w")
            settings_file.write("%s;%s;%s"%(self.server_conf[0],self.server_conf[1],self.server_conf[2]))
            settings_file.close()
        print("zamykam")
        gtk.main_quit()

    def clearMainVbox(self):
        #usuwanie poprzednich
        print self.program_mode
        if self.program_mode == 1:
            self.vbox_main.remove(self.nav_hbox)
            self.vbox_main.remove(self.question_frame)
            self.vbox_main.remove(self.answer_frame)
        if self.program_mode in (2,3):
            self.vbox_main.remove(self.treeView)
            self.vbox_main.remove(self.hbox_browser_navigation)
            self.vbox_main.remove(self.hbox_browser_actions)


    def show_item(self, item=None):
        self.clearMainVbox()
        self.program_mode = 1

        #nawigacja po pytaniach
        self.prev_btn = gtk.Button(" << Poprzednie ")
        self.prev_btn.connect("clicked", self.prev_btn_clicked)
        if self.current_item == 1:
            self.prev_btn.set_sensitive(False)
        self.nav_lbl = gtk.Label(" Pytanie %s/%s "%(self.current_item,self.total_items))
        self.next_btn = gtk.Button(" Następne >> ")
        self.next_btn.connect("clicked", self.next_btn_clicked)
        self.nav_hbox = gtk.HBox()
        self.nav_hbox.pack_start(self.prev_btn, False, False, 0)
        self.nav_hbox.pack_start(self.nav_lbl, True, False, 0)
        self.nav_hbox.pack_start(self.next_btn, False, False, 0)
        self.vbox_main.pack_start(self.nav_hbox, False, False, 0)

        #pytanie
        self.question_frame = QuestionFrame.QuestionFrame(item)
        self.vbox_main.pack_start(self.question_frame, False, False, 0)

        #odpowiedź
        self.answer_frame = AnswerFrame.AnswerFrame(item)
        self.vbox_main.pack_start(self.answer_frame, False, False, 0)

        self.vbox_main.show_all()

    def prev_btn_clicked(self, widget, data=None):
        self.validate_input()

        if self.current_item == self.total_items and self.validation_error:
            self.current_item -= 1
            self.total_items -= 1
            self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))
        elif self.validation_error:
        #TODO: popup z informacja
            print self.validation_error
        else:
            self.add_or_update_item()
            self.current_item -= 1
            self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))

    def next_btn_clicked(self, widget, data=None):
        self.validate_input()

        if self.validation_error:
            #TODO: okienko z bledem, albo komunikat w statusbarze
            print self.validation_error
        else:
            self.add_or_update_item()
            if self.current_item == self.total_items:
                self.total_items += 1
            self.current_item += 1
            self.show_item(Item.get_by(test_id=self.test.id, order=self.current_item))

    def add_or_update_item(self):
        item = Item.get_by(test_id=self.test.id, order=self.current_item)
        type_id = self.answer_frame.answer_type_combo.get_active()
        if item:
            item.question.delete()
            for op in item.option:
                op.delete()
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

        if type_id == 1:#txt
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
        
    def checkdb(self):
        """ Przygotowuje baze danych """
        if os.path.exists("tests.sqlite"):
            setup_all()
        else:
            setup_all(True)# tworzenie bazy

    def validate_input(self):
        self.validation_error = ""

        if (self.question_frame.buffer.get_char_count() == 0) and (len(self.question_frame.question_vbox.get_children()) < 3):
            self.validation_error = "Brak pytania\n"
        elif (self.answer_frame.answer_type_combo.get_active() == 0):
            self.validation_error += "Nie wybrano rodzaju odpowiedzi\n"
        #jesli wybrano txt to nie sprawdzam, pytanie otwarte
        elif (self.answer_frame.answer_type_combo.get_active() == 1) and (self.answer_frame.buffer.get_char_count() == 0):
            self.validation_error += "Brak odpowiedzi"
        elif (self.answer_frame.answer_type_combo.get_active() in (2,3)) and not (self.answer_frame.buffer[0].get_char_count() or self.answer_frame.image.get(0) or
                                                                                  self.answer_frame.buffer[1].get_char_count() or self.answer_frame.image.get(1) or
                                                                                  self.answer_frame.buffer[2].get_char_count() or self.answer_frame.image.get(2) or
                                                                                  self.answer_frame.buffer[3].get_char_count() or self.answer_frame.image.get(3)):
            self.validation_error += "Brak odpowiedzi"

        #print self.validation_error

if __name__ == "__main__":
    k = Knut()
    gtk.main()
