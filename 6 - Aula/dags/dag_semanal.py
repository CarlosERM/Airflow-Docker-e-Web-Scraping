# Aluno: Carlos Eduardo Rocha Miranda
# Professor: Jesmmer.
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# (cron presets): para executar uma vez por semana.

dag_semanal = DAG(dag_id="dag_semanal",
                  description="Roda uma vez por semana",
                  start_date=datetime(2023, 1, 1),
                  catchup=True,
                  schedule_interval='@weekly')


def nascer():
    print("Nascer.")


def estudar():
    print("Estudar.")


def trabalhar():
    print("Trabalhar")


def casar():
    print("Casar.")


def filhos():
    print("Filhos.")


def morrer():
    print("Morrer")


t1 = PythonOperator(
    task_id="nascer",
    python_callable=nascer,
    dag=dag_semanal
)

t2 = PythonOperator(
    task_id="estudar",
    python_callable=estudar,
    dag=dag_semanal
)

t3 = PythonOperator(
    task_id="trabalhar",
    python_callable=trabalhar,
    dag=dag_semanal
)

t4 = PythonOperator(
    task_id="casar",
    python_callable=casar,
    dag=dag_semanal
)

t5 = PythonOperator(
    task_id="filhos",
    python_callable=filhos,
    dag=dag_semanal
)

t6 = PythonOperator(
    task_id="morrer",
    python_callable=morrer,
    dag=dag_semanal
)


t1 >> t2 >> t3 >> t4 >> t5 >> t6
