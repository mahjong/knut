#encoding:utf-8
#!/usr/bin/env python

import gtk, pygtk

class TreeViewTestBrowser(gtk.TreeView):
    """ do przegladania listy testów """

    def __init__(self, tests, listStore):
        gtk.TreeView.__init__(self, listStore)

        self.listStore = listStore

        self.treeView = gtk.TreeView(self.listStore)
        self.tvColTitle = gtk.TreeViewColumn("Tytuł")
        self.tvColInstructions = gtk.TreeViewColumn("Instrukcje")
        self.tvColVersion = gtk.TreeViewColumn("Wersja")

        for test in tests:
            self.listStore.append([test.title, test.instructions, test.version])

        self.append_column(self.tvColTitle)
        self.append_column(self.tvColInstructions)
        self.append_column(self.tvColVersion)

        self.cell = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()

        self.tvColTitle.pack_start(self.cell, False)
        self.tvColInstructions.pack_start(self.cell1, False)
        self.tvColVersion.pack_start(self.cell2, False)

        self.tvColTitle.set_attributes(self.cell, text=0)
        self.tvColInstructions.set_attributes(self.cell1, text=1)
        self.tvColVersion.set_attributes(self.cell2, text=2)

        self.treeView.set_search_column(0)

        self.tvColTitle.set_sort_column_id(0)
        self.tvColInstructions.set_sort_column_id(1)
        self.tvColVersion.set_sort_column_id(2)
