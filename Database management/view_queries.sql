CREATE VIEW sectorBuying AS
    (   SELECT Buying.*, C.Sector
        FROM Buying INNER JOIN Company C on Buying.Symbol = C.Symbol);

CREATE VIEW allBuying AS
    (   SELECT Buying.*, S.Price
        FROM Buying INNER JOIN Stock S on Buying.Symbol = S.Symbol and Buying.tDate = S.tDate );

CREATE VIEW varietyInvestor1 AS
    (  SELECT S1.ID, S1.tDate, COUNT(DISTINCT S1.Sector) as count
        FROM sectorBuying S1
        GROUP BY S1.ID, S1.tDate);

CREATE VIEW varietyInvestor2 AS
    (  SELECT DISTINCT S1.ID
        FROM varietyInvestor1 S1
        WHERE S1.count>7);

CREATE VIEW sumInvestments AS
    (   SELECT allBuying.ID, SUM(allBuying.Price*allBuying.BQuantity) as Sum
        FROM allBuying
        GROUP BY allBuying.ID);

CREATE VIEW nameVarietyInvestor AS
    (   SELECT Investor.Name, Investor.ID
        FROM varietyInvestor2 INNER JOIN Investor ON varietyInvestor2.ID=Investor.ID);


 -----------------------------------


 CREATE VIEW bigInvestor AS
    (   SELECT Buying.ID, Buying.Symbol, SUM(Buying.BQuantity) as sum
        FROM Buying
        GROUP BY Buying.ID, Buying.Symbol);


CREATE VIEW bigSymbol AS
    (   SELECT bigInvestor.Symbol, MAX(bigInvestor.sum) as max
        FROM bigInvestor
        GROUP BY bigInvestor.Symbol);

CREATE VIEW bigSymbol2 AS
    (   SELECT bigInvestor.Symbol, bigInvestor.ID, bS.max
        FROM bigInvestor INNER JOIN bigSymbol bS on bigInvestor.Symbol = bS.Symbol
        WHERE bigInvestor.sum = bS.max AND bS.max>10);

CREATE VIEW bigSymbol3 AS
    (   SELECT bigSymbol2.Symbol, bigSymbol2.ID, Investor.Name,bigSymbol2.max
        FROM bigSymbol2 INNER JOIN Investor on bigSymbol2.ID = Investor.ID);


CREATE VIEW length AS
    (   SELECT COUNT(DISTINCT tDate) as num
        FROM Buying
        );


CREATE VIEW popular AS
    (   SELECT Buying.Symbol
        FROM Buying , length
        GROUP BY Buying.Symbol, length.num
        HAVING COUNT(DISTINCT tDate)>(length.num/2) );

----------------------------------------------

CREATE VIEW once AS
    (   SELECT Buying.Symbol
        FROM Buying
        GROUP BY Buying.Symbol
        HAVING(COUNT(Buying.tDate)=1));

CREATE VIEW once1 AS
    (
        SELECT Buying.Symbol, Buying.tDate, Buying.ID
        FROM Buying INNER JOIN once o on Buying.Symbol = o.Symbol
        );


CREATE VIEW successor AS
    (   SELECT b1.tDate, MIN(b2.tDate) AS minDate
        FROM Stock b1 , Stock b2
        WHERE b1.tDate < b2.tDate
        GROUP BY b1.tDate );

CREATE VIEW onceSuccessor AS
    (   SELECT once1.ID, once1.tDate AS day1, once1.Symbol, s.minDate
        FROM once1 INNER JOIN successor s on once1.tDate = s.tDate
    );

CREATE VIEW priceDay1 AS
    (   SELECT s.*, Stock.Price AS price1
        FROM Stock INNER JOIN onceSuccessor s on Stock.Symbol = s.Symbol AND Stock.tDate= s.day1

    );

CREATE VIEW priceDay2 AS
    (   SELECT s.*, Stock.Price AS price2
        FROM Stock INNER JOIN priceDay1 s on Stock.Symbol = s.Symbol AND Stock.tDate= s.minDate
    );

CREATE VIEW finalName AS
    (   SELECT s.*, Investor.Name
        FROM Investor INNER JOIN priceDay2 s on Investor.ID=s.ID
    );




















