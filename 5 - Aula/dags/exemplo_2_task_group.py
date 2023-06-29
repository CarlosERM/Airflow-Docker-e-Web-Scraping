from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

dag = DAG(dag_id="exemplo_2_task_group", description="Exemplo de dag com Task Group",
          start_date=datetime(2023, 3, 4), schedule_interval="@daily")

start = EmptyOperator(task_id="START", dag=dag)

with TaskGroup(group_id="A-C", tooltip="Task group com A, A1, B e C", dag=dag) as gr_1:
    a = EmptyOperator(task_id="Task_A", dag=dag)
    a1 = EmptyOperator(task_id="Task_A1", dag=dag)
    b = EmptyOperator(task_id="Task_B", dag=dag)
    c = EmptyOperator(task_id="Task_C", dag=dag)
    b >> c
d = EmptyOperator(task_id="Task_D", dag=dag)
e = EmptyOperator(task_id="Task_E", dag=dag)
f = EmptyOperator(task_id="Task_F", dag=dag)
g = EmptyOperator(task_id="Task_G", dag=dag)
end = EmptyOperator(task_id="END", dag=dag)

start >> gr_1 >> d >> e >> f >> g >> end
