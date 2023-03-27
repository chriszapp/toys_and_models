import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy as sql
connection = 'mysql://toyscie:WILD4Rdata!@51.178.25.157:23456/toys_and_models'
sql_engine = sql.create_engine(connection)
query_LQ1 = '''SELECT p.productName, sum(p.quantityInStock) as total_stock
FROM orderdetails od
    JOIN products p
      ON od.productcode = p.productcode
    GROUP BY p.productCode
    ORDER BY sum(od.quantityOrdered) DESC
    LIMIT 5;'''
df_lq1 = pd.read_sql_query(query_LQ1, sql_engine)


st.write('hello')
df_lq1
