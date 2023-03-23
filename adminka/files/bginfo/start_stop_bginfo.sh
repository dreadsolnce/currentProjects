#!/bin/bash

 # Запускаем основной файл bginfo, для того чтобы узнать есть ли у нас изменения в кофигурационных файлах (зависит от кода з-авершения программы bginfo, если 0 - то изменений нет, если 1 - то есть изменения) и если есть то перерисовываем экран.
 /bin/bash /usr/local/bin/bginfo.bg; echo $?
while true
do
 if [[ $? == 0 ]];then
  number_proc_bginfo=$(ps -efH | grep /bin/bash | grep /usr/local/bin/bginfo.bg | grep `logname`" " | awk '{print $2}')
  echo "Номер равен="$number_proc_bginfo
  if [ ! -z "${number_proc_bginfo}" ]; then
   kill $number_proc_bginfo
  fi
  sleep 5
  # number_proc_root_tail=$(ps -efH | grep bg1.tmp | grep root-tail | awk '{print $2}')
  # kill $number_proc_root_tail

  /bin/bash /usr/local/bin/bginfo.bg
  sleep 5
 fi
done
