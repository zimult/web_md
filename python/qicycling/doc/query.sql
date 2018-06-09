--
select * from wp_term_taxonomy t
inner join wp_terms w on w.term_id=t.term_id
where taxonomy = 'category'


