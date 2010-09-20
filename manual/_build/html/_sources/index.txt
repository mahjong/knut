.. Podręcznik użytkownika edytora testów Knut - dokumentacja

.. image:: images/Knut.gif
	:align: center

Witamy w Podręczniku użytkownika edytora testów Knut!
=====================================================

Spis treści:

* :ref:`wprowadzenie`
	* :ref:`wymagania-systemowe`
	* :ref:`instalacja-programu`
	* :ref:`usuniecie-programu`
* :ref:`tworzenie-edycja`
	* :ref:`wlasciwosci-testu`
	* :ref:`edycja-pytan`
	* :ref:`zapisywanie-testu`	
* :ref:`zarzadzanie-testami`
	* :ref:`zarzadzanie-zapisanymi`
	* :ref:`zalozenie-konta`
	* :ref:`zarzadzanie-testami-na-serwerze`
	* :ref:`zarzadzanie-wynikami`
	
.. toctree::
   :maxdepth: 2

.. _wprowadzenie:

Wprowadzenie
============ 

Edytor testów Knut to darmowy program do tworzenia i edycji testów wiedzy.
Umożliwia on przygotowanie testów, udostępnienie pytań uczniom i zebranie wyników łącznie z udzielonymi odpowiedziami.

Funkcje programu:
	*	Tworzenie i edycja testów
	*	Zarządzanie zapisanymi testami
	*	Udostępnianie testów uczniom i innym użytkownikom
	*	Edytowanie udostępnionych testów 
	*	Zarządzanie wynikami uczniów
	
.. _wymagania-systemowe:
	
Wymagania systemowe
-------------------
		
	*	System operacyjny Ubuntu 8.04 lub nowszy
	*	Komputer osobisty z procesorem 500 MHz lub szybszym
	*	conajmniej 128 MB pamięci RAM
	*	minimum 10 MB miejsca na dysku twardym 

.. _instalacja-programu:

Instalacja programu
-------------------

Program można pobrać ze strony knutest.org. Należy wybrać program Knut App i zapisać go na dysku. Po podwójnym kliknięciu w plik aplikacji pojawi sie okno instalacji.
	
	.. image:: images/Instalacja.png

Należy kliknąć na przycisk "Zainstaluj pakiet" i wprowadzić hasło administratora. Po chwili pojawi się komunikat o zakończonej istalacji. Program Knut będzie widoczny w menu systemu (Programy -> Edukacja -> Edytor testów Knut).

	.. image:: images/MenuPoInstalacji.png

.. _usuniecie-programu:

Usunięcie programu
------------------

Aby usunąć program należy uruchomić komendę ``sudo apt-get remove knutapp`` w terminalu i wprowadzić hasło administratora. Polecenie to usunie wszystkie pliki programu oprócz testów i ustawień użytkownika, które znajdują sie na dysku twardym w katalogu ``katalog_domowy/.knutapp``. Można bezpiecznie usunąć zawartość tego katalogu jeśli nie zamierzamy korzystać z aplikacji.

.. _tworzenie-edycja:

Tworzenie i edycja testu
========================

Aby utworzyć nowy test należy wybrać z menu okna programu ``Test`` a następnie ``Nowy`` lub użyć skrótu klawiaturowego ``Ctrl + N``. Pojawi się wtedy okno właściwości testu.

	.. image:: images/NowyTest.png 

.. _wlasciwosci-testu:

Właściwości testu
-----------------

Właściwości testu:
	*	opisują test
	*	pomogają go odnaleźć
	*	zawierają instrukcje dla uczniów
	*	mogą zawierać hasło zabezpieczające przed nieupoważnionym pobraniem (np. nauczyciel podaje hasło w klasie i wszyscy uczniowie mogą równocześnie pobrać test). 

Okno edycji właściwości	* :ref:`Założenie konta i konfiguracja ustawień serwera`
	* :ref:`Zarządzanie testami na serwerze (zdalnie)`
	* :ref:`Zarządzanie wynikami i odpowiedziami` testu

	.. image:: images/WlasciwosciTestu.png 
		:alt: Edycja właściwości testu

Okno edycji właściwości testu pojawia się zawsze przy tworzeniu nowego testu, można również zmienić je wywołać po zapisaniu testu.

