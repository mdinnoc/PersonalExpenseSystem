-- =============================================================================
-- dati_esempio.sql — Script SQL di inserimento dati di esempio
--
-- Sistema di Gestione delle Spese Personali e del Budget
--
-- Questo script popola il database con dati sufficienti a dimostrare
-- il funzionamento completo del sistema, inclusi:
--   - Categorie di spesa
--   - Spese per più mesi
--   - Budget mensili (con casi di superamento e rispetto del limite)
--
-- ATTENZIONE: Le tabelle vengono create automaticamente da main.py (primo avvio)
-- oppure eseguendo prima schema.sql.
--
-- Procedura consigliata:
--   sqlite3 spese.db < schema.sql      # crea le tabelle
--   sqlite3 spese.db < dati_esempio.sql  # inserisce i dati
-- =============================================================================

-- Abilita il supporto alle FOREIGN KEY (obbligatorio in SQLite)
PRAGMA foreign_keys = ON;


-- =============================================================================
-- INSERIMENTO CATEGORIE
-- Vincoli verificati: NOT NULL, UNIQUE sul nome
-- =============================================================================
INSERT INTO categorie (nome) VALUES ('Alimentari');    -- id = 1
INSERT INTO categorie (nome) VALUES ('Trasporti');     -- id = 2
INSERT INTO categorie (nome) VALUES ('Svago');         -- id = 3
INSERT INTO categorie (nome) VALUES ('Salute');        -- id = 4
INSERT INTO categorie (nome) VALUES ('Abbigliamento'); -- id = 5


-- =============================================================================
-- INSERIMENTO SPESE — Gennaio 2025
-- Vincoli verificati: NOT NULL su data/importo, CHECK (importo > 0),
--                     FOREIGN KEY (categoria_id esiste in categorie)
-- =============================================================================

-- Alimentari — Gennaio 2025
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-03', 45.20, 1, 'Spesa settimanale supermercato');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-08', 12.50, 1, 'Pranzo in ufficio');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-12', 38.90, 1, 'Spesa supermercato');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-15', 25.00, 1, 'Pranzo fuori');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-20', 52.30, 1, 'Spesa settimanale + pulizia');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-27', 48.60, 1, 'Spesa fine mese');

-- Somma Alimentari Gennaio: 222.50 → ENTRO il budget di 250.00


-- Trasporti — Gennaio 2025
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-02', 35.00, 2, 'Abbonamento mensile autobus');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-10', 18.50, 2, 'Taxi aeroporto');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-22', 55.00, 2, 'Pieno benzina');

-- Somma Trasporti Gennaio: 108.50 → ENTRO il budget di 120.00


-- Svago — Gennaio 2025
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-05', 15.00, 3, 'Cinema');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-14', 22.00, 3, 'Cena con amici');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-25', 40.00, 3, 'Concerto');

-- Somma Svago Gennaio: 77.00 → ENTRO il budget di 80.00


-- Salute — Gennaio 2025 (nessun budget definito per questa categoria)
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-18', 30.00, 4, 'Visita medica');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-01-18', 28.50, 4, 'Farmaci');


-- =============================================================================
-- INSERIMENTO SPESE — Febbraio 2025
-- Caso di SUPERAMENTO BUDGET per la categoria Alimentari
-- =============================================================================

-- Alimentari — Febbraio 2025 (budget: 250.00 → speso: 320.50 → SUPERAMENTO)
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-01', 55.00, 1, 'Spesa settimanale');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-07', 48.90, 1, 'Spesa + prodotti casa');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-13', 62.40, 1, 'Spesa abbondante per ospiti');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-19', 72.20, 1, 'Spesa e vini per cena');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-25', 82.00, 1, 'Spesa fine mese extra');

-- Somma Alimentari Febbraio: 320.50 → SUPERAMENTO del budget di 250.00


-- Trasporti — Febbraio 2025
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-03', 35.00, 2, 'Abbonamento mensile autobus');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-15', 45.00, 2, 'Pieno benzina');

-- Somma Trasporti Febbraio: 80.00 → ENTRO il budget di 120.00


-- Abbigliamento — Febbraio 2025 (nessun budget definito)
INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-10', 89.99, 5, 'Scarpe invernali');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2025-02-22', 45.00, 5, 'Maglione');


-- =============================================================================
-- INSERIMENTO BUDGET MENSILI
-- Vincoli verificati: NOT NULL, CHECK (importo > 0),
--                     FOREIGN KEY, UNIQUE(mese, categoria_id)
-- =============================================================================

-- Budget Gennaio 2025
INSERT INTO budget_mensile (mese, categoria_id, importo)
VALUES ('2025-01', 1, 250.00);   -- Alimentari: limite 250.00 €

INSERT INTO budget_mensile (mese, categoria_id, importo)
VALUES ('2025-01', 2, 120.00);   -- Trasporti: limite 120.00 €

INSERT INTO budget_mensile (mese, categoria_id, importo)
VALUES ('2025-01', 3, 80.00);    -- Svago: limite 80.00 €


-- Budget Febbraio 2025
INSERT INTO budget_mensile (mese, categoria_id, importo)
VALUES ('2025-02', 1, 250.00);   -- Alimentari: limite 250.00 € (SUPERATO: speso 320.50)

INSERT INTO budget_mensile (mese, categoria_id, importo)
VALUES ('2025-02', 2, 120.00);   -- Trasporti: limite 120.00 €

INSERT INTO budget_mensile (mese, categoria_id, importo)
VALUES ('2025-02', 3, 60.00);    -- Svago: limite 60.00 €


-- =============================================================================
-- VERIFICA DEI DATI INSERITI
-- Queste query di controllo mostrano che i dati sono stati inseriti
-- correttamente e che i vincoli di integrità funzionano
-- =============================================================================

-- Verifica categorie
SELECT 'Categorie inserite: ' || COUNT(*) AS riepilogo FROM categorie;

-- Verifica spese
SELECT 'Spese inserite: ' || COUNT(*) AS riepilogo FROM spese;

-- Verifica budget
SELECT 'Budget definiti: ' || COUNT(*) AS riepilogo FROM budget_mensile;

-- Verifica FOREIGN KEY: tutte le spese hanno una categoria valida
SELECT 'Spese con categoria valida: ' || COUNT(*) AS riepilogo
FROM spese s
INNER JOIN categorie c ON s.categoria_id = c.id;

-- Anteprima Report 1 — Totale per categoria
SELECT c.nome AS Categoria, ROUND(SUM(s.importo), 2) AS Totale
FROM spese s
INNER JOIN categorie c ON s.categoria_id = c.id
GROUP BY c.nome
ORDER BY Totale DESC;
