import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
import logging
from airflow.operators.python import PythonOperator


# create_pet_table, populate_pet_table, get_all_pets, and get_birth_date are examples of tasks created by
# instantiating the Postgres Operator

def get_birth_date(sql):
    pg_hook = PostgresHook.get_hook('postgres_default')
    logging.info(
        "Exportando o resultado da consulta para /opt/airflow/consultas/pet.csv")
    pg_hook.copy_expert(
        sql, filename="/opt/airflow/consultas/pet.csv")

def get_all_pets(sql):
    pg_hook = PostgresHook.get_hook('postgres_default')
    logging.info(
        "Exportando o resultado da consulta para /opt/airflow/consultas/pet.csv")
    pg_hook.copy_expert(
        sql, filename="/opt/airflow/consultas/all_pets.csv")
def get_lily_pet(sql):
    pg_hook = PostgresHook.get_hook('postgres_default')
    logging.info(
        "Exportando o resultado da consulta para /opt/airflow/consultas/pet.csv")
    pg_hook.copy_expert(
        sql, filename="/opt/airflow/consultas/lily_pets.csv")
    

with DAG(
    dag_id="postgres_operator_dag",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
    template_searchpath='/opt/airflow/sql',
) as dag:

    create_pet_table = PostgresOperator(
        task_id="create_pet_table",
        postgres_conn_id='postgres_default',
        sql='pet_schema.sql',
    )

    populate_pet_table = PostgresOperator(
        task_id="populate_pet_table",
        postgres_conn_id='postgres_default',
        sql='pet_populate.sql',
    )
    # get_all_pets = PostgresOperator(
    #     task_id="get_all_pets",
    #     postgres_conn_id='postgres_default',
    #     sql='select_pet.sql'
    # )

    get_birth_date = PythonOperator(
        task_id="get_birth_date",
        python_callable=get_birth_date,
        op_kwargs={"sql": "COPY (SELECT * FROM pet WHERE birth_date BETWEEN SYMMETRIC '2020-01-01' AND '2020-12-31') TO STDOUT WITH CSV HEADER"}
    )
    """
        A operação de SELECT não funciona no PostgresOperator porque o Airflow não foi construído para transferir
        dados de uma tarefa para outra(é possível fazer isso), e sim para orquestrar processos. 
    """

    get_all_pets = PythonOperator(
        task_id="get_all_pets",
        python_callable=get_all_pets,
        op_kwargs={"sql": "COPY (SELECT * FROM pet)  TO STDOUT WITH CSV HEADER"}
    )

    get_lily_pets = PythonOperator(
        task_id="get_lily_pets",
        python_callable=get_lily_pet,
        op_kwargs={"sql": "COPY (SELECT * FROM pet where OWNER='Lily') TO STDOUT WITH CSV HEADER"}
    )

    create_pet_table >> populate_pet_table >> get_birth_date >> get_all_pets >> get_lily_pets