Wszystkie pola oprócz hasła sa wymagane. Jeśli hasło jest pozostawione puste, test będzie publiczny i każdy będzie mógł go pobrać i rozwiązać. W przeciwnym wypadku uczeń zostanie poproszony o hasło przed pobraniem testu.

Pozostałe pola używane są do identyfikacji testu i wyjaśnienia zdjącemu zasady testu.
Po uzupełnieniu właściwości testu program przechodzi do edycji testu (jeśli tworzymy nowy test)

.. _edycja-pytan:

Edycja pytań
------------

Ekran edycji pytań wyświetla się po uzupełnieniu właściwości testu lub po rozpoczęciu edycji testu już istniejącego.


Ekran edycji pytań
	
	.. image:: images/OknoEdycjiPytania.png
	
Ekran edycji pytania składa się z 3 części:
	*	sekcji nawigacji pomiędzy pytaniami z numerem akutalnego pytania i liczby wszystkich pytań oraz przycisków nawigacyjnych do zmiany pytania na poprzednie i następne
	*	sekcji pytania z polem tesktowym i możliwościa dodania obrazka
	*	sekcji wyboru typu odpowiedzi i pól odpowiedzi
	
Program pozwala na tworzenie pytań:
	*	jednokrotnego wyboru
	*	wielkrotnego wyboru
	*	prawda/fałsz

Pytanie jak i odpowiedzi mogą zawierać obrazek. Po kliknięciu w przycisk "Dodaj obrazek" pojawia się okno dialogowe pozwalające na wybór pliku graficznego w formacie png/jpeg/gif. 

.. _zapisywanie-testu:

Zapisywanie testu i ponowna edycja	
----------------------------------

Zapisywanie poszczególnych pytań następuje po przejściu na następne/poprzednie pytanie. Po uzupełnieniu wszystkich pól pytania i naciścnięciu przycisku 'Następne' lub 'Poprzednie' program zaspiuje pytanie i przechodzi do pytania w wybranym kierunku.

Po przygotowaniu pytań test pojawi się na liście testów w bazie lokalnej. Funkcjonalność ta jest opisana w części XXX

.. _zarzadzanie-testami:

Zarządzanie testami, komunikacja z serwerem
===========================================

Po utworzeniu testy znajdują sie na komputerze użytkownika. Udostępnienie testu dla innych użytkowników edytora testów i uczniów odbywa się pośrednictwem serwera. Serwerem może być dowolny komputer w sieci z zainstalowanym kodem serwera dostępnym na knutest.org.
W tej części podręcznika użytkownika opisane jest zarządzanie testami i odpowiedziami uczniów.

.. _zarzadzanie-zapisanymi:

Zarządzanie zapisanymi testami
------------------------------

Wyświetlenie testów dostępnych na dysku uzyskujemy przez wybranie z menu okna programu ``Test`` a następnie ``Przeglądaj Lokalnie`` lub użyć skrótu klawiaturowego ``F2``

	.. image:: images/PrzegladajLokalnie.png

Test będące aktualnie na dysku wyświetlane są w formie tabeli.

	.. image:: images/TestyLokalnie.png

W pierwszej kolumnie znajduje się id testu, jest to numer porządkowy z bazy danych. 

W kolejnych dwóch kolumnach jest tytuł i instrukcje testu podane w oknie edycji właściwości testu. 

Ostatnia kolumna zawiera wersję testu. Kolejny numer wersji testu jest przydzielany po każdej edycji. Test nowo utworzony ma wersje 1. Jeśli edytujemy jego pytania raz, wersja zmieni się na 2. Wersja przydzielana jest przez program i użytkownik nie ma możliwości jej zmiany.

Okno przeglądania testów ma dodatkowo przyciski pozwalające na manipulację zapisanymi testami. Są to kolejno:
	*	``Edytuj pytania`` - otwiera pytania wybranego testu (otwiera okno edycji pytań na pierwszym pytaniu)
	*	``Edytuj właściwości`` - otwiera okno edycji właściwości wybranego testu
	*	``Usuń`` - usuwa wybrany test z dysku, nie możliwości odzyskania usuniętego testu
	*	``Wyślij na serwer`` - wysyła test na serwer przez co umożliwia innym użytkownikom pobranie testu (więcej na ten temat w kolejnych rozdziałach)
	*	``Drukuj`` - otwiera okno menedżera drukowania testu

