-- =============================================================================
-- schema.sql — Script SQL di creazione del database
--
-- Sistema di Gestione delle Spese Personali e del Budget
--
-- Questo file definisce la struttura completa del database relazionale.
-- Contiene tutti i vincoli di integrità richiesti dalla specifica:
--   - PRIMARY KEY   (su ogni tabella)
--   - FOREIGN KEY   (in spese e budget_mensile → categorie)
--   - NOT NULL      (su tutti i campi obbligatori)
--   - UNIQUE        (su categorie.nome e su coppia mese/categoria nel budget)
--   - CHECK         (importo > 0 in spese e in budget_mensile)
--
-- Database: SQLite (database SQL relazionale, file-based, senza server)
-- Compatible con: SQLite 3.x
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Configurazione iniziale
-- Abilita il supporto alle FOREIGN KEY (disabilitato di default in SQLite)
-- -----------------------------------------------------------------------------
PRAGMA foreign_keys = ON;


-- -----------------------------------------------------------------------------
-- Rimozione delle tabelle (in ordine inverso rispetto alle dipendenze)
-- per consentire una ricreazione pulita dello schema durante i test
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS budget_mensile;
DROP TABLE IF EXISTS spese;
DROP TABLE IF EXISTS categorie;


-- =============================================================================
-- TABELLA: categorie
--
-- Memorizza le categorie di spesa definite dall'utente.
-- Esempi: Alimentari, Trasporti, Svago, Salute, Abbigliamento
--
-- Vincoli presenti:
--   - PRIMARY KEY AUTOINCREMENT  (id univoco auto-generato)
--   - NOT NULL                   (nome obbligatorio)
--   - UNIQUE                     (nessun duplicato di nome)
-- =============================================================================
CREATE TABLE IF NOT EXISTS categorie (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,   -- PRIMARY KEY: identificatore univoco
    nome  TEXT    NOT NULL                      -- NOT NULL: il nome è obbligatorio
                  UNIQUE                        -- UNIQUE: non possono esistere due categorie con lo stesso nome
);


-- =============================================================================
-- TABELLA: spese
--
-- Registra ogni singola transazione di spesa effettuata dall'utente.
--
-- Vincoli presenti:
--   - PRIMARY KEY AUTOINCREMENT  (id univoco auto-generato)
--   - NOT NULL                   (data e importo obbligatori)
--   - CHECK                      (importo deve essere strettamente > 0)
--   - FOREIGN KEY                (categoria_id riferisce categorie.id)
--   - ON DELETE RESTRICT         (impedisce la cancellazione di una categoria in uso)
--
-- Colonne:
--   id           — chiave primaria auto-incrementale
--   data         — data della spesa in formato YYYY-MM-DD (es. 2025-01-15)
--   importo      — valore monetario della spesa (es. 25.50)
--   categoria_id — riferimento alla categoria di appartenenza
--   descrizione  — nota opzionale (può essere NULL)
-- =============================================================================
CREATE TABLE IF NOT EXISTS spese (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    data         TEXT     NOT NULL,                           -- NOT NULL: data obbligatoria
    importo      REAL     NOT NULL                            -- NOT NULL: importo obbligatorio
                          CHECK (importo > 0),               -- CHECK: importo deve essere positivo
    categoria_id INTEGER  NOT NULL                            -- NOT NULL: la categoria è obbligatoria
                          REFERENCES categorie(id)           -- FOREIGN KEY verso categorie
                              ON DELETE RESTRICT             -- impedisce di cancellare categorie usate
                              ON UPDATE CASCADE,             -- aggiorna categoria_id se l'id cambia
    descrizione  TEXT                                         -- campo opzionale (NULL ammesso)
);


-- =============================================================================
-- TABELLA: budget_mensile
--
-- Definisce il limite di spesa mensile per ogni categoria.
-- Un utente può impostare un budget diverso per ogni mese e categoria.
--
-- Vincoli presenti:
--   - PRIMARY KEY AUTOINCREMENT  (id univoco auto-generato)
--   - NOT NULL                   (mese, categoria_id e importo obbligatori)
--   - CHECK                      (importo budget deve essere > 0)
--   - FOREIGN KEY                (categoria_id riferisce categorie.id)
--   - UNIQUE(mese, categoria_id) (un solo budget per coppia mese-categoria)
--
-- Colonne:
--   id           — chiave primaria auto-incrementale
--   mese         — mese di riferimento in formato YYYY-MM (es. 2025-01)
--   categoria_id — categoria a cui si riferisce il budget
--   importo      — limite di spesa mensile (es. 300.00)
-- =============================================================================
CREATE TABLE IF NOT EXISTS budget_mensile (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    mese         TEXT     NOT NULL,                           -- NOT NULL: mese obbligatorio
    categoria_id INTEGER  NOT NULL                            -- NOT NULL: categoria obbligatoria
                          REFERENCES categorie(id)           -- FOREIGN KEY verso categorie
                              ON DELETE RESTRICT
                              ON UPDATE CASCADE,
    importo      REAL     NOT NULL                            -- NOT NULL: importo budget obbligatorio
                          CHECK (importo > 0),               -- CHECK: budget deve essere positivo
    UNIQUE (mese, categoria_id)                              -- UNIQUE: un solo budget per mese/categoria
);


-- =============================================================================
-- SCHEMA LOGICO (rappresentazione testuale)
--
--   categorie
--   ┌─────────────────────────┐
--   │ id   INTEGER PK         │
--   │ nome TEXT NOT NULL UNI  │
--   └────────────┬────────────┘
--                │ 1
--                │
--      ┌─────────┴──────────────────────────┐
--      │ N                                  │ N
--      ▼                                    ▼
--   spese                          budget_mensile
--   ┌─────────────────────────┐    ┌─────────────────────────┐
--   │ id           INTEGER PK          │    │ id           INTEGER PK │
--   │ data         TEXT NN             │    │ mese         TEXT NN    │
--   │ importo      REAL NN,>0          │    │ categoria_id INTEGER FK │
--   │ categoria_id INTEGER FK          │    │ importo      REAL NN,>0 │
--   │ descrizione  TEXT                │    │ UNIQUE(mese,cat_id)     │
--   └─────────────────────────┘    └─────────────────────────┘
--
-- PK = PRIMARY KEY | FK = FOREIGN KEY | NN = NOT NULL | UNI = UNIQUE
-- =============================================================================
