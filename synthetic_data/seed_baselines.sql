-- ROLE BASELINES — Fabric IQ operational mirror
INSERT INTO role_baselines (id, role_type, department, expected_meeting_hrs, focus_time_min_hrs, overload_threshold, context_notes) VALUES
(gen_random_uuid(), 'ENGINEERING_MANAGER', 'DEPT-ENG',   30, 4,  38, 'EMs have high meeting load by design. Flag at 38hrs/week.'),
(gen_random_uuid(), 'SENIOR_ENGINEER',     'DEPT-ENG',   18, 10, 28, 'Senior engineers need deep focus time. Protect below 10hrs.'),
(gen_random_uuid(), 'JUNIOR_ENGINEER',     'DEPT-ENG',   12, 14, 22, 'Juniors need maximum focus time for skill development.'),
(gen_random_uuid(), 'SALES_EXECUTIVE',     'DEPT-SALES', 25, 6,  35, 'Sales roles have naturally high meeting cadence.');