.. _zalozenie-konta:

Założenie konta i konfiguracja ustawień serwera
-----------------------------------------------

Do udostępniania testów wymagane jest konto na serwerze i odpowiednia konfiguracja edytora testów.

Istnieje możliwość założenia konta na knutest.org, w tym celu należy napisać e-mail na adres wiktor.idzikowski@gmail.com. Administrator serwera przydzieli nam nazwę użytkownika i hasło. Dane te należy wprowadzić do edytora testów.

W celu wprowadzenia ustawień serwera należy wybrać z menu okna programu ``Serwer`` a następnie ``Preferencje`` lub użyć skrótu klawiaturowego ``F5``. Pojawi się wtedy okno ustawień serwera.

	.. image:: images/UstawieniaSerwera.png

Pojawi się wtedy okno ustawień serwera.

	.. image:: images/OknoUstawienSerwera.png

Do komunikacji z serwerem wymagane są:

	*	Adres serwera - adres serwera w sieci bez http i www np. ``knutest.org``
	*	Login - podany przez administratora serwera, np. ``jankowalski``
	*	Hasło - podane przez administratora serwera, np. ``maslo``
	
Wszystkie pola są wymagane do udostępniania testów.

Kolejne rozdziały opisują funkcje edytora testów wymagające poprawnych ustawień serwera.

.. _zarzadzanie-testami-na-serwerze:

Zarządzanie testami na serwerze
-------------------------------

Edytor testów pozwala na współdzielenie testów z uczniami i innymi użytkownikami programu. Przeglądanie testów dostępnych na serwerze uzyskuję się poprzez wybranie z menu okna programu ``Test`` a następnie ``Preferencje`` lub użycie skrótu klawiaturowego ``F3``

	.. image:: images/PrzegladajSerwer.png
	
W rezultacie pojawi się lista dostępnych testów lub komunikat o braku testów na serwerze.

Test dostępne na serwerze wyświetlane są w formie tabeli.

	.. image:: images/PrzegladajNaSerwerze.png
	
Okno przegladania testów zawiera 4 kolumny:
	*	``Id`` - unikalne id testu, przydatne do odnalezienia i identyfikacji testu
	*	``Tytuł`` - tytuł testu
	*	``Instrukcje`` - intrukcje przydatne przy rozwiązywaniu testu
	*	``Wersja`` - wersja testu

Okno przeglądania testów na serwerze ma dodatkowo przyciski pozwalające na manipulację testami. Są to kolejno:
	*	``Usuń z serwera`` - usuwa test z serwera
	*	``Pobierz wyniki`` - pobiera wyniki uczniów, którzy rozwiązywali test
	*	``Pobierz z serwera`` - pobiera test z serwera. Pobrany test będzie dostępny do edycji i pojawi się na liście testów lokalnych.
	
.. _zarzadzanie-wynikami:

Zarządzanie wynikami i odpowiedziami
------------------------------------

Program umożliwia przeglądanie wyników i poszczególnych odpowiedzi uczniów. Odpowiedzi uczniów zapisywane są na serwerze i są dostępne dla osoby, która ułożyła dany test. Aby przejść do ekranu z wynikami należy na ekranie przeglądnia testów wybrać ``Pobierz wyniki``.

Wyniki ucznia wyświetlane są w formie tabeli.

	.. image:: images/WynikiUcznia.png
	
Okno wyników zawiera 4 kolumny:
	
	*	``Id Ucznia`` - identyfikator ucznia
	*	``Punkty`` - wynik testu wyrażony w punktach
	*	``Wynik procentowo`` - wynik testu wyrażony procentowo
	*	``Data`` - data odesłania wyników

Istnieje możliwość zobaczenia odpowiedzi ucznia na poszczególne pytania. W tym celu należy kliknąć na wybrany wynik i następnie na przycisk ``Pobierz odpowiedzi``. Pojawi się wtedy lista pytań i udzielonych odpowiedzi.



Ekran odpowiedzi ucznia na poszczególne pytania .

	.. image:: images/OdpowiedziUcznia.png
	