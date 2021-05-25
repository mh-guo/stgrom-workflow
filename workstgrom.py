import json, os, sys, glob

# from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from airflow.exceptions import AirflowSkipException, AirflowFailException

# from dpdispatcher.lazy_local_context import LazyLocalContext
from dpdispatcher.submission import Submission, Job, Task, Resources
from dpdispatcher.batch_object import BatchObject
# from dpdispatcher.pbs import PBS
# from functions import NPT_end_func
# sys.path.append("/home/fengbo/dpti-1-yfb-Sn/")
from dpti import equi, hti, hti_liq, ti
import subprocess as sp

#sys.path.append("/home/minghao/stgrom/")
#from stgrom import SUN_MASS
#print(SUN_MASS)
import stgrom
from stgrom import EOS_DATA, SUN_MASS, TSDensity, TSPoints, STGHandler

# def get_dag_work_dir(context):
#     dag_run = context['params']
#     work_base_dir = dag_run['work_base_dir']
#     target_temp = int(dag_run['target_temp'])
#     target_press = int(dag_run['target_press'])
#     conf_lmp = str(dag_run['conf_lmp'])
#     ti_path = str(dag_run['ti_path'])

#     dag_work_dirname=str(target_temp)+'K-'+str(target_press)+'bar-'+str(conf_lmp)

#     work_base_abs_dir = os.path.realpath(work_base_dir)

#     dag_work_dir=os.path.join(work_base_abs_dir, dag_work_dirname)
#     return dag_work_dir
def get_empty_submission(job_work_dir):
    context = get_current_context()
    dag_run = context['params']
    work_base_dir = dag_run['work_base_dir']

    with open(os.path.join(work_base_dir, 'machine.json'), 'r') as f:
        mdata = json.load(f)
    batch_dict = mdata['batch']
    resources_dict = mdata['resources']
    batch = BatchObject(jdata=batch_dict)
    resources = Resources(**resources_dict)

    submission = Submission(
        work_base=job_work_dir, 
        resources=resources, 
        batch=batch, 
    )
    return submission


@task()
def STG_all_start_check():
    context = get_current_context()
    print(context)

    dag_run = context['params']
    work_base_dir = dag_run['work_base_dir']
    target_temp = int(dag_run['target_temp'])
    target_pres = int(dag_run['target_pres'])
    conf_lmp = str(dag_run['conf_lmp'])
    ti_path = str(dag_run['ti_path'])
    ens = str(dag_run['ens'])
    if_liquid = dag_run['if_liquid']

    work_base_abs_dir = os.path.realpath(work_base_dir)

    dag_work_dir=os.path.join(work_base_abs_dir, 'dag')

    start_info = dict(work_base_dir=work_base_dir, 
        target_temp=target_temp,
        target_pres=target_pres, 
        conf_lmp=conf_lmp, 
        ti_path=ti_path,
        ens=ens, 
        if_liquid=if_liquid, 
        work_base_abs_dir=work_base_abs_dir,
        dag_work_dir=dag_work_dir)
    print('start_info:', start_info)
    return start_info


@task()
def STG_start(start_info):
    print(start_info)
    work_base_abs_dir = start_info['work_base_abs_dir']
    dag_work_dir = start_info['dag_work_dir']
    
    cwd = os.getcwd()
    os.chdir(work_base_abs_dir)
    if os.path.isdir(dag_work_dir) is False:
            os.mkdir(dag_work_dir)
    for i in range(100):
        job_work_dir = os.path.join(dag_work_dir,'new_job.%03d'%i)#, 'STG_gen''new_job'
        if os.path.isdir(job_work_dir) is False:
            os.mkdir(job_work_dir)
            break
    #equi.make_task(job_work_dir, task_jdata)
    os.chdir(cwd)
    os.chdir(job_work_dir)
    #os.chdir(job_work_dir)
    os.system('ln -s '+work_base_abs_dir+'/generate_raw.py '+job_work_dir)
    #job_work_dir=work_base_abs_dir
    return job_work_dir

@task()
def STG_gen_init(job_work_dir):
    os.chdir(job_work_dir)
    job_file_dir = os.path.join(job_work_dir,'Task')#, 'STG_gen''new_job'
    if os.path.isdir(job_file_dir) is False:
        os.mkdir(job_file_dir)
    return job_work_dir

