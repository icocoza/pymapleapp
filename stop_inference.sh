pid=`ps aux | grep posco | grep -v grep | awk '{print $2}'`
if [ -n "$pid" ]; then
kill -9 $pid
fi