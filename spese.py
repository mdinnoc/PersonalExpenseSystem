"""
spese.py — Modulo 2: Inserimento di una Spesa.

Specifica (dal documento):
  Input:
    - Data (formato YYYY-MM-DD)
    - Importo (numero decimale positivo)
    - Nome della categoria (deve esistere nel database)
    - Descrizione (opzionale)

  Elaborazione:
    1. Acquisizione di tutti gli input da console
    2. Validazione dell'importo: if (importo <= 0) → errore
    3. Verifica dell'esistenza della categoria (SQL SELECT)
    4. Inserimento della spesa (SQL INSERT con chiave esterna)

  Output:
    - "Spesa inserita correttamente."              → successo
    - "Errore: l'importo deve essere maggiore di zero."
    - "Errore: la categoria non esiste."
"""

import re                              # Per validare il formato della data con regex
from database import get_connection    # Connessione centralizzata al database
from categorie import cerca_categoria_per_nome  # Utility per cercare una categoria


def inserisci_spesa() -> None:
    """
    Punto di ingresso del Modulo 2: Inserimento di una Spesa.

    Guida l'utente attraverso l'acquisizione di tutti i campi necessari,
    esegue le validazioni richieste dalla specifica e infine esegue
    il SQL INSERT per registrare la spesa nel database.
    """
    print("\n--- Inserisci una Nuova Spesa ---")

    # -----------------------------------------------------------------------
    # Step 1: Acquisizione della data
    # -----------------------------------------------------------------------
    data = _leggi_data()
    if data is None:
        # L'utente ha inserito un formato non valido → abbandona il modulo
        return

    # -----------------------------------------------------------------------
    # Step 2: Acquisizione e validazione dell'importo
    # Specifica: if (importo <= 0) → errore
    # -----------------------------------------------------------------------
    importo = _leggi_importo()
    if importo is None:
        return  # Errore già stampato nella funzione _leggi_importo

    # -----------------------------------------------------------------------
    # Step 3: Acquisizione del nome della categoria
    # -----------------------------------------------------------------------
    nome_categoria = input("Categoria: ").strip()

    if not nome_categoria:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    # -----------------------------------------------------------------------
    # Step 4: Acquisizione della descrizione (campo opzionale)
    # -----------------------------------------------------------------------
    descrizione = input("Descrizione (opzionale, premi INVIO per saltare): ").strip()
    # Se l'utente preme INVIO senza scrivere nulla, descrizione rimane stringa vuota
    # → la salviamo come None nel database (NULL SQL)
    if not descrizione:
        descrizione = None

    # -----------------------------------------------------------------------
    # Step 5: Verifica dell'esistenza della categoria (SQL SELECT)
    # -----------------------------------------------------------------------
    categoria_id = cerca_categoria_per_nome(nome_categoria)

    if categoria_id is None:
        # Categoria non trovata → messaggio di errore dalla specifica
        print("Errore: la categoria non esiste.")
        return

    # -----------------------------------------------------------------------
    # Step 6: Inserimento della spesa (SQL INSERT con chiave esterna)
    # -----------------------------------------------------------------------
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL INSERT — registra la nuova spesa
        # categoria_id è la FOREIGN KEY verso la tabella categorie
        cursore.execute(
            """
            INSERT INTO spese (data, importo, categoria_id, descrizione)
            VALUES (?, ?, ?, ?);
            """,
            (data, importo, categoria_id, descrizione)
        )
        conn.commit()

        # Messaggio di successo (dalla specifica)
        print("Spesa inserita correttamente.")

    except Exception as e:
        # Cattura errori imprevisti del database e li mostra all'utente
        print(f"Errore durante il salvataggio: {e}")

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Funzioni private di acquisizione e validazione dell'input
# ---------------------------------------------------------------------------

def _leggi_data() -> str | None:
    """
    Legge una data da console e verifica il formato YYYY-MM-DD.

    Returns:
        str: la data in formato YYYY-MM-DD se valida
        None: se il formato non è corretto
    """
    data = input("Data (YYYY-MM-DD): ").strip()

    # Espressione regolare per verificare il formato della data
    # Pattern: 4 cifre - 2 cifre - 2 cifre (es. 2025-01-15)
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, data):
        print("Errore: formato data non valido. Usare YYYY-MM-DD (es. 2025-01-15).")
        return None

    return data


def _leggi_importo() -> float | None:
    """
    Legge l'importo da console e verifica che sia un numero positivo.

    Specifica: if (importo <= 0) → "Errore: l'importo deve essere maggiore di zero."

    Returns:
        float: l'importo se valido e positivo
        None: se l'input non è un numero o è <= 0
    """
    testo = input("Importo (es. 25.50): ").strip()

    # Tentativo di conversione in float
    try:
        importo = float(testo)
    except ValueError:
        # Input non numerico
        print("Errore: l'importo deve essere un numero (es. 25.50).")
        return None

    # Validazione: l'importo deve essere > 0 (dalla specifica)
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return None

    return importo


def visualizza_spese_recenti() -> None:
    """
    Visualizza le ultime 10 spese inserite, ordinate per data decrescente.

    Funzione di utilità accessibile dal modulo report (Report 3).
    """
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL SELECT con JOIN per ottenere il nome della categoria
        # ORDER BY data DESC → le più recenti prima
        cursore.execute(
            """
            SELECT
                s.data,
                c.nome     AS categoria,
                s.importo,
                s.descrizione
            FROM spese s
            INNER JOIN categorie c ON s.categoria_id = c.id
            ORDER BY s.data DESC
            LIMIT 10;
            """
        )
        righe = cursore.fetchall()

        if not righe:
            print("\nNessuna spesa registrata.")
            return

        # Intestazione tabella (stile specifica)
        print("\n{:<12} {:<15} {:>10} {:<30}".format(
            "Data", "Categoria", "Importo", "Descrizione"
        ))
        print("-" * 70)

        for riga in righe:
            # Se la descrizione è NULL, stampiamo una stringa vuota
            descrizione = riga["descrizione"] if riga["descrizione"] else ""
            print("{:<12} {:<15} {:>10.2f} {:<30}".format(
                riga["data"],
                riga["categoria"],
                riga["importo"],
                descrizione
            ))

    finally:
        conn.close()
