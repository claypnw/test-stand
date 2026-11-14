# Effort log — standing queries

Run both with muse.db for the day being logged. The day runs from midnight
Arizona time; in the database that is 07:00 UTC on the day to 07:00 UTC the
next day. Replace DAY_START with e.g. '2026-11-10T07:00:00Z' and DAY_END with
the next day's 'T07:00:00Z'.

Grouping rule: a job that ran more than 4 times in the day gets ONE grouped
row (its runs added together). Every other job gets one row per job (its runs
that day added together). Feed pulses group under one row. Rows with no token
record and no run time get the note "no record stands".

## Query 1 — the all-day watches (jobs with many runs), grouped
WITH hatch_cte_tok AS (SELECT agent_id, sum(input_tokens) AS in_tok, sum(output_tokens) AS out_tok FROM agent.agent_message_token_usage GROUP BY agent_id)
SELECT r.job_id AS job, count(*) AS runs_n, sum(date_part('epoch', r.finished_at - r.started_at)) AS run_seconds, sum(coalesce(w.in_tok,0) + coalesce(h.in_tok,0)) AS in_tok, sum(coalesce(w.out_tok,0) + coalesce(h.out_tok,0)) AS out_tok
FROM scheduler.job_runs r
LEFT JOIN hatch_cte_tok w ON w.agent_id = r.worker_agent_id
LEFT JOIN hatch_cte_tok h ON h.agent_id = r.worker_history_agent_id
WHERE r.scheduled_for >= 'DAY_START' AND r.scheduled_for < 'DAY_END'
GROUP BY r.job_id HAVING count(*) > 4 ORDER BY run_seconds DESC

## Query 2 — every other job, one row per job
Same CTE and joins; ending:
GROUP BY r.job_id HAVING count(*) <= 4 ORDER BY min(r.started_at)
and also select min(r.started_at) if the start time is wanted.
