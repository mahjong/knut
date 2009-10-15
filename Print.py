#encoding:utf-8
import gtk
import pango
import cairo

class Print(gtk.PrintOperation):
    
    M_PI = 3.14159265
    test = None
    parent = None
    
    def __init__(self, test, parent=None):
        gtk.PrintOperation.__init__(self)
        self.parent = parent
        self.test = test
        self.items_num = len(test.item)
       
        self.connect("begin-print", self.__begin_print)
        self.connect("draw-page", self.__draw_page)
       
        print test.item
        res = self.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, parent)
#        res = self.run(gtk.PRINT_OPERATION_ACTION_PREVIEW, parent)

        if res == gtk.PRINT_OPERATION_RESULT_ERROR:
            error_dialog = gtk.MessageDialog(parent,
                                          gtk.DIALOG_DESTROY_WITH_PARENT,
                                          gtk.MESSAGE_ERROR,
      					  gtk.BUTTONS_CLOSE,
      					  "Error printing file:\n")
            error_dialog.connect("response", lambda w,id: w.destroy())
            error_dialog.show()

    def __begin_print(self, operation, context):
        operation.set_n_pages(self.items_num/2+1+self.items_num%2)
        #layout = context.create_pango_layout()
        #desc = pango.FontDescription("monospace 10")
        #layout.set_font_description(desc)
        #
        #layout.set_text("abc")
        #
        #height = layout.get_size()[1]/pango.SCALE
        #paper_height = context.get_height()
        #line_height = height/layout.get_line_count()
        #
        #from math import floor, ceil
        #self.n_pages = ceil(height/paper_height)
        #self.max_lines_in_page = floor(paper_height/line_height)
        #operation.set_n_pages(int(self.n_pages))
        #
        #print "number of pages: "+ repr(self.n_pages)
        #print "max lines in page: " + repr(self.max_lines_in_page)
        #print "Height of context in pixels: "+ repr(height/pango.SCALE)
        #print "Height of paper "+ repr(paper_height)

    def __draw_page(self, operation, context, page_nr):
        cr = context.get_cairo_context() 
        if page_nr == 0:#cover
            layout = context.create_pango_layout()
            layout.set_text(self.test.title)
            desc = pango.FontDescription("sans bold 28")	    
            layout.set_font_description(desc)
            width = int(context.get_width()*pango.SCALE)
            layout.set_width(width)
            layout.set_alignment(pango.ALIGN_CENTER)
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(0, 100)
            cr.show_layout(layout)
	    
            layout.set_text('Instrukcje:\n%s' % self.test.instructions)
            desc = pango.FontDescription("sans bold 20")	    
            layout.set_font_description(desc)
    	    width = int(context.get_width()*pango.SCALE)
    	    layout.set_width(width)
    	    layout.set_alignment(pango.ALIGN_CENTER)
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(0, 300)
            cr.show_layout(layout)
            
            
            layout.set_text('Powodzenia\n%s' % self.test.author)
            desc = pango.FontDescription("sans bold 12")        
            layout.set_font_description(desc)
            width = int(context.get_width()*pango.SCALE)
            layout.set_width(width)
            layout.set_alignment(pango.ALIGN_CENTER)
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(0, 600)
            cr.show_layout(layout)
            
            layout.set_text('Czas: %s minut' % self.test.time)
            desc = pango.FontDescription("sans bold 12")        
            layout.set_font_description(desc)
            width = int(context.get_width()*pango.SCALE)
            layout.set_width(width)
            layout.set_alignment(pango.ALIGN_RIGHT)
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(0, 500)
            cr.show_layout(layout)

        else:
            layout = context.create_pango_layout()
            q_number = page_nr*2 -1
            print q_number
            self.draw_item(self.test.item[q_number-1], q_number, layout, context, cr, 50)
            
            q_number = page_nr*2
            if self.items_num > q_number:
                self.draw_item(self.test.item[q_number-1], q_number, layout, context, cr, 450)
            
    def draw_item(self, item, q_number, layout, context, cr, begin_y):
        q_text = '%s. %s' % ( q_number, item.question.text)

        desc = pango.FontDescription("sans bold 14")        
        layout.set_font_description(desc)
        width = int(context.get_width()*pango.SCALE)
        layout.set_width(width)
        layout.set_alignment(pango.ALIGN_LEFT)
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(0, begin_y)
        
        if item.type in ('one', 'mul'):
            if item.question.img:
                img_filename = 'test_files/%s/%s/%s' % (self.test.id, item.order, item.question.img)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
                cr.set_source_pixbuf(pixbuf, 200 ,begin_y+50)
                cr.paint()
                begin_y += 150
            if item.type == 'one':
                layout.set_text(q_text + ' (Wybierz jedną odpowiedź)')
            else:
                layout.set_text(q_text + ' (Wybierz odpowiedzi)')
            cr.show_layout(layout)
            layout.set_width(width/2)
            layout.set_wrap(pango.WRAP_WORD_CHAR)
            layout.set_text('A) ' + item.option[0].text)
            cr.move_to(0, begin_y+50)
            cr.show_layout(layout)
            if item.option[0].img:
                img_filename = 'test_files/%s/%s/%s' % (self.test.id, item.order, item.option[0].img)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
                cr.set_source_pixbuf(pixbuf, 20 ,begin_y+50)
                cr.paint()
            layout.set_text('B) ' + item.option[1].text)
            cr.move_to(0, begin_y+150)
            cr.show_layout(layout)
            if item.option[1].img:
                img_filename = 'test_files/%s/%s/%s' % (self.test.id, item.order, item.option[1].img)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
                cr.set_source_pixbuf(pixbuf, 20 ,begin_y+150)
                cr.paint()
            layout.set_text('C) ' + item.option[2].text)
            cr.move_to(300, begin_y+50)
            cr.show_layout(layout)
            if item.option[2].img:
                img_filename = 'test_files/%s/%s/%s' % (self.test.id, item.order, item.option[2].img)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
                cr.set_source_pixbuf(pixbuf, 320 ,begin_y+50)
                cr.paint()
            layout.set_text('D) ' + item.option[3].text)
            cr.move_to(300, begin_y+150)
            cr.show_layout(layout)
            if item.option[3].img:
                img_filename = 'test_files/%s/%s/%s' % (self.test.id, item.order, item.option[3].img)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
                cr.set_source_pixbuf(pixbuf, 320 ,begin_y+150)
                cr.paint()
#            if item.option[0].img:
#                img_filename = 'test_files/%s/%s/%s' % (self.test.id, item.order, item.option[0].img)
#                print img_filename
#                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img_filename, 200, 100)
#                cr.set_source_pixbuf(pixbuf, 0 ,0)
#                cr.paint()
#            cr.move_to(50, 50)
#            cr.arc(50, 50, 5, 0, 2 * Print.M_PI)
#            cr.stroke()
        elif item.type == 't/f':
            layout.set_text(q_text)
            cr.show_layout(layout)
            layout.set_text('Prawda')
            cr.move_to(100, begin_y+100)
            cr.show_layout(layout)
            layout.set_text('Fałsz')
            cr.move_to(300, begin_y+100)
            cr.show_layout(layout)
        elif item.type == 'txt':
            layout.set_text(q_text + ' (Odpowiedź pisemna)')
            cr.show_layout(layout)
        else:
            # log error, continue
            pass
                  
            

if __name__ == '__main__':
    # requires test in db
    from dbmodel import *
    setup_all()
    p = Print(Test.query.all()[1])