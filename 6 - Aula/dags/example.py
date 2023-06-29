# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from datetime import datetime, timedelta
# from airflow.timetables.trigger import CronTriggerTimetable
# from airflow.timetables.events import EventsTimetable
# import pendulum
# Minuto(0 - 59) Hora(0 - 23) Dia do mês(1 - 31) Mês(1 - 12) Dia da Semana(0 - 6)(Domingo até o Sábado)

# dag = DAG(dag_id="timetable_example", description="Testando o Timetable",
#           start_date=datetime(2023, 2, 1),
#           catchup=True, timetable=CronTriggerTimetable("0 1 * * 3", timezone="UTC"))  # 01:00 na Quarta-Feira

# t1 = BashOperator(
#     task_id="print_date",
#     bash_command="date",
#     dag=dag
# )


# dag = DAG(dag_id="timetable_example_2", description="Testando o Timetable",
#           start_date=datetime(2023, 2, 1),
#           catchup=True,
#           timetable=CronTriggerTimetable("0 18 * * 5", timezone="UTC", interval=timedelta(days=4, hours=9)))
# # Roda toda Sexta-Feira às 18:00 para cobrir toda a semana de trabalho (9:00 Segunda-Feira até 18:00 Sexta-Feira)
# t1 = BashOperator(
#     task_id="print_date",
#     bash_command="date",
#     dag=dag
# )

# dag = DAG(dag_id="timetable_example_3", description="Testando o Timetable",
#           start_date=datetime(2023, 2, 1),
#           catchup=True,
#           schedule=timedelta(minutes=30))
# # Roda de 30 em 30 minutos.
# t1 = BashOperator(
#     task_id="print_date",
#     bash_command="date",
#     dag=dag
# )

# dag = DAG(dag_id="timetable_example_4", description="Testando o Timetable",
#           start_date=datetime(2023, 2, 1),
#           catchup=True,
#           timetable=EventsTimetable(event_dates=[
#               pendulum.datetime(2022, 4, 5, 8, 27, tz="America/Chicago"),
#               pendulum.datetime(2022, 4, 17, 8, 27, tz="America/Chicago"),
#               pendulum.datetime(2022, 4, 22, 8, 27, tz="America/Chicago"),
#               pendulum.datetime(2022, 4, 23, 8, 27, tz="America/Chicago"),
#               pendulum.datetime(2022, 4, 25, 8, 27, tz="America/Chicago"),
#           ]))
# # Roda de 30 em 30 minutos.
# t1 = BashOperator(
#     task_id="print_date",
#     bash_command="date",
#     dag=dag
# )
