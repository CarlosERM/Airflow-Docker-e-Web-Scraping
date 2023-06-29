# Aluno: Carlos Eduardo Rocha Miranda
# Professor: Jesmmer.
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.timetables.trigger import CronTriggerTimetable
from airflow.timetables.events import EventsTimetable
import pendulum
from airflow.operators.python import PythonOperator

dag_eventos = DAG(dag_id="dag_eventos", description="Roda às 12:00 em todo feriado do mês de Novembro de 2023.",
                  start_date=datetime(2023, 2, 1),
                  catchup=True,
                  # (timetable): para executar às 12:00 em todo feriado do mês de Novembro de 2023.
                  timetable=EventsTimetable(event_dates=[
                      pendulum.datetime(2023, 11, 2, 12, 0,
                                        tz="America/Sao_Paulo"),
                      pendulum.datetime(2023, 11, 15, 12, 0,
                                        tz="America/Sao_Paulo"),
                  ]))


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
    dag=dag_eventos
)

t2 = PythonOperator(
    task_id="estudar",
    python_callable=estudar,
    dag=dag_eventos
)

t3 = PythonOperator(
    task_id="trabalhar",
    python_callable=trabalhar,
    dag=dag_eventos
)

t4 = PythonOperator(
    task_id="casar",
    python_callable=casar,
    dag=dag_eventos
)

t5 = PythonOperator(
    task_id="filhos",
    python_callable=filhos,
    dag=dag_eventos
)

t6 = PythonOperator(
    task_id="morrer",
    python_callable=morrer,
    dag=dag_eventos
)


t1 >> t2 >> t3 >> t4 >> t5 >> t6
