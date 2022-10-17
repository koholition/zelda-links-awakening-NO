# Legenden om Zelda: Links Oppvåkning

La oss oversette Link's Awakening til norsk!

Det finnes allerede en svensk versjon som vi kan la oss inspirere av: [Legenden om Zelda: Links Uppvaknande](https://www.romhacking.net/translations/1245/)

## Opplegg

Dette repoet er basert på [denne disassemblyen](https://github.com/zladx/LADX-Disassembly), men holdes ikke automatisk i sync. @tobiasvl kan synce manuelt ved behov.

## Diskuter

- Lag en [issue](https://github.com/tobiasvl/zelda-links-awakening-NO/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) om dere kommer på noe som må fikses eller som vi må huske på.
- Større prosjekter kan vi eventuelt putte i [projects](https://github.com/gbdev/rgbds/projects).
- Trenger vi å diskutere noe (utenom skjelett-chatten) kan vi bruke [discussions](https://github.com/tobiasvl/zelda-links-awakening-NO/projects?query=is%3Aopen)-forumet??

## Bidra med oversettelser

- Tekst som skal oversettes: https://github.com/tobiasvl/zelda-links-awakening-NO/tree/main/src/text
- Vi må også fikse font: https://github.com/tobiasvl/zelda-links-awakening-NO/tree/main/src/gfx/fonts
- Noe grafikk, som tittelskjermen, kan vi ta ved behov

## Teste spillet

For å bygge selve ROM-en:

### Installer RGBDS og avhengigheter

RGBDS er Game Boy-assembleren vi bruker for å bygge ROM av dette repoet, så den må installeres. For eksempel, på Ubuntu (inkludert WSL på Windows):

```bash
cd /tmp
sudo apt-get install bison flex libpng-dev python3               # Installer avhengigheter
wget https://github.com/gbdev/rgbds/archive/refs/tags/v0.5.2.zip # Last ned RGBDS
unzip v0.5.2 && cd rgbds-0.5.2                                   # Pakk ut RGBDS
make && sudo make install                                        # Installer RGBDS
```

### Bygg ROM

Akkurat nå har jeg bare hacket til så den engelske versjonen brukes som den norske. Så dette bør holde (på Linux):

```
make
```

Da bygges både ROM og debug-symboler som kan brukes i [BGB](https://github.com/zladx/LADX-Disassembly/wiki/Tooling-for-reverse-engineering#bgb).

### Debug

Hvis man bygger ROM-en, vil første lagringsfil alltid være en DEBUG-fil der alt er låst opp, med følgende funksjonalitet:

#### Tekst-debugger

Hvis du går til Marin foran hanestatuen i landsbyen, kan du teste all dialogen i spillet.

- Bruk D-paden for å velge et tall XX (venstre/høyre velger enere, opp/ned tiere)
- Trykk A for å vise tekst nr. XX
- Trykk B for å vise tekst nr. 1XX
- Trykk SELECT for å vise tekst nr. 2XX

#### Noclip

Du kan skru på «noclip»-modus på en av to måter:

- Hold inne D-paden og trykk SELECT for å fryse spillet, og trykk så SELECT igjen for å skru på noclip
- Trykk START (pauseskjerm) og så SELECT

#### Warp

Trykk B + SELECT på kartet for å warpe direkte hvor du vil. Du kan ende opp inni en vegg, skru i så fall på noclip.

#### Vinn spillet

Trykk START på kartet for å warpe direkte til Vindfisken og sluttscenen.

## Ressurser

I tilfelle vi trenger å analysere ROM-en:

- [disassembling How-Tos](https://github.com/zladx/LADX-Disassembly/wiki)
- [Artemis251's Link's Awakening Cache](http://artemis251.fobby.net/zelda/index.php): ROM map, maps data format
- [Xkeeper's Link's Awakening depot](https://xkeeper.net/hacking/linksawakening/): maps tilesets and save format infos
- [LALE](https://github.com/anotak/LALE): level editor, notes on maps data format
- [The Legend of Zelda Link's Awakening /DX Speedrunning Wiki](http://spiraster.x10host.com/LADXWiki/index.php/) : infos on wrong warps and map data format
- [Zelda III Disassembly](http://www.zeldix.net/t143-disassembly-zelda-docs) ([archive](https://web.archive.org/web/20180315181518/http://www.zeldix.net/t143-disassembly-zelda-docs)): good source on Zelda SNES source code, which has many similarities to LADX
- [Disassembling Link's Awakening](https://kemenaran.winosx.com/posts/category-disassembling-links-awakening/): a series of blog posts and progress reports
- Discord: [LADX](https://discord.gg/sSHrwdB)
