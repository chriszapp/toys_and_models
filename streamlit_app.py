import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
#connection to mysql
connection = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.178.25.157', port = '23456', database = 'toys_and_models', use_pure = True)
#put your querys here and name them "query_FQ1" if it is finances quest 1
query_FQ2 = '''Select o.customernumber, o.orderdate, o.ordernumber, sum((od.quantityordered * od.priceeach)) as Order_Value
from orders o
join orderdetails od
	on o.ordernumber = od.ordernumber
group by o.ordernumber
having sum((od.quantityordered * od.priceeach)) not in (select p.amount
from payments p)'''
query_FQ1 = '''WITH my_table AS (
    SELECT SUM(od.quantityOrdered * od.priceEach) AS turnover,
           YEAR(o.orderDate) AS Year,
           country
    FROM products AS p
    JOIN orderdetails AS od ON p.productCode = od.productCode
    JOIN orders AS o ON o.orderNumber = od.orderNumber
    JOIN customers AS c ON o.customerNumber = c.customerNumber 
    WHERE o.orderDate >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)
    GROUP BY Year, country
    ORDER BY country
)

SELECT mt.turnover, 
       mt.Year, 
       mt.country
FROM my_table AS mt
ORDER BY mt.country;'''
#define your databases here, follow the same logic, df_FQ1, for example
df_FQ2 = pd.read_sql_query(query_FQ2, con = connection)
df_FQ1 = pd.read_sql_query(query_FQ1, con = connection)
#dont touch these
with st.sidebar:
    p = st.button("Presentation")
    S = st.button("Sales")
    F = st.button("Finance")
    L = st.button("Logistics")
    HR = st.button("Human Resources")
#uncomment your if after you paste the code and make sure it works
#if p:
#if S:
if F:
   st.header("Finances Quest 1")
   st.subheader("The turnover of the orders of the last two months by country")
   df_FQ1
   st.header("Finances Quest 2")
   st.subheader("Orders that have not yet been paid")
   df_FQ2
#if L: