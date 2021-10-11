if [[ -z "$1" ]]; then
  read -p "Username: " -r username
else
  username=$1
fi
PGOPTIONS="-c default_transaction_read_only=true" psql "sslmode=require hostaddr=$DB_HOST user=$username dbname=$DB_NAME" --no-psqlrc -e -L ~/.audit/$CURRENT_USER/sql_${username}_$(date --iso-8601=ns).log
