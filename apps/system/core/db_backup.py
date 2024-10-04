from subprocess import PIPE, Popen


from django.conf import settings

from utils.env import get_env_var


class Backup:
    def __init__(self):
        DATABASE_NAME = get_env_var("DATABASE_NAME")
        DATABASE_USER = get_env_var("DATABASE_USER")
        DATABASE_HOST = get_env_var("DATABASE_HOST")
        DATABASE_PASSWORD = get_env_var("DATABASE_PASSWORD")

        success = True

        command = (
            f"pg_dump --host={DATABASE_HOST} "
            f"--dbname={DATABASE_NAME} "
            f"--username={DATABASE_USER} "
            f"--no-password "
            f"--file=backup.dmp "
        )

        try:
            proc = Popen(command, shell=True, env={"PGPASSWORD": DATABASE_PASSWORD})
            proc.wait()
        except Exception as e:
            success = False
            print("Exception happened during dump %s" % (e))

        if success:
            print("db dump successfull")
        print(" restoring to a new database database")

        path = ""

        if not success:
            print("dump unsucessfull. retsore not possible")
        else:
            try:
                process = Popen(
                    [
                        "pg_restore",
                        "--no-owner",
                        "--dbname=postgresql://{}:{}@{}:{}/{}".format(
                            "postgres",  # db user
                            "sarath1996",  # db password
                            "localhost",  # db host
                            "5432",
                            "ReplicaDB",
                        ),  # db port ,#db name
                        "-v",
                        path,
                    ],
                    stdout=PIPE,
                )

                output = process.communicate()[0]

            except Exception as e:
                print("Exception during restore %e" % (e))
