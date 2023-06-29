# Aluno: Carlos Eduardo Rocha Miranda
# Professor: Jesmmer.
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.timetables.trigger import CronTriggerTimetable


# (cron expressions): para executar executar toda terça feira, 12:45, a cada dois meses;

dag_cron = DAG(dag_id="dag_cron",
               description="Roda toda terça feira, 12:45, a cada dois meses",
               start_date=datetime(2022, 1, 1),
               catchup=True,
               # Minuto(0 - 59) Hora(0 - 23) Dia do mês(1 - 31) Mês(1 - 12) Dia da Semana(0 - 6)(Domingo até o Sábado)
               timetable=CronTriggerTimetable("45 12 * */2 2", timezone="UTC"))


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
    dag=dag_cron
)

t2 = PythonOperator(
    task_id="estudar",
    python_callable=estudar,
    dag=dag_cron
)

t3 = PythonOperator(
    task_id="trabalhar",
    python_callable=trabalhar,
    dag=dag_cron
)

t4 = PythonOperator(
    task_id="casar",
    python_callable=casar,
    dag=dag_cron
)

t5 = PythonOperator(
    task_id="filhos",
    python_callable=filhos,
    dag=dag_cron
)

t6 = PythonOperator(
    task_id="morrer",
    python_callable=morrer,
    dag=dag_cron
)


t1 >> t2 >> t3 >> t4 >> t5 >> t6
