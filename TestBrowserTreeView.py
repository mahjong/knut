#encoding:utf-8
#!/usr/bin/env python

import gtk, pygtk

class TestBrowserTreeView(gtk.TreeView):
    """ do przegladania listy testów """

    def __init__(self, tests, listStore):
        gtk.TreeView.__init__(self, listStore)

        self.listStore = listStore

        self.treeView = gtk.TreeView(self.listStore)
        self.tvColTitle = gtk.TreeViewColumn("Tytuł")
        self.tvColAuthor = gtk.TreeViewColumn("Autor")
        self.tvColInstructions = gtk.TreeViewColumn("Instrukcje")
        self.tvColMode = gtk.TreeViewColumn("Tryb")

        for test in tests:
            self.listStore.append([test.title, test.author, test.instructions, test.mode])

        self.append_column(self.tvColTitle)
        self.append_column(self.tvColAuthor)
        self.append_column(self.tvColInstructions)
        self.append_column(self.tvColMode)

        self.cell = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        self.cell3 = gtk.CellRendererText()

        self.tvColTitle.pack_start(self.cell, False)
        self.tvColAuthor.pack_start(self.cell1, False)
        self.tvColInstructions.pack_start(self.cell2, False)
        self.tvColMode.pack_start(self.cell3, False)

        self.tvColTitle.set_attributes(self.cell, text=0)
        self.tvColAuthor.set_attributes(self.cell1, text=1)
        self.tvColInstructions.set_attributes(self.cell2, text=2)
        self.tvColMode.set_attributes(self.cell3, text=3)

        self.treeView.set_search_column(0)

        self.tvColTitle.set_sort_column_id(0)
        self.tvColAuthor.set_sort_column_id(1)
