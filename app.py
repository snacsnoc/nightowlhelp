# TODO: check that worker2.py is running

from rq import Queue
from rq.job import Job
from rq.registry import ScheduledJobRegistry

from worker2 import conn
from send_sms import add_to_sms



from flask import Flask, render_template, request, redirect

# for enqueue time deltas
from datetime import timedelta


q = Queue(connection=conn)


app = Flask(__name__)


@app.route("/results/<job_key>", methods=["GET"])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    registry = ScheduledJobRegistry(queue=q)

    if job in registry:  # Outputs True as job is placed in ScheduledJobRegistry
        return (
            "job is in queue, be patient! <a href=/delete/" + job_key + ">delete</a>",
            200,
        )

    if job.is_finished:
        return "job is finished!", 200
    else:
        return "job haven't been run!", 202



@app.route("/delete/<job_key>", methods=["GET"])
def get_delete(job_key):

    # This deletes the job but the data still remains in Redis
    job = Job.fetch(job_key, connection=conn)

    if job.delete():
        return "cancel good!", 200
    else:
        return "not good", 202


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    if request.method == "POST":
        if "phone_number" in request.form:

            # TODO: phone number validation
            # TODO: check if phone number in queue
            phone_number = request.form["phone_number"]

            # delay in seconds from form
            delay = int(request.form["delay"])

            # maximum seconds
            max_value = 500000

            if delay < 1 or delay > max_value:
                print("this is good!")
            else:
                print("this should not run")

            # Check that the phone number doesn't exist, we want to limit text messages to one per phone number
            sched = ScheduledJobRegistry("default", connection=conn)
            # Get all scheduled, not running, job ids
            sched_job_ids = sched.get_job_ids()
            for a in sched_job_ids:
                jj = q.fetch_job(a)

                # This is very hacky but it works
                # We can get the job function arguments as a string and check if our phone number exists
                #
                # <Job 27123e4c-154b-4105-b200-38e70d5323ff: app.add_to_sms('5558675309')>
                if phone_number in str(jj):
                    print("has scheduled sms!!")
                else:
                    print("this is good!")

            job = q.enqueue_in(
                timedelta(seconds=delay), add_to_sms, args=(phone_number,)
            )

            print(job.get_id())
            if job.get_id():
                return redirect("/results/" + job.get_id(), code=302)
            else:
                return "no job, error!", 202
    # Everything else, return the template
    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run()
