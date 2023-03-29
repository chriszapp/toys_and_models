import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
#connection to mysql
connection = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.178.25.157', port = '23456', database = 'toys_and_models', use_pure = True)
#put your querys here and name them "query_FQ1" , for example
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
query_LQ1 = '''SELECT p.productName, sum(p.quantityInStock) as total_stock
FROM orderdetails od
    JOIN products p
      ON od.productcode = p.productcode
    GROUP BY p.productCode
    ORDER BY sum(od.quantityOrdered) DESC
    LIMIT 5;'''
query_human_res = '''SELECT year, month, x.sellers, monthly_turnover
FROM (SELECT year(o.OrderDate) as year,
			month(o.OrderDate) as month,
			concat(e.firstName, ' ', e.lastname) AS sellers,
            SUM(od.quantityOrdered) AS monthly_turnover,
            row_number() over (partition by year(o.OrderDate), month(o.OrderDate) order by SUM(od.quantityOrdered) desc) as seq
FROM orders as o
JOIN customers as c
ON c.customerNumber=o.customerNumber
JOIN employees as e
ON e.employeeNumber=c.salesRepEmployeeNumber
JOIN orderdetails as od
ON od.orderNumber=o.orderNumber
GROUP BY year(o.OrderDate), month(o.OrderDate), sellers
Order by year(o.OrderDate), month(o.OrderDate)) as x
where x.seq <=2;'''
#define your databases here, follow the same logic, df_FQ1, for example
df_FQ2 = pd.read_sql_query(query_FQ2, con = connection)
df_FQ1 = pd.read_sql_query(query_FQ1, con = connection)
df_LQ1 = pd.read_sql_query(query_LQ1, con = connection)
df_HR = pd.read_sql_query(query_human_res, con = connection)
df_HR['date'] = pd.to_datetime(df_HR[['year', 'month']]. assign(day=1))
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
if L:
    st.header("Logistics")
    st.subheader("The stock of the 5 most ordered products")
    st.write(df_LQ1)
    viz_L = sns.barplot(data = df_LQ1,
                        x = 'productName',
                        y = 'total_stock')
    st.pyplot(viz_L.figure)
if HR:
    st.header("Human Resources")
    st.subheader("Each month, the 2 sellers with the highest turnover")
    df_HR
    viz_HR = sns.barplot(data =( df_HR[df_HR['date'] == '2021-01-01'] ),
                         x = 'sellers',
                         y = 'monthly_turnover', dodge=True)
    st.pyplot(viz_HR.figure)