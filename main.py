from data import db_session, jobs
from data.db_session import global_init

global_init('db/mars_explorer.db')

session = db_session.create_session()

job = jobs.Jobs()

job.teamleader = 1
job.job = 'deployment of residential modules 1 and 2'
job.work_size = 15
job.collaborators = '2, 3'

session.add(job)
session.commit()
session.close()