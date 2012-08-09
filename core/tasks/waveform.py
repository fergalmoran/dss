from celery.task import task
from core.utils.waveform import generate_waveform

@task(name='dss.create_waveform_task')
def create_waveform_task(in_file, out_file):
    generate_waveform(in_file, out_file)


