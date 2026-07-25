"""
budget.py — Modulo 3: Definizione del Budget Mensile.

Specifica (dal documento):
  Obiettivo: Impostare un limite di spesa per una categoria in un determinato mese.

  Input:
    - Mese (formato YYYY-MM, es. 2025-01)
    - Nome della categoria
    - Importo del budget (decimale positivo)

  Elaborazione:
    1. Verifica che il budget sia > 0
    2. Controllo dell'esistenza della categoria (SQL SELECT)
    3. Inserimento OPPURE aggiornamento del record di budget
       (se esiste già un budget per quella coppia mese/categoria, lo aggiorna)

  Output:
    - "Budget mensile salvato correttamente."  → successo
    - Messaggi di errore per input invalido o categoria inesistente
"""

import re                                     # Per validare il formato YYYY-MM
from database import get_connection           # Connessione centralizzata al database
from categorie import cerca_categoria_per_nome  # Utility per cercare una categoria


def definisci_budget() -> None:
    """
    Punto di ingresso del Modulo 3: Definizione del Budget Mensile.

    Guida l'utente attraverso l'inserimento dei dati necessari,
    esegue le validazioni e salva (INSERT o UPDATE) il budget nel database.

    La specifica richiede che se esiste già un budget per la stessa
    coppia (mese, categoria), esso venga aggiornato (non duplicato).
    """
    print("\n--- Definisci Budget Mensile ---")

    # -----------------------------------------------------------------------
    # Step 1: Acquisizione del mese
    # -----------------------------------------------------------------------
    mese = _leggi_mese()
    if mese is None:
        return  # Formato non valido, errore già stampato

    # -----------------------------------------------------------------------
    # Step 2: Acquisizione del nome della categoria
    # -----------------------------------------------------------------------
    nome_categoria = input("Categoria: ").strip()

    if not nome_categoria:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    # -----------------------------------------------------------------------
    # Step 3: Acquisizione e validazione dell'importo del budget
    # Specifica: budget deve essere > 0
    # -----------------------------------------------------------------------
    importo = _leggi_importo_budget()
    if importo is None:
        return  # Errore già stampato

    # -----------------------------------------------------------------------
    # Step 4: Verifica dell'esistenza della categoria (SQL SELECT)
    # -----------------------------------------------------------------------
    categoria_id = cerca_categoria_per_nome(nome_categoria)

    if categoria_id is None:
        print("Errore: la categoria non esiste. Aggiungila prima nel Modulo 1.")
        return

    # -----------------------------------------------------------------------
    # Step 5: INSERT o UPDATE del budget
    #
    # Utilizziamo INSERT OR REPLACE (equivalente a UPSERT in SQLite):
    # - Se non esiste un budget per (mese, categoria_id) → lo INSERISCE
    # - Se esiste già → lo SOSTITUISCE con il nuovo importo
    #
    # Questo comportamento è reso possibile dal vincolo UNIQUE(mese, categoria_id)
    # definito nella tabella budget_mensile (vedi database.py)
    # -----------------------------------------------------------------------
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL INSERT OR REPLACE — inserisce o sovrascrive il budget
        cursore.execute(
            """
            INSERT INTO budget_mensile (mese, categoria_id, importo)
            VALUES (?, ?, ?)
            ON CONFLICT(mese, categoria_id)
            DO UPDATE SET importo = excluded.importo;
            """,
            (mese, categoria_id, importo)
        )
        conn.commit()

        # Messaggio di successo (dalla specifica)
        print("Budget mensile salvato correttamente.")

    except Exception as e:
        print(f"Errore durante il salvataggio del budget: {e}")

    finally:
        conn.close()


def visualizza_budget_attivi() -> None:
    """
    Visualizza tutti i budget mensili attualmente definiti.

    Funzione di utilità accessibile anche dal modulo report.
    """
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL SELECT con JOIN per mostrare il nome della categoria
        cursore.execute(
            """
            SELECT
                bm.mese,
                c.nome   AS categoria,
                bm.importo
            FROM budget_mensile bm
            INNER JOIN categorie c ON bm.categoria_id = c.id
            ORDER BY bm.mese DESC, c.nome;
            """
        )
        righe = cursore.fetchall()

        if not righe:
            print("\nNessun budget mensile definito.")
            return

        print("\n{:<10} {:<20} {:>12}".format("Mese", "Categoria", "Budget (€)"))
        print("-" * 45)

        for riga in righe:
            print("{:<10} {:<20} {:>12.2f}".format(
                riga["mese"],
                riga["categoria"],
                riga["importo"]
            ))

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Funzioni private di acquisizione e validazione dell'input
# ---------------------------------------------------------------------------

def _leggi_mese() -> str | None:
    """
    Legge un mese da console nel formato YYYY-MM e ne verifica la validità.

    Returns:
        str: il mese in formato YYYY-MM se valido
        None: se il formato non è corretto
    """
    mese = input("Mese (YYYY-MM, es. 2025-01): ").strip()

    # Espressione regolare: 4 cifre, trattino, 2 cifre (01-12)
    pattern = r"^\d{4}-(0[1-9]|1[0-2])$"
    if not re.match(pattern, mese):
        print("Errore: formato mese non valido. Usare YYYY-MM (es. 2025-01).")
        return None

    return mese


def _leggi_importo_budget() -> float | None:
    """
    Legge l'importo del budget da console e verifica che sia positivo.

    Specifica: il budget deve essere > 0.

    Returns:
        float: l'importo se valido e positivo
        None: se l'input non è numerico o è <= 0
    """
    testo = input("Importo budget (es. 300.00): ").strip()

    try:
        importo = float(testo)
    except ValueError:
        print("Errore: l'importo deve essere un numero (es. 300.00).")
        return None

    # Validazione: il budget deve essere strettamente positivo (dalla specifica)
    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return None

    return importo
