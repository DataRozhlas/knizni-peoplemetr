Dlouhodobé sledování české knižní produkce a jejího hodnocení na čtenářských platformách.

## Co tu je, co tu není a jak to funguje

- Ignorujte skripty a sešity do č. 049. Scrapují informace o knižních novinkách a o jejich hodnocení na platformách, tato data (za celé sledované odbobí, tzn. od dubna 2024 do posledního commitu) najdete ve složce ```data```, netřeba namáhat servery vícekrát.

- Kvůli zdejším limitům na velikost souborů naopak ve složce ```data``` nenajdete opracovaná data z České národní bibliografie („Česká národní bibliografie obsahuje záznamy dokumentů vydaných na území České republiky. Většinou se jedná o záznamy dokumentů zaslaných do Národní knihovny ČR jako povinný výtisk.“ – [viz více](https://ezdroje.muni.cz/prehled/zdroj.php?lang=cs&id=20)). Pro jejich získání je nutné spustit (v číselném/abecedním pořadí) skripty začínající 05x. Potřebné knihovny: ```lxml```, ```pymarc```, ```pandas```. Stačit by snad mělo 8 GB RAM, ale 16 je jistota.

    - Takto vygenerovaný soubor ```data/cnb_vyber.parquet``` bude obsahovat profiltrovaný dump ČNB s knihami vydanými po roce 1900. Filtr lze zkontrolovat ve skriptu č. 053.

    - Složka ```data/cnb_sloupce``` bude obsahovat kompletní sloupce (knihy i neknihy od roku 1800) z původního dumpu. Lze si je tedy přidat do vyfiltrovaného datasetu anebo z nich poskládat dataset nový.

- V obou případech je nutné mít na paměti, že při konverzi z XML do JSONu mohlo dojít k chybám. Jedna věc, o které vím: tam, kde má jeden pod knihou podepsaný člověk uvedeno v poli 700_4 více rolí (např. autor+ilustrátor), nesou opracovaná data informaci pouze o první z nich.

Užitečné klíče k datům ČNB:

- [MARC 21](https://www.loc.gov/marc/bibliographic/)
- [Formální deskriptory](https://text.nkp.cz/o-knihovne/odborne-cinnosti/zpracovani-fondu/Archiv/formalnideskriptory-1)
- [Pravidla indexace beletrie se zaměřením na situaci v českých knihovnách](https://is.muni.cz/th/d8dtu/DIPLOMKA_NACISTO.pdf)
- Nejdůležitější kódy viz níže.

## To-do

- Průběžně ladit všechny filtry řádků při přípravě souborů ```cnb_vyber.parquet``` i ```aut_vyber.parquet```. Nejsem knihovník, je možné, že tam mám chyby a vyhazuju něco, co nemám.

- Umístit funkce pro hledání roku vydání, čísla vydání atd. do ```src``` a odtud importovat do skriptů a sešitů.

- skript 050: Ověřit, že jsou stažené archivy větší a/nebo novější než ty stávající.

- s. 052: Pořešit více rolí jednoho člověka na jedné knize.

- s. 052: Zefektivnit hledání opakovaných klíčů.

- s. 053: Explodovat při přípravě ty sloupce, kde explodování nezvýší počet řádků.

- s. 053: Dořešit ukládání málo vyplněných sloupců v datasetu autorit.

- s. 054: Při hledání nových českých knih odstranit duplikáty (nespoléhat se na informaci o vydání.)

- s. 050: Automatizovat stahování dat ČNB (aktualizují je vždy v pondělí, bohužel jen v kompletním balíku; zároveň mi ze záhadných důvodů nefungoval wget ani curl).

- s. 060+: Předělat sešity na skripty.

- s. 063: Ve finálním souboru s wikidaty nahradit Q-identifikátory českými/anglickými názvy.

- Scrapovat toho z knihkupectví víc:

    - ukázky e-booků
    - info o bestsellerech
    - čtenářské hodnocení
    - obálky

- Pokusit se získat informace o přesných datech vydání. Něco je na Goodreads, ne moc spolehlivé. Pro nové knihy: kdy se poprvé změnilo předpokládané datum vydání na vyšlo? Nebo kdy je zakatalogovala knihovna?

- Poziční válka s antiscrapovacími opatřeními Goodreads: další kolo je evidovat odmítnuté požadavky, zkusit je stáhnout ještě jednou.

- Scrapovat z Goodreads i cifru "added" (není v HTML, rvou to tam nějakým JS, bude nutné Selenium).

- Napojit další zdroje dat:

    - městské knihovny pro info o rozpůjčovanosti (zřejmě však příliš mnoho bandwidthu pro málo zajímavostí)
    - Knihobot / Trh knih pro info o dostupnosti (dtto)

## Klíč k nejdůležitějším polím v České národní bibliografii

Při zpracování dat se právě z tohoto seznamu berou čísla sloupců k zachování, s výjimkou těch označených hvězdičkou. Kurzívou jsou označeny [oficiální názvy kategorií](https://text.nkp.cz/o-knihovne/odborne-cinnosti/zpracovani-fondu/katalogizacni-politika/katalogizace-podle-rda-ve-formatu-marc-21-tistene-a-elektronicke-monografie-katalogizace-na-urovni-minimalniho-doporuceneho-zaznamu), zbytek jsou opisy.

### Česká národní bibliografie – cnb.xml

- leader - _návěští_
- 001 - _identifikační číslo_
- 007 - _pole pevné délky pro fyzický popis specifikace pro tištěný či rukopisný (okem čitelný) text_ (t jako první znak je text, s audio) *
- 008 - _údaje pevné délky: specifikace pro knihy_
- 020_a - _ISBN_
- 020_c - _dostupnost_ (čili cena)
- 020_q - _zpřesnění_ (vč. informací o vazbě)
- 022_a - ISSN *
- 028_b - vydavatelství audia *
- 041_ind1 - _indikátor překladu_ (0 = není/neobsahuje překlad, 1 = naopak)
- 041_a - _kód jazyka textu_
- 041_h	- _kód jazyka originálu_
- 041_k - _kód jazyka překladu zprostředkujícího původní text_ *
- 044_a - _kód země vydání_
- 072_a - _klasifikační znak jako součást skupiny Konspektu_  
- 072_x - _slovní označení skupiny Konspektu_
- 080_a - _klasifikační znak MDT_
- 080_x - pomocný znak MDT *
- 100_4	- role tvůrcovstva
- 100_7 - _číslo autority_
- 100_a - _osobní jméno_
- 100_c - _doplňky ke jménu jiné než data_ *
- 100_d	- _data související se jménem_
- 210_a - zkrácený název *
- 222_a - klíčový název *
- 240_l - _jazyk díla_
- 245_a	- _název_
- 245_b - _další údaje o názvu_ *
- 245_c - _údaj o odpovědnosti_
- 245_h - _obecné označení druhu dokumentu_ *
- 245_n - _číslo části/sekce díla_
- 245_p - _název části/sekce díla_
- 246_a - variantní název
- 250_a - _označení vydání_
- 250_b - nové údaje o vydání
- 260_ind1 - ovlivňuje význam následujících polí (2 = _intervening publisher_, 3 = _current/latest publisher_)
- 260_a - lokalita nakladatele
- 260_b - jméno nakladatele
- 260_c - datum vydání
- 260_e - místo výroby
- 260_f - jméno výrobce
- 260_g - rok výroby *
- 264_ind2 - ovlivňuje význam následujících polí (1 = nakladatel, 2 = distributor, 3 = výrobce, 4 = copyright)
- 264_a - _místo vydání_ / distributora / výrobce
- 264_b - _jméno nakladatele_ / distributora / výrobce
- 264_c - _datum vydání_ / výroby / copyrightu
- 300_a - _rozsah_
- 300_b - _další fyzické údaje_
- 300_c - _rozměr_
- 300_e - _doprovodný materiál_ *
- 310_a - současná periodicita *
- 310_b - data označující současnou periodicitu *
- 321_a - předcházející periodicita *
- 321_b - data označující předcházející periodicitu *
- 336_a - _typ obsahu_ *
- 337_a - _typ média_ *
- 338_a - _typ nosiče_ *
- 490_a - _údaje o edici_
- 490_v - _označení svazku/pořadí_
- 500_a	- _všeobecná poznámka_ (náklad, překlad atp.)
- 520_a - _resumé: text poznámky_ (slogan)
- 520_b - _resumé: rozšířený text poznámky_ (anotace)
- 521_a - _poznámka k uživatelskému určení_
- 546_a - _poznámka o jazyku_
- 546_b - _typ jazyka nebo písma_ *
- 550_a - _poznámka k vydavateli_ *
- 600_a - jméno člověka, který je subjektem publikace *
- 600_c - titul člověka, který je subjektem publikace *
- 600_7 - kód člověka, který je subjektem publikace *
- 648_a - _chronologický termín_
- 650_a - _věcné téma jako vstupní prvek_
- 650_x - podtémata
- 650_z - _geographic subdivision_
- 650_y - dobové zařazení
- 651_a - _geografické jméno_
- 653_a - _index term added entry that is not constructed by standard subject heading/thesaurus-building conventions_
- 655_a - _žánr/forma či základní termín_
- 700_4 - role tvůrcovstva
- 700_7 - _číslo autority_
- 700_a - _osobní jméno_
- 700_c - _doplňky ke jménu jiné než data_ *
- 700_d	- _data související se jménem_
- 710_a - _jméno korporace nebo jurisdikce jako vstupní prvek_
- 710_b - _podřízená složka_
- 710_4 - role korp.
- 710_7 - _číslo autority_
- 830_a - název edice
- 810_p - řada *
- 928_a - _národní pole_, nakladatel pro záznam
- 964_a - předmětové heslo

### Databáze národních autorit NK ČR – aut.xml

- leader - _návěští_
- 001 - _identifikační číslo_
- 024_a - _other standard identifier: standard number or code_ ("Q506600")
- 024_2 - _other standard identifier: source_ ("Wikidata")
- 046_f - _birth date_
- 046_g - _death date_
- 100_a - _personal name_
- 100_ind1 - _type of personal name entry element: 0 = forename, 1 = surname, 3 = family name_
- 100_d - _dates associated with a name_
- 100_7 - identifikační číslo
- 110_a - _corporate name or jurisdiction name as entry element_
- 370_a - _place of birth_
- 370_b - _place of death_
- 370_c - _associated country_
- 370_f - _other associated place_
- 370_s - _start period_ *
- 370_t - _end period_ *
- 372_a - _field of activity_
- 373_a - _associated group_
- 374_a - _occupation_
- 375_a - _gender_
- 377_a - _associated language code_
- 400_ind1 - _type of personal name element_
- 400_a - _personal name_
- 400_d - _dates associated with a name_
- 400_i - _relationship information_
- 400_q - _fuller form of name_ *
- 410_a - _corporate name or jurisdiction name as entry element_
- 411_a - _meeting name or jurisdiction name as entry element_
- 430_a - _uniform title_
- 450_a - _topical term or geographic name entry element_
- 500_ind1 - _type of personal name entry element_
- 500_a - _personal name_
- 500_i - _relationship information_
- 550_a - _topical term or geographic name entry element_ *
- 550_7 - _data provenance_
- 678_a - _biographical or historical data_
- 856_u - zde bývá odkaz na Wikipedii (nejenom)

Viz také [zkratky profesí](https://www.loc.gov/marc/relators/relaterm.html).