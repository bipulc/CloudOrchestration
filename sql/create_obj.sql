create table test_load (x number);
create sequence load_seq start with 1;

create or replace procedure load_tab_proc(pi_rows in number )          
as
i number;
begin

i := 1;

loop

	insert into test_load (x) values (i);
	i := i + 1;
	EXIT when i > pi_rows;

end loop;

commit;
end load_tab_proc;
/
