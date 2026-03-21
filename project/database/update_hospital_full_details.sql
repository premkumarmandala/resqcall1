-- Create full hospital details with lat/long and simulated data

-- Add columns if they don't exist (using a procedure or just straight logic if script is run once)
-- We will assume columns need to be added. 
-- For safety, since we can't do IF NOT EXISTS for columns in simple MySQL easily without procedure,
-- we will just attempt to update assuming user is running populate first time or willing to reset.
-- Actually, the best way is to DROP and RECREATE or just clear data.
-- We will clear existing data to avoid duplicates and ensure clean state.

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE hospitals;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO hospitals (name, address, contact_phone, total_beds, icu_beds, oxygen_status, latitude, longitude) VALUES
('King George Hospital (KGH)', 'Opp. District Collector Office, Maharanipeta, Visakhapatnam, Andhra Pradesh 530002', '0891-2564891', 1200, 150, 'Available', 17.7032, 83.3056),
('Visakha Institute of Medical Sciences (VIMS)', 'Hanumanthavaka, Arilova, Visakhapatnam, Andhra Pradesh 530040', '0891-2740404', 800, 100, 'Available', 17.7654, 83.3345),
('Apollo Hospitals', 'Waltair Main Road, Ram Nagar, Visakhapatnam, Andhra Pradesh 530002', '0891-2727272', 350, 60, 'Available', 17.7171, 83.3092),
('Care Hospitals', 'A.S. Raja Complex, Waltair Main Road, Ramnagar, Visakhapatnam, Andhra Pradesh 530002', '0891-3041444', 300, 50, 'Available', 17.7118, 83.3139),
('Seven Hills Hospital', 'Rockdale Layout, Waltair Main Road, Visakhapatnam, Andhra Pradesh 530002', '0891-6677777', 400, 70, 'Available', 17.7174, 83.3094),
('Medicover Hospitals', 'NH 16, Venkojipalem, Visakhapatnam, Andhra Pradesh 530022', '0891-6688888', 500, 80, 'Available', 17.7397, 83.3289),
('Mahatma Gandhi Cancer Hospital', '1/7, MVP Colony, Sector 7, Visakhapatnam, Andhra Pradesh 530017', '0891-2878787', 250, 40, 'Available', 17.7425, 83.3389),
('Indus Hospitals', 'KGH Down Road, Maharanipeta, Visakhapatnam, Andhra Pradesh 530002', '0891-2508888', 200, 30, 'Low', 17.7035, 83.3032), 
('OMNI RK Super Specialty Hospital', 'Opposite Lions Club, Waltair Main Road, Ram Nagar, Visakhapatnam, Andhra Pradesh 530002', '0891-2555555', 220, 35, 'Available', 17.7186, 83.3116),
('Queens NRI Hospital', '50-53-14, Gurudwara Lane, Seethammadhara, Visakhapatnam, Andhra Pradesh 530013', '0891-2525252', 180, 25, 'Available', 17.7379, 83.3040),
('GITAM Hospital', 'Rushikonda, Visakhapatnam, Andhra Pradesh 530045', '0891-2840450', 600, 90, 'Available', 17.7815, 83.3765),
('Pinnacle Hospital', 'Arilova Main Road, Health City, Chinagadili, Visakhapatnam, Andhra Pradesh 530040', '0891-6699999', 300, 45, 'Available', 17.7637, 83.3082),
('Manipal Hospital', '15-2-8/A, Gokhale Road, Maharanipeta, Visakhapatnam, Andhra Pradesh 530002', '1800-102-5555', 250, 40, 'Available', 17.7085, 83.3052),
('MyCure Hospitals', '15-2-9, Gokhale Rd, Krishna Nagar, Maharanipeta, Visakhapatnam, Andhra Pradesh 530002', '0891-6661111', 150, 20, 'Critical', 17.7120, 83.3147),
('A.N. Beach Hospital', '15-9-13/24, Krishna Nagar, Maharanipeta, Visakhapatnam, Andhra Pradesh 530002', '0891-2566666', 100, 15, 'Available', 17.7129, 83.3198),
('L.V. Prasad Eye Institute', 'GMR Varalakshmi Campus, Hanumanthawaka Junction, Visakhapatnam, Andhra Pradesh 530040', '0891-6622222', 120, 10, 'Available', 17.7668, 83.3387),
('Homi Bhabha Cancer Hospital', 'Aganampudi, Visakhapatnam, Andhra Pradesh 531011', '0891-2999999', 150, 20, 'Available', 17.6899, 83.1144),
('Government Victoria Hospital', 'Chengal Rao Peta, Visakhapatnam, Andhra Pradesh 530001', '0891-2562222', 180, 25, 'Low', 17.6974, 83.2986),
('Government Hospital for Mental Care', 'Chinna Waltair, Visakhapatnam, Andhra Pradesh 530003', '0891-2559999', 300, 0, 'Available', 17.7284, 83.3335),
('Lazarus Hospitals', 'Opposite Vasan Eye Care, Waltair Main Road, Visakhapatnam, Andhra Pradesh 530002', '0891-2588888', 120, 18, 'Available', 17.7172, 83.3083);
