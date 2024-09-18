Dlouhodobé sledování české knižní produkce a jejího hodnocení na čtenářských platformách. Časem posbíraná data napoví věci, např. do jakých období směrují nakladatelství novinky, která předvánoční anketa knihám pomáhá nejvíc, jak se liší popisy knih psanými muži a ženami atd.

Hlavní pipeline (čerstvé knihy): novinky z Martinusu → CSV (momentálně v ```.gitignore```, čili ne zde) → ISBNs nepřekladových knih vydaných v letech 2023 a 2024 periodicky do Goodreads a Databáze knih → JSON (ve složce ```data```).

Pobočná pipeline (všechny knihy): ruční stažení [České národní biografie](https://ezdroje.muni.cz/prehled/zdroj.php?lang=cs&id=20) do složky ```downloads```, rozsekání na menší XML, konverze na JSON, jejich profiltrování a export do JSONu, který neuvaří notebook.

Užitečné klíče k datům ČNB:

    - [MARC 21](https://www.loc.gov/marc/bibliographic/)
    - [formální deskriptory](https://text.nkp.cz/o-knihovne/odborne-cinnosti/zpracovani-fondu/Archiv/formalnideskriptory-1)
    - [Pravidla indexace beletrie se zaměřením na situaci v českých knihovnách](https://is.muni.cz/th/d8dtu/DIPLOMKA_NACISTO.pdf)

Todo:

- Pročištění dat ČNB:

    - pokusit se zmáčknout kompletní archiv na velikost použitelnou na laptopu – rozsekat po sloupcích / odstranit duplikáty / vybrat první vydání / optimalizovat datatypy atd.
    - oddělit fyzické výtisky (brožované, vázané) a zbytek
    - menší dataframy: původní beletrie, původní nonfikce apod.
    - zdokonalovat filtrování starší beletrie bez identifikace v poli 072_a
        - laciný trik: jednoznačné autorstvo beletrie do seznamu a jím filtrovat starší knihy
    - do slovníku lidsky srozumitelné názvy sloupců pro překlad pro export

- Přidat/přidávat (viz bod níže) ISBN z ČNB do seznamu knih ke scrapování.

- Automatizovat stahování dat ČNB (prý je aktualizují ca jednou týdně, bohužel jen v kompletním balíku; zároveň mi ze záhadných důvodů nefungoval wget ani curl).

- Scrapovat toho z knihkupectví víc:

    - ukázky e-booků
    - info o bestsellerech
    - čtenářské hodnocení
    - obálky

- Pokusit se získat informace o přesných datech vydání. Něco je na Goodreads, ne moc spolehlivé. Pro nové knihy: kdy se poprvé změnilo předpokládané datum vydání na vyšlo? 

- Poziční válka s antiscrapovacími opatřeními Goodreads: další kolo je evidovat odmítnuté požadavky, zkusit je stáhnout ještě jednou.

- Scrapovat z Goodreads i počty jednotlivých hvězdičkových hodnocení (ratingsCountDist).

- Scrapovat z Goodreads i cifru "added" (není v HTML, rvou to tam nějakým JS, bude nutné Selenium).

- Napojit další zdroje dat:

    - městské knihovny pro info o rozpůjčovanosti (zřejmě však příliš mnoho bandwidthu pro málo zajímavostí)
    - Knihobot / Trh knih pro info o dostupnosti (dtto)
    - Wikidata pro biografické údaje o autorstvu (alternativně Personální autority od NK)