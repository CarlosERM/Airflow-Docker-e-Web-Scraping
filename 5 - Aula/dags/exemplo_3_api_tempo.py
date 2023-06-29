from airflow import DAG
from airflow.operators.empty import EmptyOperator
import airflow.utils.dates


dag = DAG(dag_id="exemplo_3_api_tempo",
          description="Exemplo de uma pipeline utilizando inteligência artificial.",
          start_date=airflow.utils.dates.days_ago(5),
          schedule_interval="@daily")

buscar_previsao_do_tempo = EmptyOperator(
    task_id="buscar_previsao_do_tempo", dag=dag)

buscar_dados_de_vendas = EmptyOperator(
    task_id="buscar_dados_de_vendas", dag=dag)

limpar_dados_de_previsao = EmptyOperator(
    task_id="limpar_dados_de_previsao", dag=dag)

limpar_dados_de_vendas = EmptyOperator(
    task_id="limpar_dados_de_vendas", dag=dag)

juntar_datasets = EmptyOperator(
    task_id="juntar_datasets", dag=dag)

treinar_modelo_IA = EmptyOperator(
    task_id="treinar_modelo_IA", dag=dag)

implantar_modelo_IA = EmptyOperator(
    task_id="implantar_modelo_IA", dag=dag)

buscar_previsao_do_tempo >> limpar_dados_de_previsao
buscar_dados_de_vendas >> limpar_dados_de_vendas
[limpar_dados_de_previsao, limpar_dados_de_vendas] >> juntar_datasets
juntar_datasets >> treinar_modelo_IA >> implantar_modelo_IA
