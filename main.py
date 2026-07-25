"""
main.py — Punto di ingresso principale del Sistema di Gestione delle Spese Personali.

Struttura del programma (dalla specifica):
  1. Visualizzazione del messaggio di benvenuto
  2. Mostra il Menu Principale
  3. Attende la scelta dell'utente
  4. Esegue il modulo corrispondente tramite switch (if/elif)
  5. Ripete il ciclo fino alla scelta "Esci"

Menu Principale (dalla specifica):
  -------------------------
   SISTEMA SPESE PERSONALI
  -------------------------
  1. Gestione Categorie
  2. Inserisci Spesa
  3. Definisci Budget Mensile
  4. Visualizza Report
  5. Esci
  -------------------------

Dipendenze:
  - categorie.py  → Modulo 1
  - spese.py      → Modulo 2
  - budget.py     → Modulo 3
  - report.py     → Modulo 4
  - database.py   → configurazione database SQLite

Requisiti:
  - Python 3.10+
  - Librerie standard: sqlite3, re, os (nessuna installazione aggiuntiva)
"""

# Importazione dei quattro moduli funzionali del sistema
from categorie import gestisci_categorie   # Modulo 1: gestione categorie
from spese    import inserisci_spesa       # Modulo 2: inserimento spese
from budget   import definisci_budget      # Modulo 3: definizione budget mensile
from report   import visualizza_report     # Modulo 4: visualizzazione report


def mostra_benvenuto() -> None:
    """
    Visualizza il messaggio di benvenuto al primo avvio.

    Dalla specifica: "All'avvio, il programma deve visualizzare un
    messaggio di benvenuto."
    """
    print("=" * 45)
    print("   SISTEMA DI GESTIONE DELLE SPESE PERSONALI")
    print("=" * 45)
    print("  Benvenuto nel tuo gestore di spese personali.")
    print("  Tieni traccia delle tue uscite e del tuo budget")
    print("  in modo semplice e organizzato.")
    print("=" * 45)


def mostra_menu_principale() -> None:
    """
    Visualizza il Menu Principale.

    Struttura esatta dalla specifica del documento:
      -------------------------
       SISTEMA SPESE PERSONALI
      -------------------------
      1. Gestione Categorie
      2. Inserisci Spesa
      3. Definisci Budget Mensile
      4. Visualizza Report
      5. Esci
      -------------------------
    """
    print("\n" + "-" * 33)
    print("   SISTEMA SPESE PERSONALI")
    print("-" * 33)
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-" * 33)


def esegui_menu() -> None:
    """
    Ciclo principale del programma.

    Implementa il flusso richiesto dalla specifica:
      1. Mostra il menu
      2. Legge la scelta dell'utente (cin)
      3. Seleziona il modulo tramite switch (if/elif in Python)
      4. Ritorna al menu, salvo scelta "Esci"

    Dalla specifica: "Se la scelta non è compresa tra 1 e 5, il programma
    deve visualizzare: Scelta non valida. Riprovare."
    """
    # Ciclo iterativo: si ripete fino a quando l'utente sceglie "5. Esci"
    while True:

        # --- Output: visualizza il menu principale ---
        mostra_menu_principale()

        # --- Input: acquisisce la scelta dell'utente ---
        scelta = input("Inserisci la tua scelta: ").strip()

        # --- Switch: selezione del modulo tramite if/elif ---
        if scelta == "1":
            # Modulo 1 — Gestione delle Categorie
            gestisci_categorie()

        elif scelta == "2":
            # Modulo 2 — Inserimento di una Spesa
            inserisci_spesa()

        elif scelta == "3":
            # Modulo 3 — Definizione del Budget Mensile
            definisci_budget()

        elif scelta == "4":
            # Modulo 4 — Visualizzazione dei Report (con sottomenu)
            visualizza_report()

        elif scelta == "5":
            # Uscita dal programma (dalla specifica)
            print("\nArrivederci! Il tuo database è stato salvato.")
            print("File database: spese.db")
            break  # Esce dal ciclo while → termina il programma

        else:
            # Input non valido (dalla specifica: "Scelta non valida. Riprovare.")
            print("Scelta non valida. Riprovare.")


# ---------------------------------------------------------------------------
# Entry point: Python esegue questo blocco solo quando il file viene lanciato
# direttamente (non importato come modulo)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Mostra il messaggio di benvenuto
    mostra_benvenuto()

    # 2. Avvia il ciclo del menu principale
    esegui_menu()
