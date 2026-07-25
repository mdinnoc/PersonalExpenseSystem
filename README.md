Sistema di Gestione delle Spese Personali e del Budget

Applicazione console sviluppata in **Python** con database **SQLite** per la
gestione delle spese personali, delle categorie e dei budget mensili.

---

Requisiti per l'Esecuzione

Interprete necessario
- **Python 3.10** o versione superiore

Librerie utilizzate
Sono tutte librerie standard di Python — non è necessario installare nulla:

| Libreria  | Uso nel progetto                          |
|-----------|-------------------------------------------|
| `sqlite3` | Connessione e operazioni sul database SQL |
| `re`      | Validazione del formato di data e mese    |
| `os`      | Percorso del file di database             |

---

Struttura del Repository

```
sistema-spese/
├── main.py           # Punto di ingresso — menu principale + ciclo di controllo
├── database.py       # Configurazione database, creazione tabelle, connessione
├── categorie.py      # Modulo 1 — Gestione delle Categorie
├── spese.py          # Modulo 2 — Inserimento di una Spesa
├── budget.py         # Modulo 3 — Definizione del Budget Mensile
├── report.py         # Modulo 4 — Visualizzazione dei Report
├── schema.sql        # Script SQL di creazione delle tabelle (con tutti i vincoli)
├── dati_esempio.sql  # Script SQL di inserimento dati di esempio
└── README.md         # Questo file
```

Il file `spese.db` viene creato automaticamente nella stessa cartella al primo avvio.


Schema del Database

```
categorie
┌─────────────────────────┐
│ id   INTEGER PK         │
│ nome TEXT NOT NULL UNIQ │
└────────────┬────────────┘
             │ 1
             ├──────────────────────────────────────┐                                                                                 │ N                                    │ N
             ▼                                      ▼
           spese                              budget_mensile
┌─────────────────────────┐            ┌─────────────────────────┐
│ id           INTEGER PK │            │ id           INTEGER PK │
│ data         TEXT NN    │            │ mese         TEXT NN    │
│ importo      REAL NN >0 │            │ categoria_id INTEGER FK │
│ categoria_id INTEGER FK |            │ importo      REAL NN >0 │
│ descrizione  TEXT       │            │ UNIQUE(mese, cat_id)    │
└─────────────────────────┘            └─────────────────────────┘
```

Legenda: PK = PRIMARY KEY ; FK = FOREIGN KEY ; NN = NOT NULL ; UNIQ = UNIQUE

Vincoli di integrità implementati

| Vincolo       |applicato in                                                             |
|---------------|-------------------------------------------------------------------------|
| `PRIMARY KEY` | Ogni tabella ha un `id` auto-incrementale                               |
| `FOREIGN KEY` | `spese.categoria_id` e `budget_mensile.categoria_id` → `categorie.id`   |
| `NOT NULL`    | `data`, `importo`, `categoria_id` in spese; `mese`, `importo` in budget |
| `UNIQUE`      | `categorie.nome`; coppia `(mese, categoria_id)` in budget               |
| `CHECK`       | `importo > 0` in spese; `importo > 0` in budget_mensile                 |

---

Menu dell'Applicazione

```
---------------------------------
   SISTEMA SPESE PERSONALI
---------------------------------
1. Gestione Categorie
2. Inserisci Spesa
3. Definisci Budget Mensile
4. Visualizza Report
5. Esci
---------------------------------
```

---
 Moduli Funzionali

 Modulo 1 — Gestione Categorie
- Aggiunge nuove categorie di spesa (es. Alimentari, Trasporti, Svago)
- Verifica duplicati prima dell'inserimento (SQL SELECT → INSERT)
- Visualizza tutte le categorie esistenti

 Modulo 2 — Inserimento Spesa
- Registra una spesa con data, importo, categoria e descrizione opzionale
- Valida il formato della data (YYYY-MM-DD) e l'importo (> 0)
- Verifica che la categoria esista prima dell'inserimento

 Modulo 3 — Budget Mensile
- Imposta un limite di spesa per categoria e mese (formato YYYY-MM)
- Se il budget per quella coppia mese/categoria esiste, lo aggiorna
- Valida che il budget sia > 0 e che la categoria esista

 Modulo 4 — Report (sottomenu)
1. Totale spese per categoria — somma aggregata con GROUP BY
2. Spese mensili vs budget — confronto con stato (ENTRO / SUPERAMENTO)
3. Elenco completo — tutte le spese ordinate per data con totale generale

---

 Esempio di Sessione

```
=============================================
   SISTEMA DI GESTIONE DELLE SPESE PERSONALI
=============================================
  Benvenuto nel tuo gestore di spese personali.

---------------------------------
   SISTEMA SPESE PERSONALI
---------------------------------
1. Gestione Categorie
2. Inserisci Spesa
3. Definisci Budget Mensile
4. Visualizza Report
5. Esci
---------------------------------
Inserisci la tua scelta: 1

--- Gestione Categorie ---
1. Aggiungi una nuova categoria
2. Visualizza tutte le categorie
3. Torna al menu principale
Nome della nuova categoria: Alimentari
Categoria inserita correttamente.

Inserisci la tua scelta: 2
Data (YYYY-MM-DD): 2025-01-15
Importo (es. 25.50): 25.00
Categoria: Alimentari
Descrizione (opzionale): Pranzo
Spesa inserita correttamente.
```

---

 Note Tecniche

- Il database `spese.db` è un file SQLite che viene creato automaticamente nella
  stessa cartella di `main.py` al primo avvio del programma.
- Le FOREIGN KEY di SQLite sono disabilitate per default: il programma le abilita
  esplicitamente con `PRAGMA foreign_keys = ON` ad ogni connessione.
- Tutti i confronti sui nomi delle categorie sono **case-insensitive**
  (es. "alimentari" e "Alimentari" sono trattati come uguali).
- L'applicazione non richiede connessione a internet né server esterni.
