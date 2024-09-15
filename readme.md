Dlouhodobé sledování české knižní produkce. Časem posbíraná data napoví věci, např. do jakých období směrují nakladatelství novinky, která předvánoční anketa knihám pomáhá nejvíc, jak se liší popisy knih psanými muži a ženami atd.

Současná pipeline: novinky z Martinusu → CSV (momentálně v ```.gitignore```) → ISBNs nepřekladových knih vydaných v letech 2023 a 2024 periodicky do Goodreads a Databáze knih → JSON (ve složce ```data```).

Todo:

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

    - [Národní knihovna](https://text.nkp.cz/o-knihovne/odborne-cinnosti/otevrena-data) pro info o knihách.
    - Městské knihovny pro info o rozpůjčovanosti (zřejmě však příliš mnoho bandwidthu pro málo zajímavostí).
    - Wikidata pro biografické údaje o autorstvu.