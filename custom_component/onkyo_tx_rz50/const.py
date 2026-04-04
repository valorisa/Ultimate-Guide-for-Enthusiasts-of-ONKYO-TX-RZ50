"""Constantes pour le composant ONKYO TX-RZ50."""

DOMAIN = "onkyo_tx_rz50"
MANUFACTURER = "Onkyo"
MODEL = "TX-RZ50"

SOURCES = {
    "00": "BD/DVD",
    "01": "GAME",
    "02": "CBL/SAT",
    "03": "STRM BOX",
    "04": "PC",
    "05": "AUX",
    "06": "CD",
    "07": "TV",
    "08": "PHONO",
    "26": "TUNER",
    "27": "NET",
    "28": "USB",
    "29": "BLUETOOTH",
}

REVERSE_SOURCES = {v: k for k, v in SOURCES.items()}
