"""
report.py — Modulo 4: Visualizzazione dei Report.

Specifica (dal documento):
  Il modulo include un sottomenu con switch:
    1. Totale spese per categoria
    2. Spese mensili vs budget
    3. Elenco completo delle spese ordinate per data
    4. Ritorna al menu principale

  Ogni report esegue query SQL e formatta l'output su console.
"""

from database import get_connection  # Connessione centralizzata al database


def visualizza_report() -> None:
    """
    Punto di ingresso del Modulo 4: Visualizzazione dei Report.

    Mostra un sottomenu e gestisce la selezione tramite ciclo while + if/elif
    (equivalente allo switch richiesto dalla specifica).
    Il ciclo si ripete finché l'utente non sceglie di tornare al menu principale.
    """
    while True:
        # ------------------------------------------------------------------
        # Sottomenu dei report (dalla specifica)
        # ------------------------------------------------------------------
        print("\n--- Visualizza Report ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Torna al menu principale")
        print("-" * 35)

        scelta = input("Inserisci la tua scelta: ").strip()

        # Selezione tramite if/elif (switch)
        if scelta == "1":
            _report_totale_per_categoria()
        elif scelta == "2":
            _report_mensile_vs_budget()
        elif scelta == "3":
            _report_elenco_completo()
        elif scelta == "4":
            # Uscita dal sottomenu: ritorno al menu principale
            break
        else:
            print("Scelta non valida. Riprovare.")


# ---------------------------------------------------------------------------
# REPORT 1 — Totale delle Spese per Categoria
# ---------------------------------------------------------------------------

def _report_totale_per_categoria() -> None:
    """
    REPORT 1: Calcola e visualizza il totale delle spese per ogni categoria.

    Query SQL:
      - GROUP BY categoria: aggrega tutte le spese per categoria
      - SUM(importo): calcola il totale per ogni gruppo
      - INNER JOIN: collega spese → categorie per ottenere il nome

    Output atteso (dalla specifica):
      Categoria........Totale Speso
      Alimentari.......320.50
      Trasporti........120.00
    """
    print("\n========================================")
    print("  REPORT 1 — Totale Spese per Categoria")
    print("========================================")

    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL SELECT con GROUP BY e SUM: calcola il totale speso per categoria
        cursore.execute(
            """
            SELECT
                c.nome          AS categoria,
                SUM(s.importo)  AS totale_speso   -- SUM: somma di tutti gli importi
            FROM spese s
            INNER JOIN categorie c ON s.categoria_id = c.id
            GROUP BY c.id, c.nome                 -- GROUP BY: una riga per categoria
            ORDER BY totale_speso DESC;            -- ordina dalla spesa maggiore
            """
        )
        righe = cursore.fetchall()

        if not righe:
            print("\nNessuna spesa registrata.")
            return

        # Intestazione (stile dalla specifica)
        print("\n{:<25} {:>15}".format("Categoria", "Totale Speso (€)"))
        print("-" * 42)

        # Stampa ogni riga del risultato
        for riga in righe:
            print("{:<25} {:>15.2f}".format(
                riga["categoria"],
                riga["totale_speso"]
            ))

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# REPORT 2 — Spese Mensili vs Budget
# ---------------------------------------------------------------------------

