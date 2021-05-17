CREATE KEYSPACE assignment5 WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE assignment5.universities_near_person (
    university_name text,
    person_name text,
    university_phone text,
    university_address text,
    person_phone text,
    person_address text,
    distance_km smallint,
    PRIMARY KEY ((university_name), person_name)
) WITH comment = 'Q1. Q2. Q3. Q5.'
AND CLUSTERING ORDER BY (person_name ASC) ;

CREATE TABLE assignment5.available_courses_by_registration_date (
    course_id text,
    university_name text,
    name text,
    cost text,
    registration_date date,
    is_available boolean,
    PRIMARY KEY ((course_id), university_name)
) WITH comment = 'Q4.';

INSERT INTO assignment5.universities_near_person (university_name, person_name, university_phone, university_address, person_phone, person_address, distance_km) VALUES ('University of Victoria', 'Ron Garcia','250-208-1212', 'University address, Victoria, BC', '250-202-1199', 'Person address, Victoria, BC', 12);
INSERT INTO assignment5.universities_near_person (university_name, person_name, university_phone, university_address, person_phone, person_address, distance_km) VALUES ('University of Waterloo', 'Ron Garcia','519-888-4567', 'University address, Waterloo, ON', '250-202-1199', 'Person address, Victoria, BC', 4000);
INSERT INTO assignment5.universities_near_person (university_name, person_name, university_phone, university_address, person_phone, person_address, distance_km) VALUES ('University of Victoria', 'Geo Parrott','250-208-1212', 'University address, Victoria, BC', '250-202-0202', 'Person address, Victoria, BC', 50);

INSERT INTO assignment5.available_courses_by_registration_date (course_id, university_name, name, cost, registration_date, is_available) VALUES ('DS_101', 'University of Waterloo','Spark', '$1000', '2021-02-18', false);
INSERT INTO assignment5.available_courses_by_registration_date (course_id, university_name, name, cost, registration_date, is_available) VALUES ('DS_201', 'University of Waterloo','Cassandra', '$1000', '2021-04-12', true);
INSERT INTO assignment5.available_courses_by_registration_date (course_id, university_name, name, cost, registration_date, is_available) VALUES ('DS_201', 'University of Victoria','Cassandra', '$1350', '2021-06-15', true);