@task()
def STG_gen(job_work_dir):
    os.chdir(job_work_dir)
    #task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP4 >> "Task_AP4_log.out"', task_work_path='./')
    #task = Task(command='conda activate airflow && python -u generate_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    submission = get_empty_submission(job_work_dir)
    submission.register_task_list([task])
    submission.run_submission()
    return job_work_dir

@task()
def STG_gen_AP3(job_work_dir):
    #task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP4 >> "Task_AP4_log.out"', task_work_path='./')
    #task = Task(command='conda activate airflow && python -u generate_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP3 ', task_work_path='./')
    submission = get_empty_submission(job_work_dir)
    submission.register_task_list([task])
    submission.run_submission()
    return job_work_dir

@task()
def STG_cor_init(job_work_dir,start_info):
    work_base_abs_dir = start_info['work_base_abs_dir']
    os.chdir(job_work_dir)
    os.system('ln -s '+work_base_abs_dir+'/correct_raw.py '+job_work_dir)
    job_file_dir = os.path.join(job_work_dir,'Cor')#, 'STG_gen''new_job'
    if os.path.isdir(job_file_dir) is False:
        os.mkdir(job_file_dir)
    return job_work_dir


@task()
def STG_cor(job_work_dir,geninfo):
    #task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP4 >> "Task_AP4_log.out"', task_work_path='./')
    #task = Task(command='conda activate airflow && python -u generate_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    print(geninfo)
    task = Task(command='python -u correct_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    submission = get_empty_submission(job_work_dir)
    submission.register_task_list([task])
    submission.run_submission()
    return job_work_dir


@task()
def STG_ex_init(job_work_dir,start_info):
    work_base_abs_dir = start_info['work_base_abs_dir']
    os.chdir(job_work_dir)
    os.system('ln -s '+work_base_abs_dir+'/ex_raw.py '+job_work_dir)
    job_file_dir = os.path.join(job_work_dir,'Ex')#, 'STG_gen''new_job'
    if os.path.isdir(job_file_dir) is False:
        os.mkdir(job_file_dir)
    return job_work_dir

@task()
def STG_ex(job_work_dir):
    #task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP4 >> "Task_AP4_log.out"', task_work_path='./')
    #task = Task(command='conda activate airflow && python -u generate_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    task = Task(command='python -u ex_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    submission = get_empty_submission(job_work_dir)
    submission.register_task_list([task])
    submission.run_submission()
    return job_work_dir

@task()
def STG_rom_init(job_work_dir,start_info):
    work_base_abs_dir = start_info['work_base_abs_dir']
    os.chdir(job_work_dir)
    os.system('ln -s '+work_base_abs_dir+'/rom_raw.py '+job_work_dir)
    job_file_dir = os.path.join(job_work_dir,'Rom')#, 'STG_gen''new_job'
    if os.path.isdir(job_file_dir) is False:
        os.mkdir(job_file_dir)
    return job_work_dir

@task()
def STG_rom(job_work_dir):
    #task = Task(command='python -u generate_raw.py --label=Task --EOS-name=AP4 >> "Task_AP4_log.out"', task_work_path='./')
    #task = Task(command='conda activate airflow && python -u generate_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    task = Task(command='python -u rom_raw.py --label=Task --EOS-name=AP4 ', task_work_path='./')
    submission = get_empty_submission(job_work_dir)
    submission.register_task_list([task])
    submission.run_submission()
    return job_work_dir

default_args = {
    'owner': 'minghao',
    'start_date': datetime(2020, 1, 1, 8, 00)
}


@dag(default_args=default_args, schedule_interval=None, start_date=datetime(2021, 1, 1, 10, 00))
def STG_taskflow():
    #start_info = all_start_check()

    start_info = STG_all_start_check()

    start_mark=STG_start(start_info)


    STG_geninfo=STG_gen(STG_gen_init(start_mark))

    STG_corinfo=STG_cor(STG_cor_init(STG_geninfo,start_info),STG_geninfo)

    STG_exinfo=STG_ex(STG_ex_init(STG_corinfo,start_info))

    STG_rominfo=STG_rom(STG_rom_init(STG_exinfo,start_info))

    STG_endinfo=STG_rominfo

    return STG_endinfo


# HTI_dag = HTI_taskflow()
STG_dag = STG_taskflow()
