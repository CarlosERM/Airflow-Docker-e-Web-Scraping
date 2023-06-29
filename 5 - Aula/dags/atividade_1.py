from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

dag = DAG(dag_id="atividade_1", description="Primeira atividade do Jesmmer",
          start_date=datetime(2023, 3, 4), schedule_interval="@daily")
'''
Definição da Dag. 
Aqui especificamos o nome da dag, sua descrição, quando ela vai começar a rodar e o seu intervalo.
'''

start = EmptyOperator(task_id="start", dag=dag)
'''
Definição da task start. 
Nela, assim como em todas nesse exemplo, é utilizado um EmptyOperator que não faz nada além de
desenhar uma task com nome na interface do Airflow.
Uma task é uma instância de um Operador. Um operador é como uma classe que possui as 
definições necessárias para que uma task funcione.
'''

with TaskGroup(group_id="taskgroup_1", dag=dag) as taskgroup_1:
    op_1 = EmptyOperator(task_id="op-1", dag=dag)
    op_2 = EmptyOperator(task_id="op-2", dag=dag)
'''
Definição de um Task Group chamado taskgroup_1. 
Um Task Group é um grupo de tarefas. Todas as tarefas dentro de um Task Group aparecerão agrupadas na interface do Airflow. 
Todas as tasks aqui serão rodadas em paralelo, a não ser que seja especificado outro tipo de fluxo.
'''

some_other_task = EmptyOperator(task_id="some-other-task", dag=dag)

'''
Definição de uma task chamada some-other-task. 
É mais uma task que utliza um EmptyOperator que não faz nada.
'''

with TaskGroup(group_id="taskgroup_2", dag=dag) as taskgroup_2:
    op_3 = EmptyOperator(task_id="op-3", dag=dag)
    op_4 = EmptyOperator(task_id="op-4", dag=dag)

'''
Definição de um Task Group chamado taskgroup_2. 
É só mais um Task Group. Possui as tasks op-3 e op-4.
'''

end = EmptyOperator(task_id="end", dag=dag)
'''
Definição de uma task chamada end. 
É a última task dessa dag.
'''
start >> taskgroup_1 >> some_other_task >> taskgroup_2 >> end
'''
Aqui é definido a ordem do fluxo dessa dag.
'''
