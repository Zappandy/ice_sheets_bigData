CREATE KEYSPACE IF NOT EXISTS icesheet_keyspace 
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
/*
CREATE TABLE icesheetreport(
  _year INT,
  _month INT,
  _day INT,
  extend FLOAT,
  missing FLOAT,
  hemisphere TEXT)
  PRIMARY KEY (hemisphere, extend)
);
*/
