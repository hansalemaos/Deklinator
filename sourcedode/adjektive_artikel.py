import bs4
import spacy
from add_color_print_reg import *
from menudownload import *
satzanalyse_werkzeug = spacy.load("de_dep_news_trf")
import regex
from satzmetzger.satzmetzger import Satzmetzger
from fuzzywuzzy import fuzz
from maximize_console import *
add_color_print_to_regedit()
cfg = {}
maximize_console(lines=30000)


colorfunctionslogo = [drucker.f.black.red.normal, drucker.f.black.brightyellow.normal]
drucker.p_ascii_front_on_flag_with_border(
    text="Deklinator",
    colorfunctions=colorfunctionslogo,
    bordercolorfunction=drucker.f.brightgreen.black.italic,
    font="slant",
    width=1000,
    offset_from_left_side=5,
    offset_from_text=15,
)
colorfunctionspage = [
    drucker.f.black.brightwhite.normal,
    drucker.f.black.brightgreen.normal,
]
drucker.p_ascii_front_on_flag_with_border(
    text="www . queroestudaralemao . com . br",
    colorfunctions=colorfunctionspage,
    bordercolorfunction=drucker.f.brightgreen.black.negative,
    font="slant",
    width=1000,
    offset_from_left_side=1,
    offset_from_text=1,
)

def txtdateien_lesen(text):
    try:
        dateiohnehtml = (
            b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = bs4.BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)


kurzbeschreibung_aufgabe = drucker.f.black.brightyellow.italic(
    "\nDekliniere alle Wörter!\n"
)
return_choice = drucker.f.black.brightcyan.italic(
    " <-- Gib diese Nummer ein, sobald du alle Wörter dekliniert hast!\n"
)
prompt = drucker.f.black.magenta.bold(
    """Einige Wörter sind nicht gebeugt!\nGib die Nummer, die vor dem Wort steht, ein, um das Wort zu deklinieren!\n"""
)

