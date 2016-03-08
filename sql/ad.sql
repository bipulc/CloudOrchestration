declare
 
l_start_dt date := '4 sep 2015';
l_tmp_dt date;
 
begin
    for i in 1..14 loop
--        dbms_output.put_line(' P-Start ' || l_start_dt);
        l_tmp_dt := l_start_dt;
        l_start_dt := l_start_dt + 6;
        dbms_output.put_line(' P-Start-End ' || l_tmp_dt || ' - ' || l_start_dt);
 
        l_start_dt := l_start_dt + 1;
  --      dbms_output.put_line(' D-Start ' || l_start_dt);
        l_tmp_dt := l_start_dt;
        l_start_dt := l_start_dt + 20;
        dbms_output.put_line(' D-Start-End ' || l_tmp_dt || ' - ' || l_start_dt);
        l_start_dt := l_start_dt + 1;
    end loop;
 
end;
