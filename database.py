"""
database.py — Modulo di configurazione e connessione al database SQLite.

Responsabilità:
  - Aprire (o creare) il file del database 'spese.db'
  - Creare le tabelle se non esistono già
  - Garantire i vincoli di integrità (PRIMARY KEY, FOREIGN KEY,
    CHECK, UNIQUE, NOT NULL) come richiesto dalla specifica

Uso:
  from database import get_connection
  conn = get_connection()
"""

import sqlite3  # Libreria standard Python per SQLite (database SQL relazionale)
import os       # Per costruire il percorso del file del database


# ---------------------------------------------------------------------------
# Percorso del file di database: viene creato nella stessa cartella di questo
# script, così il programma è auto-contenuto (nessun server esterno necessario)
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "spese.db")


def get_connection() -> sqlite3.Connection:
    """
    Apre una connessione al database SQLite e restituisce l'oggetto Connection.

    Chiamata ogni volta che un modulo ha bisogno di accedere al database.
    La funzione:
      1. Apre/crea il file 'spese.db'
      2. Abilita il supporto alle FOREIGN KEY (disabilitato di default in SQLite)
      3. Inizializza le tabelle se è il primo avvio

    Returns:
        sqlite3.Connection: oggetto connessione pronto all'uso
    """
    # Apre (o crea) il file del database
    conn = sqlite3.connect(DB_PATH)

    # IMPORTANTE: SQLite non applica le FOREIGN KEY per default.
    # Questo pragma le attiva per la connessione corrente.
    conn.execute("PRAGMA foreign_keys = ON;")

    # Imposta la modalità di recupero righe come dizionario
    # (permette di accedere alle colonne per nome: riga["nome"] invece di riga[0])
    conn.row_factory = sqlite3.Row

    # Crea le tabelle al primo avvio (se non esistono)
    _inizializza_tabelle(conn)

    return conn


def _inizializza_tabelle(conn: sqlite3.Connection) -> None:
    """
    Crea le tabelle del database se non esistono ancora.

    Schema logico:
      categorie  (1) ──< (N)  spese
      categorie  (1) ──< (N)  budget_mensile

    Vincoli implementati (obbligatori da specifica):
      - PRIMARY KEY   su ogni tabella
      - FOREIGN KEY   in spese e budget_mensile → categorie
      - NOT NULL      su tutti i campi obbligatori
      - UNIQUE        su categorie.nome e su (budget_mensile.mese, categoria_id)
      - CHECK         su importo > 0 in spese e in budget_mensile

    Args:
        conn: connessione SQLite attiva
    """
    cursore = conn.cursor()

    # ------------------------------------------------------------------
    # TABELLA: categorie
    # Memorizza le categorie di spesa definite dall'utente (es. Alimentari)
    # ------------------------------------------------------------------
    cursore.execute("""
        CREATE TABLE IF NOT EXISTS categorie (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,  -- chiave primaria auto-incrementale
            nome  TEXT    NOT NULL UNIQUE              -- nome obbligatorio e univoco
        );
    """)

    # ------------------------------------------------------------------
    # TABELLA: spese
    # Ogni riga rappresenta una singola transazione di spesa
    # ------------------------------------------------------------------
    cursore.execute("""
        CREATE TABLE IF NOT EXISTS spese (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            data         TEXT    NOT NULL,                   -- formato YYYY-MM-DD
            importo      REAL    NOT NULL                    -- valore monetario
                         CHECK (importo > 0),               -- CHECK: importo positivo
            categoria_id INTEGER NOT NULL                   -- riferimento alla categoria
                         REFERENCES categorie(id)           -- FOREIGN KEY verso categorie
                             ON DELETE RESTRICT,            -- impedisce cancellazione categoria usata
            descrizione  TEXT                               -- campo opzionale (può essere NULL)
        );
    """)

    # ------------------------------------------------------------------
    # TABELLA: budget_mensile
    # Definisce il limite di spesa per categoria/mese
    # UNIQUE(mese, categoria_id) → un solo budget per coppia mese-categoria
    # ------------------------------------------------------------------
    cursore.execute("""
        CREATE TABLE IF NOT EXISTS budget_mensile (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            mese         TEXT    NOT NULL,                  -- formato YYYY-MM
            categoria_id INTEGER NOT NULL                   -- riferimento alla categoria
                         REFERENCES categorie(id)
                             ON DELETE RESTRICT,
            importo      REAL    NOT NULL                   -- limite di spesa mensile
                         CHECK (importo > 0),              -- CHECK: budget positivo
            UNIQUE (mese, categoria_id)                    -- UNIQUE: un budget per coppia
        );
    """)

    # Salva le modifiche al database
    conn.commit()
