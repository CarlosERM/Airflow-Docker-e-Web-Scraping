import logging
from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator


def extrair_dados_consulta(copy_sql):
    pg_hook = PostgresHook.get_hook('postgres_default')
    logging.info(
        "Exportando o resultado da consulta para /opt/airflow/consultas/customer.csv")
    pg_hook.copy_expert(
        copy_sql, filename="/opt/airflow/consultas/tb_cliente.csv")


with DAG('exemplo_3_sql',
         start_date=datetime(2023, 4, 6),
         schedule_interval="@once",
         catchup=False,
         template_searchpath='/opt/airflow/sql') as dag:

    cria_tabela = PostgresOperator(
        task_id='criar_tabela',
        postgres_conn_id='postgres_default',
        sql='criar_tabela.sql'
    )

    insere_dados = PostgresOperator(
        task_id='inserir_dados',
        postgres_conn_id='postgres_default',
        sql='inserir_dados.sql',
        params={'p_nome': "'Joaquim Silva'"}
    )
    consulta_dados = PythonOperator(
        task_id="extrair_dados",
        python_callable=extrair_dados_consulta,
        op_kwargs={
            "copy_sql": "COPY (SELECT * FROM tb_cliente) TO STDOUT WITH CSV HEADER"
        }
    )

cria_tabela >> insere_dados >> consulta_dados
