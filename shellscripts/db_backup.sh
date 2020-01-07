#/bin/sh

db_service_name=$1

mysql_backup ()

  {
    echo "MySQL backup has completed succesfully"
  }

mssql_backup ()

  {
    echo "MSSQL backup has completed succesfully"
  
  }

mongo_backup ()

    {
      echo "Mongo backup has completed succesfully"
    
    }
oracle_backup ()

    {
      echo "Oracle backup has completed succesfully"
        
    }

case $db_service_name in

    mysql) mysql_backup

    ;;

    mssql) mssql_backup

    ;;

    mongodb) mongo_backup

    ;;

    oracle_backup) oracle_backup

    ;;

    *) echo "Invalid choice!"; exit 1 ;;
esac
