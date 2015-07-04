CREATE TABLE scats (
	tcsno INTEGER,
	time TIMESTAMP,
	longitude FLOAT,
	latitude FLOAT,
	geom GEOMETRY(POINT, 4326),
	detectors INTEGER[],
	total INTEGER,
	PRIMARY KEY (tcsno, time)
);

CREATE INDEX scats_time_idx ON scats(time);

CREATE MATERIALIZED VIEW scats_locations
(tcsno, longitude, latitude, maximum, average)
AS SELECT tcsno, longitude, latitude, MAX(total), AVG(total)
FROM scats GROUP BY tcsno, longitude, latitude;

CREATE MATERIALIZED VIEW scats_times (time)
AS SELECT DISTINCT time FROM scats;

