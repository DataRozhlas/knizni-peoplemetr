Dlouhodobé sledování české knižní produkce. Časem posbíraná data napoví věci, např. do jakých období směrují nakladatelství novinky, která předvánoční anketa knihám pomáhá nejvíc, jak se liší popisy knih psanými muži a ženami atd.

Současná pipeline: novinky z Martinusu → JSON (momentálně v ```.gitignore```) → ISBNs nepřekladových knih vydaných v letech 2023 a 2024 periodicky do Goodreads a Databáze knih → JSON (ve složce ```data```).

Todo:

- Dořešit aktualizace knih připravovaných k vydání – zřejmě promazáváním stažených souborů.

- Scrapovat toho z knihkupectví víc: ukázky e-booků, info o bestsellerech, čtenářské hodnocení.

- Zlepšit filtrování novinek pro sledování.

- Dofiltrovávat sledované knihy při čištění (_Havran_ tam nemá co dělat).

- Pokusit se získat informace o přesných datech vydání (něco je na Goodreads, ne moc spolehlivé).

- Scrapovat z Goodreads i cifru "added" (není v HTML, rvou to tam nějakým JS).

- Napojit další zdroje dat:

    - [Národní knihovna](https://text.nkp.cz/o-knihovne/odborne-cinnosti/otevrena-data) pro info o knihách.
    - Městské knihovny pro info o rozpůjčovanosti (zřejmě však příliš mnoho bandwidthu pro málo zajímavostí).
    - Wikidata pro biografické údaje o autorstvu.

- Dashboard s trendy.