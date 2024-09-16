Dlouhodobé sledování české knižní produkce a jejího hodnocení na čtenářských platformách. Časem posbíraná data napoví věci, např. do jakých období směrují nakladatelství novinky, která předvánoční anketa knihám pomáhá nejvíc, jak se liší popisy knih psanými muži a ženami atd.

Hlavní pipeline (novinky): novinky z Martinusu → CSV (momentálně v ```.gitignore```, čili ne zde) → ISBNs nepřekladových knih vydaných v letech 2023 a 2024 periodicky do Goodreads a Databáze knih → JSON (ve složce ```data```).

Pobočná pipeline (knihy od roku 1901): ruční stažení [České národní biografie](https://ezdroje.muni.cz/prehled/zdroj.php?lang=cs&id=20) do složky ```downloads```, rozsekání na menší XML, konverze na JSON, jejich profiltrování a export do JSONu, který neuvaří notebook.

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

    - Městské knihovny pro info o rozpůjčovanosti (zřejmě však příliš mnoho bandwidthu pro málo zajímavostí).
    - Knihobot / Trh knih pro info o dostupnosti (dtto).
    - Wikidata pro biografické údaje o autorstvu.