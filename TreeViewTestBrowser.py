#encoding:utf-8
#!/usr/bin/env python

import gtk, pygtk

class TreeViewTestBrowser(gtk.TreeView):
    """ do przegladania listy testów """

    def __init__(self, items, listStore, labels = ['Id', 'Tytuł', 'Instrukcje', 'Wersja'], tv_type='tests'):
        gtk.TreeView.__init__(self, listStore)

        self.listStore = listStore

        self.treeView = gtk.TreeView(self.listStore)
        self.tvCol0 = gtk.TreeViewColumn(labels[0])
        self.tvCol1 = gtk.TreeViewColumn(labels[1])
        self.tvCol2 = gtk.TreeViewColumn(labels[2])
        self.tvCol3 = gtk.TreeViewColumn(labels[3])
        if tv_type == 'answers':
            self.tvCol4 = gtk.TreeViewColumn(labels[4])
        
        if tv_type == 'tests':
            for test in items:
#                print test.instructions
                if type(test.instructions) is unicode:
                    self.listStore.append([test.id, test.title, test.instructions[:50], test.version])
                else:
                    self.listStore.append([test.id_unq, test.title, test.instructions.text[:50], test.version])
        elif tv_type == 'answers':
            for item in items:
                listStore_list = [item.get('id'),]
                for option in item.getchildren():
                    listStore_list.append({'True': 'Prawda', 'False': 'Fałsz'}[str(option)])
                for x in range(len(listStore_list),5):
                    listStore_list.append('')
                print item.get('all_correct')
                if item.get('all_correct') == 'true':
                    listStore_list.append('green')
                else:
                    listStore_list.append('red')
                print listStore_list
                self.listStore.append(listStore_list)
        elif tv_type == 'results':
            for result in items:
                self.listStore.append([result.getchildren()[1], result.points, result.points_percentage, result.ts_created])

        self.append_column(self.tvCol0)
        self.append_column(self.tvCol1)
        self.append_column(self.tvCol2)
        self.append_column(self.tvCol3)
        if tv_type == 'answers':
            self.append_column(self.tvCol4)

        self.cell0 = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        self.cell3 = gtk.CellRendererText()
        if tv_type == 'answers':
            self.cell4 = gtk.CellRendererText()
            self.cell0.set_property('cell-background','red')

        self.tvCol0.pack_start(self.cell0, False)
        self.tvCol1.pack_start(self.cell1, False)
        self.tvCol2.pack_start(self.cell2, False)
        self.tvCol3.pack_start(self.cell3, False)
        if tv_type == 'answers':
            self.tvCol4.pack_start(self.cell4, False)

        if tv_type == 'answers':
            self.tvCol0.set_attributes(self.cell0, text=0, cell_background=5)
            self.tvCol1.set_attributes(self.cell1, text=1, cell_background=5)
            self.tvCol2.set_attributes(self.cell2, text=2, cell_background=5)
            self.tvCol3.set_attributes(self.cell3, text=3, cell_background=5)
            self.tvCol4.set_attributes(self.cell4, text=4, cell_background=5)
        else:
            self.tvCol0.set_attributes(self.cell0, text=0)
            self.tvCol1.set_attributes(self.cell1, text=1)
            self.tvCol2.set_attributes(self.cell2, text=2)
            self.tvCol3.set_attributes(self.cell3, text=3)
            

        self.treeView.set_search_column(0)

        self.tvCol0.set_sort_column_id(0)
        self.tvCol1.set_sort_column_id(1)
        self.tvCol2.set_sort_column_id(2)
        self.tvCol3.set_sort_column_id(3)
        if tv_type == 'answers':
            self.tvCol3.set_sort_column_id(4)
