-- PRE-COMPUTED SCORES — synthetic demo data
INSERT INTO pre_computed_scores (id, member_id, computed_at, score, risk_tier, trend_delta, trend_direction, signal_summary) VALUES
(gen_random_uuid(), 'EMP-002', NOW(), 82, 'HIGH',      12, 'worsening', '{"meeting_hrs": 34, "focus_hrs": 1,  "after_hours_days": 4}'),
(gen_random_uuid(), 'EMP-003', NOW(), 61, 'MODERATE',   8, 'worsening', '{"meeting_hrs": 26, "focus_hrs": 4,  "after_hours_days": 2}'),
(gen_random_uuid(), 'EMP-004', NOW(), 38, 'LOW',        -3, 'improving', '{"meeting_hrs": 14, "focus_hrs": 16, "after_hours_days": 0}'),
(gen_random_uuid(), 'EMP-005', NOW(), 55, 'MODERATE',   2, 'stable',    '{"meeting_hrs": 20, "focus_hrs": 8,  "after_hours_days": 1}'),
(gen_random_uuid(), 'EMP-007', NOW(), 91, 'CRITICAL',  18, 'worsening', '{"meeting_hrs": 38, "focus_hrs": 0,  "after_hours_days": 5}'),
(gen_random_uuid(), 'EMP-008', NOW(), 44, 'LOW',        -6, 'improving', '{"meeting_hrs": 18, "focus_hrs": 12, "after_hours_days": 0}');

-- EMPLOYEE PREFERENCES
INSERT INTO employee_preferences (member_id, opted_in, opted_in_at, alert_threshold) VALUES
('EMP-002', true, NOW(), 'HIGH'),
('EMP-003', true, NOW(), 'MODERATE'),
('EMP-004', true, NOW(), 'MODERATE'),
('EMP-005', true, NOW(), 'HIGH'),
('EMP-007', true, NOW(), 'MODERATE'),
('EMP-008', true, NOW(), 'HIGH');