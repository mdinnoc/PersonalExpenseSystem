"""
categorie.py — Modulo 1: Gestione delle Categorie di Spesa.

Specifica (dal documento):
  Input  : nome della categoria (stringa da console)
  Elaborazione:
    1. Lettura del nome
    2. Verifica che il nome non sia vuoto
    3. Controllo dell'esistenza della categoria (SQL SELECT)
    4. Inserimento della categoria se valida (SQL INSERT)
  Output :
    - "Categoria inserita correttamente."   → successo
    - "La categoria esiste già."            → duplicato
    - Messaggi di errore per input invalido
"""

from database import get_connection  # Connessione al database centralizzata


def gestisci_categorie() -> None:
    """
    Punto di ingresso del Modulo 1: Gestione Categorie.

    Mostra un sottomenu che consente all'utente di:
      1. Aggiungere una nuova categoria
      2. Visualizzare tutte le categorie esistenti
      3. Tornare al menu principale

    Il ciclo while mantiene il sottomenu attivo fino a che
    l'utente sceglie di tornare al menu principale.
    """
    while True:
        # ------------------------------------------------------------------
        # Sottomenu categorie
        # ------------------------------------------------------------------
        print("\n--- Gestione Categorie ---")
        print("1. Aggiungi una nuova categoria")
        print("2. Visualizza tutte le categorie")
        print("3. Torna al menu principale")
        print("-" * 30)

        scelta = input("Inserisci la tua scelta: ").strip()

        # Selezione tramite if/elif (equivalente dello switch richiesto dalla specifica)
        if scelta == "1":
            _aggiungi_categoria()
        elif scelta == "2":
            _visualizza_categorie()
        elif scelta == "3":
            # Ritorno al menu principale
            break
        else:
            print("Scelta non valida. Riprovare.")


# ---------------------------------------------------------------------------
# Funzioni private del modulo
# ---------------------------------------------------------------------------

def _aggiungi_categoria() -> None:
    """
    Aggiunge una nuova categoria di spesa al database.

    Flusso di elaborazione (dalla specifica):
      1. Acquisizione del nome da console
      2. Validazione: il nome non deve essere vuoto
      3. SQL SELECT → verifica se la categoria esiste già
      4. SQL INSERT → inserimento se la categoria è nuova
    """
    # --- Step 1: Acquisizione input ---
    nome = input("Nome della nuova categoria: ").strip()

    # --- Step 2: Validazione — il nome non può essere vuoto ---
    if not nome:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    # --- Step 3 & 4: Query SQL ---
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL SELECT — controlla se esiste già una categoria con lo stesso nome
        # UPPER() rende il confronto case-insensitive (es. "alimentari" == "Alimentari")
        cursore.execute(
            "SELECT id FROM categorie WHERE UPPER(nome) = UPPER(?);",
            (nome,)
        )
        esistente = cursore.fetchone()  # None se non trovato, altrimenti la riga

        if esistente:
            # La categoria esiste già → messaggio di errore (dalla specifica)
            print("La categoria esiste già.")
        else:
            # SQL INSERT — inserisce la nuova categoria
            cursore.execute(
                "INSERT INTO categorie (nome) VALUES (?);",
                (nome,)
            )
            conn.commit()
            # Messaggio di successo (dalla specifica)
            print("Categoria inserita correttamente.")

    finally:
        # La connessione viene chiusa in ogni caso (anche in presenza di errori)
        conn.close()


def _visualizza_categorie() -> None:
    """
    Visualizza l'elenco di tutte le categorie presenti nel database.

    SQL SELECT con ORDER BY per ordinamento alfabetico.
    """
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # Recupera tutte le categorie ordinate alfabeticamente per nome
        cursore.execute("SELECT id, nome FROM categorie ORDER BY nome;")
        righe = cursore.fetchall()

        if not righe:
            print("\nNessuna categoria definita. Aggiungine una prima.")
            return

        # Intestazione tabella
        print("\n{:<5} {:<30}".format("ID", "Categoria"))
        print("-" * 37)

        # Stampa ogni riga del risultato
        for riga in righe:
            print("{:<5} {:<30}".format(riga["id"], riga["nome"]))

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Funzione di utilità esportata (usata dagli altri moduli)
# ---------------------------------------------------------------------------

def cerca_categoria_per_nome(nome: str) -> int | None:
    """
    Cerca una categoria per nome (case-insensitive) e restituisce il suo ID.

    Questa funzione è utilizzata dagli altri moduli (spese, budget)
    per verificare l'esistenza di una categoria prima di inserire dati.

    Args:
        nome: nome della categoria da cercare

    Returns:
        int: l'ID della categoria se trovata
        None: se la categoria non esiste
    """
    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL SELECT — ricerca per nome, case-insensitive
        cursore.execute(
            "SELECT id FROM categorie WHERE UPPER(nome) = UPPER(?);",
            (nome,)
        )
        riga = cursore.fetchone()

        # Restituisce l'ID se trovato, None altrimenti
        return riga["id"] if riga else None

    finally:
        conn.close()
