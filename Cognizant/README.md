# DIO
DIO Projects

#Cognizant EMR

The MRJob package takes a long time to run a step, so I had to create a pool cluster with long idle time.
This pool cluster creation was defined in the mrjob.conf file.
Because of this long time to execute, I used the spot instances in the cluster to save money.

##Running
Run the file using the following parameters:
-r emr s3://<Your bucket>/data/sherlock.txt --output-dir=s3://<Your bucket>/output/logs
--cloud-tmp-dir=s3://<Your bucket>/temp/

set the environment variable MRJOB_CONF=./mrjob.conf (or where is your configuration file)

## Output files

The first execution was just to count the words. The output files: 
- part-00000
- part-00001
- part-00002

The second one was to put the words sorted by the number of occurrences. The output file:
- part-00000 (1)

We can see that the word 'the' is the most frequent word with 5815 occurrences.
