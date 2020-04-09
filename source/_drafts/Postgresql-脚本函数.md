---
title: Postgresql-脚本函数
tags:
categories:
---



<!-- more -->

1. 定义字段转换函数

```sql
-- 订单状态转换函数
CREATE FUNCTION order_status ( status TEXT ) RETURNS TEXT AS $$ SELECT
CASE
		
	WHEN
		status = '1' THEN
			'预订' 
			WHEN status = '2' THEN
			'退票中' 
			WHEN status = '3' THEN
			'退票失败' 
			WHEN status = '4' THEN
			'退票成功' 
			WHEN status = '5' THEN
			'取消' 
			WHEN status = '6' THEN
			'出票中' 
			WHEN status = '7' THEN
			'出票成功' 
			WHEN status = '8' THEN
			'已完成' 
			WHEN status = '9' THEN
			'支付超时关闭' 
			WHEN status = '10' THEN
			'出票失败' 
			WHEN status = '11' THEN
		'过期关闭' ELSE'' 
	END;	$$ LANGUAGE SQL IMMUTABLE STRICT;
```

2. 添加列，注释

```sql
alter table "tm"."hotel_basic_information" add column "debut_time" timestamp;
alter table "tm"."hotel_basic_information" add column "internet_site" varchar(128);
alter table "tm"."hotel_basic_information" add column "introduction" varchar(1024);
alter table "tm"."hotel_basic_information" add column "recommendation" varchar(256);
alter table "tm"."hotel_basic_information" add column "facilities" varchar(512);
alter table "tm"."hotel_basic_information" add column "notice" varchar(512);

COMMENT ON COLUMN "tm"."hotel_basic_information"."debut_time" IS '开业时间';
COMMENT ON COLUMN "tm"."hotel_basic_information"."notice" IS '预订须知/注意事项';
COMMENT ON COLUMN "tm"."hotel_basic_information"."introduction" IS '介绍';
COMMENT ON COLUMN "tm"."hotel_basic_information"."internet_site" IS '酒店网址';
COMMENT ON COLUMN "tm"."hotel_basic_information"."facilities" IS '酒店配套设施';
COMMENT ON COLUMN "tm"."hotel_basic_information"."recommendation" IS '推荐语';

```

3. 修改列定义

```sql
alter table hotel_basic_information alter column hotel_name type varchar(256);
```

4. 查询数据，使用函数，更改表头

```sql
SELECT
	order_no AS 订单编号,
	sys_short AS 业态,
	link_name AS 姓名,
	link_phone AS 电话,
	order_status(order_status) AS 订单状态,
	pay_status AS 支付状态,
	pay_money AS 支付金额,
	pay_flowing_number AS 支付流水,
	payment_number AS 支付编号,
	payment_scene AS 支付场景,
	pay_method AS 支付方式,
	checkin_time AS 核销时间,
	SOURCE AS 订单来源,
	create_time AS 创建时间,
	update_time AS 更新时间 
FROM
	order_common_info;
```