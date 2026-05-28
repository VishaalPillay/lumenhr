-- SYNTHETIC DATA ONLY — NO REAL PII
INSERT INTO employees (id, member_id, display_name, role_type, department, manager_id) VALUES
(gen_random_uuid(), 'EMP-001', 'Manager Alpha', 'ENGINEERING_MANAGER', 'DEPT-ENG',   NULL),
(gen_random_uuid(), 'EMP-002', 'Team Member B', 'SENIOR_ENGINEER',     'DEPT-ENG',   'EMP-001'),
(gen_random_uuid(), 'EMP-003', 'Team Member C', 'SENIOR_ENGINEER',     'DEPT-ENG',   'EMP-001'),
(gen_random_uuid(), 'EMP-004', 'Team Member D', 'JUNIOR_ENGINEER',     'DEPT-ENG',   'EMP-001'),
(gen_random_uuid(), 'EMP-005', 'Team Member E', 'JUNIOR_ENGINEER',     'DEPT-ENG',   'EMP-001'),
(gen_random_uuid(), 'EMP-006', 'Manager Beta',  'ENGINEERING_MANAGER', 'DEPT-SALES', NULL),
(gen_random_uuid(), 'EMP-007', 'Team Member G', 'SALES_EXECUTIVE',     'DEPT-SALES', 'EMP-006'),
(gen_random_uuid(), 'EMP-008', 'Team Member H', 'SALES_EXECUTIVE',     'DEPT-SALES', 'EMP-006');