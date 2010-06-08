#encoding:utf-8
from elixir import *



class Test(Entity):
    """ 
    Klasa opisująca tabelę testów
    
    Opis pól:
    """
    author = Field(Unicode(30))
    """Imię i nazwisko autora (30 znaków)"""
    title = Field(Unicode(30))
    """Tytuł testu (30 znaków)"""
    time = Field(Integer)
    """Czas na ukończenie testu (liczba całkowita)"""
    instructions = Field(Unicode(256))
    """Instrukcje przydatne przy rozwiązywaniu testu (256 znaków)"""
    version = Field(Integer)
    """Wersja testu (liczba całkowita)"""
    password = Field(Unicode(30))
    """Hasło (30 znaków)"""
    category = Field(Unicode(30))
    """Kategoria w jakiej test się znajduje (30 znaków)"""
    item = OneToMany('Item', cascade="all")
    """Relacje jeden do wielu z tabelą elementów testu"""

    def __repr__(self):
        return "<Test %s ,by %s>"%(self.title.encode('utf8'), self.author.encode('utf8'))

class Item(Entity):
    """
    Klasa opisująca tabelę elementów testu
    """
    order = Field(Integer)
    """Kolejność elementu (liczba całkowita)"""
    type = Field(Unicode(3))
    """Typ elementu (3 znaki)"""
    test = ManyToOne('Test')
    """Relacja z wiele do jednego z testem"""
    question = OneToOne('Question', inverse='item', cascade="all")
    """Relacja jeden do jednego z tabelą pytań"""
    option = OneToMany('Option', cascade="all ")
    """Relacja jeden do jednego z tabelą możliwych odpowiedzi"""

    def __repr__(self):
        return "<Item %s, type: %s, test: %s>"%(self.order, self.type.encode('utf8'), self.test)

class Question(Entity):
    """
    Klasa opisująca tabelę pytań
    """
    text = Field(Unicode(256))
    """Tekst pytania (256 znaków)"""
    img = Field(Unicode(30))
    """Nazwa obrazka (30 znaków)"""
    item = ManyToOne('Item')
    """Relacja wiele do jednego z tabelą elementów testu"""

    def __repr__(self):
        return "<Question %s, img %s, item %s>"%(self.text.encode('utf8'), self.img.encode('utf8'), self.item)

class Option(Entity):
    """
    Klasa opisująca tabelę możliwych odpowiedzi
    """
    correct = Field(Boolean)
    """Poprawność odpowiedzi"""
    text = Field(Unicode(256))
    """Tekst odpowiedzi (256 znaków)"""
    img = Field(Unicode(30))
    """Nazwa obrazka (30 znaków)"""
    item = ManyToOne('Item')
    """Relacja wiele do jednego z tabelą elementów testu"""

    def __repr__(self):
        return "<Option %s, img %s, correct: %s, item %s>"%(self.text.encode('utf8'), self.img.encode('utf8'), self.correct, self.item)
