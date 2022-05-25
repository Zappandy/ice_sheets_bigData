CREATE TABLE icesheetreport(
  _year INT,
  _month INT,
  _day INT,
  extend FLOAT,
  missing FLOAT,
  hemisphere TEXT)
  PRIMARY KEY (hemisphere, extend)
);