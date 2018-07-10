#!/bin/bash

home_cpmetrix=~/cpmetrix
PerfData="/usr/local/nagios/share/perfdata"

echo " ---> Started: `date +%d-%m-%Y_%H:%M:%S`"

if [ ! -e $home_cpmetrix ];then
	mkdir $home_cpmetrix;
fi

cd $PerfData 2> /dev/null

if [ $PerfData != `pwd` ];then
	echo "`date +%d-%m-%Y_%H:%M:%S` - Nao conseguiu acessar o diretorio : $PerfData";exit
fi

if [ ! -e "$home_cpmetrix/json_files" ];then
        mkdir "$home_cpmetrix/json_files";
fi

rm -f $home_cpmetrix/json_files/*json
rm -f $home_cpmetrix/csv_files/*csv

CapacityScript="/usr/local/nagiosxi/html/includes/components/capacityplanning/backend/capacityplanning.py"
HostList=`find . -type d -not -path '*/\.*' -not -path '\.'|sed 's/\.\///g'|sort`
IndexList="$home_cpmetrix/indexlist.tmp"

>$IndexList

for x in $HostList;do
	grep -H "<LABEL>" $x/*.xml|sed 's/\.xml//g'|sed 's/<[^>]\+>//g'|tr -d " " >> $IndexList;
done

echo " ---> Step 1 - Extract Data to Json Files - Started: `date +%d-%m-%Y_%H:%M:%S`"

count=1
if [ -e $IndexList ];then
	Total_Services=`cat $IndexList|wc -l`
	for y in `cat $IndexList`;do
		Host=`echo $y|cut -d"/" -f1`
		Service=`echo $y|cut -d"/" -f2|cut -d":" -f1`
		Label=`echo $y|cut -d":" -f2`
		if [[ $Label = *"/"* ]];then
			LabelEscape=`echo $Label|sed 's/[[:punct:]]/_/g'`
		else
			LabelEscape=$Label
		fi
		FileOutput="$home_cpmetrix/json_files/$Host-$Service-$LabelEscape-HoltWinters-1Month.json"
		echo " -> $count/$Total_Services -> $FileOutput"
		$CapacityScript -H "$Host" -S "$Service" -T "$LabelEscape" -M "Holt-Winters" -P "1 Month" --json-indent=2 > $FileOutput 
		count=$((count+1))
	done
fi

echo " ---> Step 1 - Extract Data to Json Files - Completed: `date +%d-%m-%Y_%H:%M:%S`"
echo " ---> Step 2 - Convert Json to Text Data - Started: `date +%d-%m-%Y_%H:%M:%S`"

csv_files=$home_cpmetrix/csv_files
if [ ! -e "$csv_files" ];then mkdir $csv_files;fi

count=1
for j in $home_cpmetrix/json_files/*.json;do
	csv_file="`ls $j|xargs -n 1 basename|sed 's/\.json//g'`.csv"
	if [ `cat $j|wc -l` -gt "2" ];then
		echo " -> $count/$Total_Services -> $csv_files/$csv_file"
		$home_cpmetrix/./json2csv.py -f $j > $csv_files/$csv_file
	else
		echo " -> $count -> !!! Empty File : $j"
	fi
	count=$((count+1))
done

echo " ---> Step 2 - Convert Json to Text Data - Completed: `date +%d-%m-%Y_%H:%M:%S`"
