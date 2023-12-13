### LOCAL FILE SYSTEM ###


           pwd
           ls
        mkdir
        cp
        mv
        Rm
            Cat
            Create new file and show cat command
            clear




### LISTING ROOT DIRECTORY ###


hadoop fs -ls /


### LISTING DEFAULT TO HOME DIRECTORY ###


hadoop fs -ls


hadoop fs -ls /user/hirwuser150430


### CREATE A DIRECTORY IN HDFS ###


hadoop fs -mkdir hadoop-test1


### COPY FROM LOCAL FS TO HDFS ###


hadoop fs -copyFromLocal  /hirw-starterkit/hdfs/commands/dwp-payments-april10.csv hadoop-test1


### COPY TO HDFS TO LOCAL FS ###


hadoop fs -copyToLocal hadoop-test1/dwp-payments-april10.csv .


hadoop fs -ls hadoop-test1


### CREATE 2 MORE DIRECTORIES ###


hadoop fs -mkdir hadoop-test2


hadoop fs -mkdir hadoop-test3


### COPY A FILE FROM ONE FOLDER TO ANOTHER ###


hadoop fs -cp hadoop-test1/dwp-payments-april10.csv hadoop-test2


### MOVE A FILE FROM ONE FOLDER TO ANOTHER ###


hadoop fs -mv hadoop-test1/dwp-payments-april10.csv hadoop-test3


### CHECK REPLICATION ###


hadoop fs -ls hadoop-test3


### CHANGE OR SET REPLICATION FACTOR ###


hadoop fs -Ddfs.replication=2 -cp hadoop-test2/dwp-payments-april10.csv hadoop-test2/test_with_rep2.csv


hadoop fs -ls hadoop-test2


hadoop fs -ls hadoop-test2/test_with_rep2.csv


### CHANGING PERMISSIONS ###


hadoop fs -chmod 777 hadoop-test2/test_with_rep2.csv




### DELETE DIR/FILES IN HDFS ###


hadoop fs -rm hadoop-test2/test_with_rep5.csv


hadoop fs -rm -r hadoop-test1
hadoop fs -rm -r hadoop-test2
hadoop fs -rm -r hadoop-test3