satzmetzgerle = Satzmetzger()
p = subprocess.run(r"Everything2TXT.exe", capture_output=True)
ganzertext = txtdateien_lesen(p.stdout)
einzelnesaetze = satzmetzgerle.zerhack_den_text(ganzertext)
allesaetzefertigfueraufgabe = []
allemoeglichenpunkte = 0
punktevomuser = 0
artikel = [
    "der",
    "die",
    "das",
    "den",
    "dem",
    "des",
    "ein",
    "eine",
    "einem",
    "einer",
    "eines",
]
for satzindex, einzelnersatz in enumerate(einzelnesaetze):
    analysierter_text = satzanalyse_werkzeug(einzelnersatz)
    dokument_als_json = analysierter_text.doc.to_json()
    alleverbenimsatz = []
    schongedruckt = False
    satzdruckeneditiert = ""
    loesungshilfeganz = ""
    for token in dokument_als_json["tokens"]:
        anfangwort = token["start"]
        endewort = token["end"]
        aktuelleswort = dokument_als_json["text"][anfangwort:endewort]
        leerzeichenplatz = len(dokument_als_json["text"][anfangwort:endewort]) * "_"
        platzhalter = (
            dokument_als_json["text"][:anfangwort]
            + leerzeichenplatz
            + dokument_als_json["text"][endewort:]
        )
        satzschongemacht = dokument_als_json["text"][:anfangwort]
        satzdrucken = ""

        if "Case=" in token["morph"] and (
            ("DET" in token["pos"] and aktuelleswort in artikel)
            or "ADJ" in token["pos"]
        ):
            loesungshilfe = (
                aktuelleswort
                + ": \n-----------------\n"
                + "\n".join(regex.split(r"\|", token["morph"]))
                + "\n\n\n\n\n"
            )
            loesungshilfeganz = loesungshilfeganz + loesungshilfe
            if "DET" in token["pos"]:
                satzdrucken = (
                    drucker.f.black.white.italic("Wir sind hier:   ")
                    + drucker.f.white.black.normal(satzschongemacht)
                    + drucker.f.brightyellow.black.italic(aktuelleswort[:1] + "___")
                )
                satzdruckeneditiert = (
                    satzdruckeneditiert + " " + aktuelleswort[:1] + "___"
                )
            if "ADJ" in token["pos"]:
                wortdrucken = regex.sub("[ersnm]{,2}$", "__", aktuelleswort)
                satzdrucken = (
                    drucker.f.black.white.italic("Wir sind hier:   ")
                    + drucker.f.white.black.normal(satzschongemacht)
                    + drucker.f.brightyellow.black.italic(wortdrucken)
                )
                satzdruckeneditiert = satzdruckeneditiert + " " + wortdrucken

            allemoeglichenpunkte = allemoeglichenpunkte + 1

            richtigeantwort = regex.findall("Case=([^\|]+)", token["morph"])[0]
            if richtigeantwort == "Nom":
                richtigeantwort = "Nominativ"
            if richtigeantwort == "Acc":
                richtigeantwort = "Akkusativ"
            if richtigeantwort == "Dat":
                richtigeantwort = "Dativ"
            if richtigeantwort == "Gen":
                richtigeantwort = "Genitiv"

            continue
        else:
            satzdruckeneditiert = satzdruckeneditiert + f" {aktuelleswort}"
    ganzersatz = dokument_als_json["text"]
    satz1ohneleer = regex.sub(r"\s+", "", ganzersatz)
    satz2ohneleer = regex.sub(r"\s+", "", satzdruckeneditiert)
    gleichsaetze = fuzz.ratio(satz1ohneleer, satz2ohneleer)
    if gleichsaetze < 99:
        ganzersatz_split = regex.split(r"\s+", satzdruckeneditiert)
        ganzersatz_split = [x for x in ganzersatz_split if any(x)]
        # print(ganzersatz_split)
        cfg = {str(key + 1): x for key, x in enumerate(ganzersatz_split)}
        erreichbarepunktzahl = 100 - gleichsaetze
        allemoeglichenpunkte = allemoeglichenpunkte + erreichbarepunktzahl
        cfg = m.config_menu(
            kurzbeschreibung_aufgabe,
            cfg.copy(),
            return_choice=return_choice,
            prompt=prompt + kurzbeschreibung_aufgabe,
        )
        falschersatz = regex.sub(r"\s+", "", "".join([x[1] for x in cfg.items()]))
        aktuelleuebereinstimmungneu = fuzz.ratio(satz1ohneleer, falschersatz)

        if aktuelleuebereinstimmungneu == 100:
            print(
                drucker.f.brightwhite.brightgreen.italic(
                    "     Jetzt ist der Satz 100% richtig! Gut gemacht!: "
                )
                + drucker.f.brightgreen.black.negative(
                    f" {aktuelleuebereinstimmungneu} Prozent     "
                )
            )
            punktedieserdurchgang = 100 - aktuelleuebereinstimmungneu
            punktedieserdurchgang = abs(punktedieserdurchgang - erreichbarepunktzahl)
            punktevomuser = punktevomuser + punktedieserdurchgang

        if (
            aktuelleuebereinstimmungneu >= gleichsaetze
            and aktuelleuebereinstimmungneu < 100
        ):
            print(
                drucker.f.brightwhite.brightgreen.italic(
                    "     Der Satz ist besser als vorher, aber es gibt noch Fehler!: Die jetzige Übereinstimmung liegt bei: "
                )
                + drucker.f.brightgreen.black.negative(
                    f" {aktuelleuebereinstimmungneu} Prozent     "
                )
            )
            punktedieserdurchgang = 100 - aktuelleuebereinstimmungneu
            punktedieserdurchgang = abs(punktedieserdurchgang - erreichbarepunktzahl)
            punktevomuser = punktevomuser + punktedieserdurchgang

        elif aktuelleuebereinstimmungneu < gleichsaetze:
            print(
                drucker.f.brightwhite.red.italic(
                    "     Das war leider nicht so gut! Der Satz ist schlechter als vor der Korrektur! Die jetzige Übereinstimmung liegt bei: "
                )
                + drucker.f.brightred.black.negative(
                    f" {aktuelleuebereinstimmungneu} Prozent     "
                )
            )
            punktedieserdurchgang = 100 - aktuelleuebereinstimmungneu
            punktedieserdurchgang = -1 * abs(
                punktedieserdurchgang - erreichbarepunktzahl
            )
            punktevomuser = punktevomuser + punktedieserdurchgang

    if gleichsaetze < 100:
        satzvomuser = " ".join([x[1] for x in cfg.items()])
        print(
            drucker.f.brightgreen.black.negative(f"Original: ")
            + drucker.f.brightgreen.black.italic(ganzersatz)
            + "\n"
            + drucker.f.brightgreen.black.negative(f"Deine Version: ")
            + drucker.f.brightgreen.black.italic(satzvomuser)
        )
        print(loesungshilfeganz)

    print(
        drucker.f.magenta.black.italic(
            f"Deine Punktzahl: {punktevomuser}\nMaximale Punktzahl: {allemoeglichenpunkte}\n"
        )
    )
    print("\n" * 10)


