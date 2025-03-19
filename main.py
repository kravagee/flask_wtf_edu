global_init(input())

session = create_session()

for jobs in session.query(Jobs).filter(Jobs.work_size < 20, Jobs.is_finished == 0).all():
    print(jobs)

session.close()
