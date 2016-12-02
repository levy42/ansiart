#!/bin/sh

if [ !$1 ]; then
    echo "deploy|start|stop|restart"
fi

if [ "$1" == "deploy" ]; then
    pip install -r requirements.txt

    if [-f /tmp/ansiart.pid]
    then
        pid=$(</tmp/ansiart.pid)
        kill "$pid"
    fi

    python app.py &
    echo $! > /tmp/ansiart.pid

    python manage.py initdb
fi

if [ "$1" == "start" ]; then
    python app.py &
    echo $! > /tmp/ansiart.pid

    python manage.py initdb
fi

if [ "$1" == "restart" ]; then
    if [-f /tmp/ansiart.pid]
    then
        pid=$(</tmp/ansiart.pid)
        kill "$pid"
    fi
    python app.py &
    echo $! > /tmp/ansiart.pid

    python manage.py initdb
fi

if [ "$1" == "stop" ]; then
    if [ -f /tmp/ansiart.pid ]
    then
        pid=$(</tmp/ansiart.pid)
        kill "$pid"
    fi
fi


