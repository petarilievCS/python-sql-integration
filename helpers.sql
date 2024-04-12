-- COMP3311 24T1 Ass2 ... SQL helper Views/Functions
-- Add any views or functions you need into this file
-- Note: it must load without error into a freshly created Pokemon database

-- The `dbpop()` function is provided for you in the dump file
-- This is provided in case you accidentally delete it

DROP TYPE IF EXISTS Population_Record CASCADE;
CREATE TYPE Population_Record AS (
	Tablename Text,
	Ntuples   Integer
);

CREATE OR REPLACE FUNCTION DBpop()
    RETURNS SETOF Population_Record
    AS $$
        DECLARE
            rec Record;
            qry Text;
            res Population_Record;
            num Integer;
        BEGIN
            FOR rec IN SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename LOOP
                qry := 'SELECT count(*) FROM ' || quote_ident(rec.tablename);

                EXECUTE qry INTO num;

                res.tablename := rec.tablename;
                res.ntuples   := num;

                RETURN NEXT res;
            END LOOP;
        END;
    $$ LANGUAGE plpgsql
;

--
-- Example Views/Functions
-- These Views/Functions may or may not be useful to you.
-- You may modify or delete them as you see fit.
--

-- `Move_Learning_Info`
-- The `Learnable_Moves` table is a relation between Pokemon, Moves, Games and Requirements.
-- As it just consists of foreign keys, it is not very easy to read.
-- This view makes it easier to read by displaying the names of the Pokemon, Moves and Games instead of their IDs.
CREATE OR REPLACE VIEW Move_Learning_Info(Pokemon, Move, Game, Requirement) AS
    SELECT
        P.Name,
        M.Name,
        G.Name,
        R.Assertion
    FROM
        Learnable_Moves AS L
        JOIN Pokemon AS P
        ON Learnt_By = P.ID
        JOIN Games AS G
        ON Learnt_In = G.ID
        JOIN Moves AS M
        ON Learns = M.ID
        JOIN Requirements AS R
        ON Learnt_When = R.ID
;

-- `Super_Effective`
-- This function takes a type name and
-- returns a set of all types that it is super effective against (multiplier > 100)
-- eg Water is super effective against Fire, so `Super_Effective('Water')` will return `Fire` (amongst others)
CREATE OR REPLACE FUNCTION Super_Effective(_Type Text)
    RETURNS SETOF Text
    AS $$
        SELECT
            B.Name
        FROM
            Types AS A
            JOIN Type_Effectiveness AS E
            ON A.ID = E.Attacking
            JOIN Types AS B
            ON B.ID = E.Defending
        WHERE
            A.Name = _Type
            AND
            E.Multiplier > 100
    $$ LANGUAGE SQL
;

--
-- Your Views/Functions Below Here
-- Remember This file must load into a clean Pokemon database in one pass without any error
-- NOTICEs are fine, but ERRORs are not
-- Views/Functions must be defined in the correct order (dependencies first)
-- eg if my_supper_clever_function() depends on my_other_function() then my_other_function() must be defined first
-- Your Views/Functions Below Here
--

SELECT g.name, l.name, e.rarity, e.levels
FROM Pokemon p
JOIN Encounters e ON (e.occurs_with = p.id)
JOIN Locations l ON (e.occurs_at = l.id)
JOIN Games g ON (l.appears_in = g.id)
WHERE p.name = 'Pikachu'
ORDER BY g.region, g.name, l.name, e.rarity, e.levels;

--- 
--- Given an encounter id
--- Returns a list of encounter requirements
---
CREATE OR REPLACE FUNCTION Get_Requirements(encounter_id INT) 
RETURNS TEXT AS $$
DECLARE
    requirements TEXT := '';
    requirement TEXT;
    inverted BOOLEAN;
    tuple RECORD;
BEGIN
    FOR tuple IN 
        SELECT r.assertion, er.inverted
        FROM Encounter_Requirements er
        JOIN Requirements r ON (er.requirement = r.id)
        WHERE er.encounter = encounter_id
        ORDER BY r.assertion
    LOOP
        requirement := tuple.assertion;
        inverted := tuple.inverted;

        IF inverted THEN
            requirement := 'Not ' || requirement; 
        END IF;
        requirements := requirements || requirement || ', ';

    END LOOP;
    requirements := LEFT(requirements, LENGTH(requirements) - 2);
    RETURN requirements;
END; 
$$ LANGUAGE PLpgSQL;

---
--- Given rarirty as an integer, returns the corressponding string
---
CREATE OR REPLACE FUNCTION Get_Rarity_String(rarity INT) 
RETURNS TEXT AS $$ 
DECLARE
    result TEXT := '';
BEGIN
    IF rarity >= 21 THEN
        result := 'Common';
    ELSIF rarity >= 6 AND rarity <= 20 THEN
        result := 'Uncommon';
    ELSIF rarity >= 1 AND rarity <= 5 THEN
        result := 'Rare';
    ELSE 
        result := 'Limited';
    END IF;

    RETURN result;
END;
$$ LANGUAGE PLpgSQL;

--- 
--- View with information for every pokemon encounter (game, location, rarity, levels, requirements)
---
CREATE OR REPLACE VIEW Q2(Region, Pokemon, Game, Location, Rarity, MinLevel, MaxLevel, Requirements) AS
    SELECT g.region, p.name, g.name, l.name, Get_Rarity_String(e.rarity), min(e.levels), max(e.levels), Get_Requirements(e.id)
    FROM Pokemon p
    JOIN Encounters e ON (e.occurs_with = p.id)
    JOIN Locations l ON (e.occurs_at = l.id)
    JOIN Games g ON (l.appears_in = g.id)
    ORDER BY g.region;

