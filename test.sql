# ALTER DATABASE leviathan DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
# alter table table_name convert to character set utf8;

INSERT into location(province,city,county,street) VALUES ('北京','北京','海淀','学院路37号');
INSERT into hospital(name,level,type,information,createtime,id_location)
VALUES ('北航校医','三级甲等','普通','北航医院，人少，学生管报销，速来。','2016/11/24 14:35',1);
INSERT into department(name,id_hospital) VALUES('外科',1);
INSERT INTO doctor(name, level, speciality, information,careertime, gender, age, createtime)
VALUES ('王大海','主任医师','外科','十年从医',10,'男',55,'2016/11/24 14:35');
INSERT INTO  doctor_department(id_department,id_doctor) VALUES (1,1);
INSERT INTO adminpublisher(loginname, password, id_hospital, createtime)
    VALUES ('test','test',1,'2016-11-26 03:19:16');
INSERT INTO bulletin(availabletime, fee, countavailable, countoccupied, id_adminpublisher, id_doctor_department, createtime)
    VALUES ('2017-01-27 03:20:10',10,5,2,1,1,'2016-11-26 03:19:16');