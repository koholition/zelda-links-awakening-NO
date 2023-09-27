PUSHC
NEWCHARMAP CreditsCharmap

SETCHARMAP AsciiCharmap

; Credits-specific charmap patches for Norwegian
charmap "[", $56 ; Æ
charmap "]", $57 ; Ø
charmap "-" $4E
charmap ".", $4D

POPC
