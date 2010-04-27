Witamy w dokumentacji Knut-a - Aplikacji do Tworzenia Testów
================================================================

Jest to dokumentacja techniczna przeznaczona dla programistów, którzy chcą zrozumieć jak działa Knut - edytor testów. Składa się ona z opisu klas, atrybutów i metod.

Program został napisany w języku `Python <http://python.org>`_, przy użyciu wrappera `PyGTK <http://www.pygtk.org>`_ biblioteki `GTK+ <http://gtk.org>`_. Do części okienek wykorzystywany był kreator interfejsów użytkownika `Glade <http://glade.gnome.org>`_.

Zawartość:

* :ref:`knut`
* :ref:`questionframe`
* :ref:`answerframe`
* :ref:`dbmodel`

  * :ref:`dbmodel-test`
  * :ref:`dbmodel-item`
  * :ref:`dbmodel-question`
  * :ref:`dbmodel-option`


.. toctree::
   :maxdepth: 2

.. _knut:

Knut - Główna klasa z logiką programu
=====================================


.. automodule:: Knut

.. autoclass:: Knut
	:members:
	:undoc-members:
 	
	
.. _questionframe:

QuestionFrame - Klasa ramki pytania
=====================================

.. automodule:: QuestionFrame

.. autoclass:: QuestionFrame
	:members:
	:undoc-members:
	
.. _answerframe:

AnswerFrame - Klasa ramki w której znajdują się możliwe odpowiedzi
==================================================================

.. automodule:: AnswerFrame

.. autoclass:: AnswerFrame
	:members:
	:undoc-members:
	
.. _dbmodel:

Opis klas bazy danych
======================

.. automodule:: dbmodel


	.. _dbmodel-test:

	Klasa opisująca tabelę testów
	=============================
	
	.. autoclass:: Test
		:members:
		:undoc-members:

	.. _dbmodel-item:

	Klasa opisująca tabelę elementów testu
	======================================
	
	.. autoclass:: Item
		:members:
		:undoc-members:

	.. _dbmodel-question:

	Klasa opisująca tabelę pytań
	============================
	
	.. autoclass:: Question   
		:members:
		:undoc-members:
	
	.. _dbmodel-option:

	Klasa opisująca tabelę możliwych odpowiedzi
	===========================================

	.. autoclass:: Option
		:members:
		:undoc-members:
	
Indeksy i tabele
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