def _report_mensile_vs_budget() -> None:
    """
    REPORT 2: Confronta il totale speso per mese/categoria con il budget definito.

    Elaborazione (dalla specifica):
      1. Calcolo del totale speso per mese e categoria (SQL)
      2. Confronto con il budget tramite if/else
      3. Visualizzazione dello stato: "SUPERAMENTO BUDGET" o "ENTRO BUDGET"

    La query usa LEFT JOIN: mostra anche le categorie con budget ma senza spese,
    e anche le spese senza un budget definito.

    Output atteso (dalla specifica):
      Mese: 2025-01
      Categoria: Alimentari | Budget: 300.00 | Speso: 320.00 | Stato: SUPERAMENTO BUDGET
    """
    print("\n========================================")
    print("  REPORT 2 — Spese Mensili vs Budget")
    print("========================================")

    conn = get_connection()
    try:
        cursore = conn.cursor()

        # Query SQL — Unisce spese aggregate per mese/categoria con i budget
        # FULL OUTER JOIN non esiste in SQLite, quindi usiamo UNION di due LEFT JOIN
        cursore.execute(
            """
            SELECT
                COALESCE(spese_agg.mese, bm.mese)              AS mese,
                c.nome                                          AS categoria,
                COALESCE(spese_agg.totale_speso, 0)            AS totale_speso,
                COALESCE(bm.importo, 0)                        AS budget
            FROM (
                -- Sottocartella: totale speso per mese e categoria
                SELECT
                    strftime('%Y-%m', s.data)   AS mese,     -- estrae YYYY-MM dalla data
                    s.categoria_id,
                    SUM(s.importo)              AS totale_speso
                FROM spese s
                GROUP BY strftime('%Y-%m', s.data), s.categoria_id
            ) AS spese_agg
            -- LEFT JOIN con budget_mensile per trovare il budget corrispondente
            LEFT JOIN budget_mensile bm
                ON spese_agg.categoria_id = bm.categoria_id
                AND spese_agg.mese = bm.mese
            -- JOIN con categorie per ottenere il nome
            INNER JOIN categorie c ON spese_agg.categoria_id = c.id

            UNION

            -- Aggiunge le categorie con budget ma senza spese nel mese
            SELECT
                bm.mese,
                c.nome,
                0            AS totale_speso,
                bm.importo   AS budget
            FROM budget_mensile bm
            INNER JOIN categorie c ON bm.categoria_id = c.id
            WHERE NOT EXISTS (
                SELECT 1 FROM spese s
                WHERE s.categoria_id = bm.categoria_id
                  AND strftime('%Y-%m', s.data) = bm.mese
            )

            ORDER BY mese DESC, categoria;
            """
        )
        righe = cursore.fetchall()

        if not righe:
            print("\nNessuna spesa o budget registrati.")
            return

        # Intestazione tabella
        print("\n{:<10} {:<20} {:>10} {:>10} {:<20}".format(
            "Mese", "Categoria", "Budget(€)", "Speso(€)", "Stato"
        ))
        print("-" * 75)

        # Stampa ogni riga con confronto if/else (dalla specifica)
        for riga in righe:
            speso  = riga["totale_speso"]
            budget = riga["budget"]

            # --- Confronto if/else richiesto dalla specifica ---
            if budget > 0 and speso > budget:
                stato = "⚠ SUPERAMENTO BUDGET"
            elif budget > 0 and speso <= budget:
                stato = "✓ ENTRO BUDGET"
            elif budget == 0:
                stato = "— Nessun budget"
            else:
                stato = "—"

            print("{:<10} {:<20} {:>10.2f} {:>10.2f} {:<20}".format(
                riga["mese"],
                riga["categoria"],
                budget,
                speso,
                stato
            ))

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# REPORT 3 — Elenco Completo delle Spese Ordinate per Data
# ---------------------------------------------------------------------------

def _report_elenco_completo() -> None:
    """
    REPORT 3: Visualizza l'elenco completo di tutte le spese, ordinate per data.

    Query SQL:
      - INNER JOIN: unisce spese con categorie per ottenere il nome
      - ORDER BY data ASC: dalla spesa più vecchia alla più recente

    Output atteso (dalla specifica):
      Data         Categoria  Importo  Descrizione
      -----------------------------------------------
      2025-01-15   Alimentari   25.00  Pranzo
    """
    print("\n========================================")
    print("  REPORT 3 — Elenco Completo delle Spese")
    print("========================================")

    conn = get_connection()
    try:
        cursore = conn.cursor()

        # SQL SELECT — tutte le spese con nome categoria, ordinate per data
        cursore.execute(
            """
            SELECT
                s.data,
                c.nome        AS categoria,
                s.importo,
                s.descrizione
            FROM spese s
            INNER JOIN categorie c ON s.categoria_id = c.id
            ORDER BY s.data ASC, s.id ASC;   -- data crescente; ID come tiebreaker
            """
        )
        righe = cursore.fetchall()

        if not righe:
            print("\nNessuna spesa registrata.")
            return

        # Intestazione (stile dalla specifica)
        print("\n{:<12} {:<15} {:>10} {:<30}".format(
            "Data", "Categoria", "Importo(€)", "Descrizione"
        ))
        print("-" * 70)

        # Stampa ogni riga
        totale_generale = 0.0
        for riga in righe:
            descrizione = riga["descrizione"] if riga["descrizione"] else ""
            print("{:<12} {:<15} {:>10.2f} {:<30}".format(
                riga["data"],
                riga["categoria"],
                riga["importo"],
                descrizione
            ))
            totale_generale += riga["importo"]

        # Riga totale a fondo report
        print("-" * 70)
        print("{:<28} {:>10.2f} {:}".format(
            "TOTALE GENERALE:", totale_generale, ""
        ))

    finally:
        conn.close()
