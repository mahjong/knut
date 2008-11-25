from elixir import *

metadata.bind = "sqlite:///tests.sqlite"
metadata.bind.echo = True

class Test(Entity):
    author = Field(Unicode(30))
    license = Field(Unicode(30))
    title = Field(Unicode(30))
    mode = Field(Unicode(4))
    time = Field(Integer)
    instructions = Field(Unicode(256))
    language = Field(Unicode(2))
    item = OneToMany('Item', cascade="all")

    def __repr__(self):
        return "<Test %s ,by %s>"%(self.title, self.author)

class Item(Entity):
    order = Field(Integer)
    type = Field(Unicode(3))
    test = ManyToOne('Test')
    question = OneToOne('Question', inverse='item', cascade="all")
    option = OneToMany('Option', cascade="all ")

    def __repr__(self):
        return "<Item %s, type: %s, test: %s>"%(self.order, self.type, self.test)

class Question(Entity):
    text = Field(Unicode(256))
    img = Field(Unicode(30))
    item = ManyToOne('Item')

    def __repr__(self):
        return "<Question %s, img %s, item %s>"%(self.text, self.img, self.item)

class Option(Entity):
    correct = Field(Boolean)
    text = Field(Unicode(256))
    img = Field(Unicode(30))
    item = ManyToOne('Item')

    def __repr__(self):
        return "<Option %s, img %s, correct: %s, item %s>"%(self.text, self.img, self.correct, self.item)
