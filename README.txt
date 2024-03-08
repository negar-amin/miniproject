please make sure you are connected to internet and docker engine is installed on your system then follow bellow steps it's recommended to turn your vpn on.
steps marked with * are critical for further steps to be done successfully so make sure * steps to be done without any error please do not interrupt them with ctrl+c.

*1)first open docker desktop then open terminal in miniproject folder and run docker compose up

*2)open new terminal (not matter in which directory you open it) run docker exec -it my_ubuntu_container bash
then run cd /codes

*3)run ./requirements.sh 
if it doesn't work run sed -i -e 's/\r$//' requirements.sh and then try again
it takes several minutes to complete please be patient and allow it to completely run  and allow all permisions by typeing y in terminal (this step is critical and must be done without error)
after previous script done compeletely  run sed -i -e 's/\r$//' script.sh

*4)run crontab -e
go to end of file
write * * * * * /codes/script.sh
then press ctrl+s and ctrl+x.

*5)run service cron start

6)after a minute open http://localhost:9100 on your browser you must see users_info topic click on it and refresh it every minute then you must see new data inserting to this topic every minute

*7)return to terminal you were working on run python3 consumer1_set_timestamp.py this consumer get data from topic users_info add new property named "insert_into_database_timestamp" to it and send it to new topic processed_once then come back to http://localhost:9100 on your browser you must see new topic processed_once 

*8)open new terminal run step 2 again

*9)run python3 consumer2_set_label.py this consumer get data from topic processed_once add new property named "status" to it for checking if users are hired somewhere or looking for job and send it to new topic processed_twice then come back to http://localhost:9100 on your browser you must see new topic processed_twice

*10)open new terminal run step 2 again

*11)run python3 consumer3_save_to_postgres.py this consumer get data from topic processed_twice and save it to postgres

12)for checking if it is working true open DBeaver (or install it if you don't have it on your system or use any other tools you want but set the configuration as I'm saying) from Database tab select New Database Connection select PostgreSQL then click Next set Database to dblab and port to 5434 and password to postgres123 click Test Connection then press OK and Finish. go to Connections -> dblab -> Databases -> dblab -> Schemas -> public -> Tables -> users then click on Data tab on top you can see users data all saved to postgres.

ATTENTION: FOR FULL BACK UP DATA ON POSTGRES CHECK backup_steps.txt IN miniproject FOLDER.

THANKS FOR THE TIME YOU'VE SPENT TO CHECK MY SOLUSION FOR THIS PROJECT :)))





