:: 1. Start the experiment
chaos run --var-file config.json experiment.json
:: 2. Create a new ADB cluster and reset the job to use the new cluster
python create_cluster_reset_job.py
:: 3. Check the message number in the queue
python queue_status.py
:: 4. wait for the experiment to finish and see the result