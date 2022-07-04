from django.shortcuts import render
from .models import Company, Buying, Investor, Stock, Transactions
from django.db import connection
from datetime import datetime


# Create your views here.


def index(request):
    return render(request, 'index.html')


def Query(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nameVarietyInvestor.name, ROUND(sumInvestments.Sum, 3) AS total_amount
            FROM sumInvestments INNER JOIN nameVarietyInvestor ON sumInvestments.ID = nameVarietyInvestor.ID
            ORDER BY total_amount DESC ;

           """)
        sql_res1 = dictfetchall(cursor)
        cursor.execute("""
            SELECT b.symbol, b.name, b.max
            FROM popular INNER JOIN bigSymbol3 b on popular.Symbol = b.Symbol
            ORDER BY b.Symbol ASC, b.Name ;

           """)
        sql_res2 = dictfetchall(cursor)
        cursor.execute("""
            SELECT finalName.symbol , finalName.name, finalName.day1
            FROM finalName
            WHERE price2 > 1.03*finalName.price1
            ORDER BY finalName.day1 ASC , finalName.Symbol ASC ;

                   """)
        sql_res3 = dictfetchall(cursor)
    return render(request, 'Query.html', {'sql_res1': sql_res1, 'sql_res2': sql_res2, 'sql_res3': sql_res3})


def Add(request):
    flag = True
    with connection.cursor() as cursor:
        cursor.execute("""
                                SELECT TOP 10 t.id, t.tdate, t.tquantity
                                FROM Transactions t
                                ORDER BY tDate DESC, ID DESC ; 
                               """)
        sql_res2 = dictfetchall(cursor)
        if request.method == 'POST' and request.POST:
            new_ID = int(request.POST["ID"])
            new_Tran = int(request.POST["Transaction"])
            cursor.execute("""
                    SELECT Investor.ID
                    FROM Investor
                    WHERE Investor.ID = %s;
        
                   """, [new_ID])
            sql_res1 = dictfetchall(cursor)
            if len(sql_res1) == 0:
                flag = False
            else:
                cursor.execute("""
                            SELECT Transactions.tquantity
                            FROM Transactions
                            WHERE Transactions.ID = %s AND Transactions.tDate = %s
                """, [new_ID, datetime.today().strftime('%Y-%m-%d')])
                quantity = dictfetchall(cursor)
                if len(quantity) != 0:
                    cursor.execute("""
                            UPDATE Investor SET AvailableCash= AvailableCash - %s WHERE ID=%s;    
                    """, [quantity[0]['tquantity'], new_ID])

                cursor.execute("""
                            DELETE FROM Transactions WHERE tDate = %s AND ID=%s;
                            """, [datetime.today().strftime('%Y-%m-%d'), new_ID])
                cursor.execute("""
                            UPDATE Investor SET AvailableCash= AvailableCash + %s  WHERE ID=%s;
                            """, [new_Tran, new_ID])
                cursor.execute("""
                            INSERT INTO Transactions (tDate, ID, TQuantity)
                            VALUES (%s, %s, %s);
                            """, [datetime.today().strftime('%Y-%m-%d'), new_ID, new_Tran])
        return render(request, 'Add.html', {'flag': flag, 'sql_res': sql_res2})


def Buy(request):
    errorS = False
    errorC = False
    errorID = False
    errorT = False
    with connection.cursor() as cursor:
        cursor.execute("""      SELECT TOP 10 t.id, t.tdate, ROUND(t.bquantity*s.price,2) as price, t.symbol
                                FROM Buying t INNER JOIN Stock S ON s.tdate= t.tdate AND s.symbol=t.symbol
                                ORDER BY price DESC, ID DESC ; 
                               """)
        sql_res1 = dictfetchall(cursor)
        if request.method == 'POST' and request.POST:
            new_ID = int(request.POST["ID"])
            new_Quantity = int(request.POST["Quantity"])
            new_Symbol = request.POST["Company"]

            cursor.execute("""      SELECT S.symbol
                                    FROM Stock S
                                    WHERE S.symbol = %s; 
                                   """, [new_Symbol])
            symbol = dictfetchall(cursor)
            if len(symbol) == 0:
                errorS = True

            cursor.execute("""      SELECT S.id
                                                    FROM Investor S
                                                    WHERE S.ID = %s; 
                                                   """, [new_ID])
            ide = dictfetchall(cursor)
            if len(ide) == 0:
                errorID = True
            if not errorS and not errorID:
                cursor.execute("""      SELECT TOP 1 S.price
                                                            FROM Stock S
                                                            WHERE S.symbol = %s
                                                            ORDER BY S.tdate DESC; 
                                                           """, [new_Symbol])
                price = float(dictfetchall(cursor)[0]['price'])
                cursor.execute("""      SELECT S.id
                                        FROM Investor S
                                        WHERE S.ID = %s AND S.AvailableCash >= %s; 
                                        """, [new_ID, new_Quantity * price])
                cash = dictfetchall(cursor)
                if len(cash) == 0:
                    errorC = True

                cursor.execute("""      SELECT S.id, S.tdate
                                            FROM Buying S
                                            WHERE S.ID = %s AND S.tDate = %s AND S.symbol = %s;
                                                    """, [new_ID, datetime.today().strftime('%Y-%m-%d'), new_Symbol])
                if len(dictfetchall(cursor)) != 0:
                    errorT = True
                if not errorS and not errorID and not errorT and not errorC:
                    cursor.execute("""      SELECT S.tdate
                                                FROM Stock S
                                                WHERE S.symbol = %s AND S.tDate = %s;
                                                """, [new_Symbol, datetime.today().strftime('%Y-%m-%d')])
                    if len(dictfetchall(cursor)) == 0:
                        cursor.execute("""      INSERT INTO Stock (Symbol, tDate, Price)
                                                    VALUES (%s, %s, %s);
                                                    """, [new_Symbol, datetime.today().strftime('%Y-%m-%d'), price])
                    cursor.execute("""      INSERT INTO Buying (tDate, ID, Symbol, BQuantity)
                                                                    VALUES (%s, %s, %s, %s);
                                                                    """,
                                   [datetime.today().strftime('%Y-%m-%d'), new_ID, new_Symbol, new_Quantity])
                    cursor.execute("""      UPDATE Investor SET AvailableCash= AvailableCash - %s WHERE ID=%s;
                                                                    """, [new_Quantity * price, new_ID])
    return render(request, 'Buy.html', {'sql_res1': sql_res1, 'errorS': errorS, 'errorC': errorC
        , 'errorID': errorID, 'errorT': errorT})


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
