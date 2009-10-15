from elixir import *

metadata.bind = "sqlite:///tests.sqlite"
metadata.bind.echo = False

class Test(Entity):
    author = Field(Unicode(30))
    title = Field(Unicode(30))
    time = Field(Integer)
    instructions = Field(Unicode(256))
    version = Field(Integer)
    password = Field(Unicode(30))
    category = Field(Unicode(30))
    item = OneToMany('Item', cascade="all")

    def __repr__(self):
        return "<Test %s ,by %s>"%(self.title.encode('utf8'), self.author.encode('utf8'))

class Item(Entity):
    order = Field(Integer)
    type = Field(Unicode(3))
    test = ManyToOne('Test')
    question = OneToOne('Question', inverse='item', cascade="all")
    option = OneToMany('Option', cascade="all ")

    def __repr__(self):
        return "<Item %s, type: %s, test: %s>"%(self.order, self.type.encode('utf8'), self.test)

class Question(Entity):
    text = Field(Unicode(256))
    img = Field(Unicode(30))
    item = ManyToOne('Item')

    def __repr__(self):
        return "<Question %s, img %s, item %s>"%(self.text.encode('utf8'), self.img.encode('utf8'), self.item)

class Option(Entity):
    correct = Field(Boolean)
    text = Field(Unicode(256))
    img = Field(Unicode(30))
    item = ManyToOne('Item')

    def __repr__(self):
        return "<Option %s, img %s, correct: %s, item %s>"%(self.text.encode('utf8'), self.img.encode('utf8'), self.correct, self.item)
