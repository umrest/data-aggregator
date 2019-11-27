DIR=/home/pi/rest/data-aggregator
VENV=/home/pi/rest/venv

cd $DIR
source $VENV/bin/activate
while true; do
    python simple_router.py
    echo "Data Aggregator Crashed..."
done