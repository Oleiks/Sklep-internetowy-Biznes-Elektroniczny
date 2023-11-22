TYPE=VIEW
query=select `pps`.`THREAD_ID` AS `thd_id`,`pps`.`PROCESSLIST_ID` AS `conn_id`,if(`pps`.`NAME` = \'thread/sql/one_connection\',concat(`pps`.`PROCESSLIST_USER`,\'@\',`pps`.`PROCESSLIST_HOST`),replace(`pps`.`NAME`,\'thread/\',\'\')) AS `user`,`pps`.`PROCESSLIST_DB` AS `db`,`pps`.`PROCESSLIST_COMMAND` AS `command`,`pps`.`PROCESSLIST_STATE` AS `state`,`pps`.`PROCESSLIST_TIME` AS `time`,`pps`.`PROCESSLIST_INFO` AS `current_statement`,if(`esc`.`END_EVENT_ID` is null,`esc`.`TIMER_WAIT`,NULL) AS `statement_latency`,if(`esc`.`END_EVENT_ID` is null,round(100 * (`estc`.`WORK_COMPLETED` / `estc`.`WORK_ESTIMATED`),2),NULL) AS `progress`,`esc`.`LOCK_TIME` AS `lock_latency`,`esc`.`ROWS_EXAMINED` AS `rows_examined`,`esc`.`ROWS_SENT` AS `rows_sent`,`esc`.`ROWS_AFFECTED` AS `rows_affected`,`esc`.`CREATED_TMP_TABLES` AS `tmp_tables`,`esc`.`CREATED_TMP_DISK_TABLES` AS `tmp_disk_tables`,if(`esc`.`NO_GOOD_INDEX_USED` > 0 or `esc`.`NO_INDEX_USED` > 0,\'YES\',\'NO\') AS `full_scan`,if(`esc`.`END_EVENT_ID` is not null,`esc`.`SQL_TEXT`,NULL) AS `last_statement`,if(`esc`.`END_EVENT_ID` is not null,`esc`.`TIMER_WAIT`,NULL) AS `last_statement_latency`,`mem`.`current_allocated` AS `current_memory`,`ewc`.`EVENT_NAME` AS `last_wait`,if(`ewc`.`END_EVENT_ID` is null and `ewc`.`EVENT_NAME` is not null,\'Still Waiting\',`ewc`.`TIMER_WAIT`) AS `last_wait_latency`,`ewc`.`SOURCE` AS `source`,`etc`.`TIMER_WAIT` AS `trx_latency`,`etc`.`STATE` AS `trx_state`,`etc`.`AUTOCOMMIT` AS `trx_autocommit`,`conattr_pid`.`ATTR_VALUE` AS `pid`,`conattr_progname`.`ATTR_VALUE` AS `program_name` from (((((((`performance_schema`.`threads` `pps` left join `performance_schema`.`events_waits_current` `ewc` on(`pps`.`THREAD_ID` = `ewc`.`THREAD_ID`)) left join `performance_schema`.`events_stages_current` `estc` on(`pps`.`THREAD_ID` = `estc`.`THREAD_ID`)) left join `performance_schema`.`events_statements_current` `esc` on(`pps`.`THREAD_ID` = `esc`.`THREAD_ID`)) left join `performance_schema`.`events_transactions_current` `etc` on(`pps`.`THREAD_ID` = `etc`.`THREAD_ID`)) left join `sys`.`x$memory_by_thread_by_current_bytes` `mem` on(`pps`.`THREAD_ID` = `mem`.`thread_id`)) left join `performance_schema`.`session_connect_attrs` `conattr_pid` on(`conattr_pid`.`PROCESSLIST_ID` = `pps`.`PROCESSLIST_ID` and `conattr_pid`.`ATTR_NAME` = \'_pid\')) left join `performance_schema`.`session_connect_attrs` `conattr_progname` on(`conattr_progname`.`PROCESSLIST_ID` = `pps`.`PROCESSLIST_ID` and `conattr_progname`.`ATTR_NAME` = \'program_name\')) order by `pps`.`PROCESSLIST_TIME` desc,if(`ewc`.`END_EVENT_ID` is null and `ewc`.`EVENT_NAME` is not null,\'Still Waiting\',`ewc`.`TIMER_WAIT`) desc
md5=42b975f81c88e5010bd88768cd426eb7
updatable=0
algorithm=2
definer_user=mariadb.sys
definer_host=localhost
suid=0
with_check_option=0
timestamp=0001700679051871453
create-version=2
source=SELECT pps.thread_id AS thd_id,\n       pps.processlist_id AS conn_id,\n       IF(pps.name = \'thread/sql/one_connection\',\n          CONCAT(pps.processlist_user, \'@\', pps.processlist_host),\n          REPLACE(pps.name, \'thread/\', \'\')) user,\n       pps.processlist_db AS db,\n       pps.processlist_command AS command,\n       pps.processlist_state AS state,\n       pps.processlist_time AS time,\n       pps.processlist_info AS current_statement,\n       IF(esc.end_event_id IS NULL,\n          esc.timer_wait,\n          NULL) AS statement_latency,\n       IF(esc.end_event_id IS NULL,\n          ROUND(100 * (estc.work_completed / estc.work_estimated), 2),\n          NULL) AS progress,\n       esc.lock_time AS lock_latency,\n       esc.rows_examined AS rows_examined,\n       esc.rows_sent AS rows_sent,\n       esc.rows_affected AS rows_affected,\n       esc.created_tmp_tables AS tmp_tables,\n       esc.created_tmp_disk_tables AS tmp_disk_tables,\n       IF(esc.no_good_index_used > 0 OR esc.no_index_used > 0, \'YES\', \'NO\') AS full_scan,\n       IF(esc.end_event_id IS NOT NULL,\n          esc.sql_text,\n          NULL) AS last_statement,\n       IF(esc.end_event_id IS NOT NULL,\n          esc.timer_wait,\n          NULL) AS last_statement_latency,\n       mem.current_allocated AS current_memory,\n       ewc.event_name AS last_wait,\n       IF(ewc.end_event_id IS NULL AND ewc.event_name IS NOT NULL,\n          \'Still Waiting\',\n          ewc.timer_wait) last_wait_latency,\n       ewc.source,\n       etc.timer_wait AS trx_latency,\n       etc.state AS trx_state,\n       etc.autocommit AS trx_autocommit,\n       conattr_pid.attr_value as pid,\n       conattr_progname.attr_value as program_name\n  FROM performance_schema.threads AS pps\n  LEFT JOIN performance_schema.events_waits_current AS ewc USING (thread_id)\n  LEFT JOIN performance_schema.events_stages_current AS estc USING (thread_id)\n  LEFT JOIN performance_schema.events_statements_current AS esc USING (thread_id)\n  LEFT JOIN performance_schema.events_transactions_current AS etc USING (thread_id)\n  LEFT JOIN sys.x$memory_by_thread_by_current_bytes AS mem USING (thread_id)\n  LEFT JOIN performance_schema.session_connect_attrs AS conattr_pid\n    ON conattr_pid.processlist_id=pps.processlist_id and conattr_pid.attr_name=\'_pid\'\n  LEFT JOIN performance_schema.session_connect_attrs AS conattr_progname\n    ON conattr_progname.processlist_id=pps.processlist_id and conattr_progname.attr_name=\'program_name\'\n ORDER BY pps.processlist_time DESC, last_wait_latency DESC;
client_cs_name=utf8mb3
connection_cl_name=utf8mb3_general_ci
view_body_utf8=select `pps`.`THREAD_ID` AS `thd_id`,`pps`.`PROCESSLIST_ID` AS `conn_id`,if(`pps`.`NAME` = \'thread/sql/one_connection\',concat(`pps`.`PROCESSLIST_USER`,\'@\',`pps`.`PROCESSLIST_HOST`),replace(`pps`.`NAME`,\'thread/\',\'\')) AS `user`,`pps`.`PROCESSLIST_DB` AS `db`,`pps`.`PROCESSLIST_COMMAND` AS `command`,`pps`.`PROCESSLIST_STATE` AS `state`,`pps`.`PROCESSLIST_TIME` AS `time`,`pps`.`PROCESSLIST_INFO` AS `current_statement`,if(`esc`.`END_EVENT_ID` is null,`esc`.`TIMER_WAIT`,NULL) AS `statement_latency`,if(`esc`.`END_EVENT_ID` is null,round(100 * (`estc`.`WORK_COMPLETED` / `estc`.`WORK_ESTIMATED`),2),NULL) AS `progress`,`esc`.`LOCK_TIME` AS `lock_latency`,`esc`.`ROWS_EXAMINED` AS `rows_examined`,`esc`.`ROWS_SENT` AS `rows_sent`,`esc`.`ROWS_AFFECTED` AS `rows_affected`,`esc`.`CREATED_TMP_TABLES` AS `tmp_tables`,`esc`.`CREATED_TMP_DISK_TABLES` AS `tmp_disk_tables`,if(`esc`.`NO_GOOD_INDEX_USED` > 0 or `esc`.`NO_INDEX_USED` > 0,\'YES\',\'NO\') AS `full_scan`,if(`esc`.`END_EVENT_ID` is not null,`esc`.`SQL_TEXT`,NULL) AS `last_statement`,if(`esc`.`END_EVENT_ID` is not null,`esc`.`TIMER_WAIT`,NULL) AS `last_statement_latency`,`mem`.`current_allocated` AS `current_memory`,`ewc`.`EVENT_NAME` AS `last_wait`,if(`ewc`.`END_EVENT_ID` is null and `ewc`.`EVENT_NAME` is not null,\'Still Waiting\',`ewc`.`TIMER_WAIT`) AS `last_wait_latency`,`ewc`.`SOURCE` AS `source`,`etc`.`TIMER_WAIT` AS `trx_latency`,`etc`.`STATE` AS `trx_state`,`etc`.`AUTOCOMMIT` AS `trx_autocommit`,`conattr_pid`.`ATTR_VALUE` AS `pid`,`conattr_progname`.`ATTR_VALUE` AS `program_name` from (((((((`performance_schema`.`threads` `pps` left join `performance_schema`.`events_waits_current` `ewc` on(`pps`.`THREAD_ID` = `ewc`.`THREAD_ID`)) left join `performance_schema`.`events_stages_current` `estc` on(`pps`.`THREAD_ID` = `estc`.`THREAD_ID`)) left join `performance_schema`.`events_statements_current` `esc` on(`pps`.`THREAD_ID` = `esc`.`THREAD_ID`)) left join `performance_schema`.`events_transactions_current` `etc` on(`pps`.`THREAD_ID` = `etc`.`THREAD_ID`)) left join `sys`.`x$memory_by_thread_by_current_bytes` `mem` on(`pps`.`THREAD_ID` = `mem`.`thread_id`)) left join `performance_schema`.`session_connect_attrs` `conattr_pid` on(`conattr_pid`.`PROCESSLIST_ID` = `pps`.`PROCESSLIST_ID` and `conattr_pid`.`ATTR_NAME` = \'_pid\')) left join `performance_schema`.`session_connect_attrs` `conattr_progname` on(`conattr_progname`.`PROCESSLIST_ID` = `pps`.`PROCESSLIST_ID` and `conattr_progname`.`ATTR_NAME` = \'program_name\')) order by `pps`.`PROCESSLIST_TIME` desc,if(`ewc`.`END_EVENT_ID` is null and `ewc`.`EVENT_NAME` is not null,\'Still Waiting\',`ewc`.`TIMER_WAIT`) desc
mariadb-version=101105
