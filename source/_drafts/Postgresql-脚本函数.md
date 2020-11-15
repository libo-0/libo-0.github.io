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

5. 创建表

```sql
CREATE TABLE "ban"."launch_page" (
	"uuid" VARCHAR (32) COLLATE "pg_catalog"."DEFAULT" NOT NULL,
	" ad_name " VARCHAR ( 60 ) COLLATE " pg_catalog "." DEFAULT " NOT NULL,
	" ad_type " SMALLINT COLLATE " pg_catalog "." DEFAULT " NOT NULL,
	" resource_url " VARCHAR ( 240 ) COLLATE " pg_catalog "." DEFAULT " NOT NULL,
	" begin_time " TIMESTAMP,
	" end_time " TIMESTAMP,
	" ad_cycle " SMALLINT,
	" show_times_per_cycle " SMALLINT,
	" priority" SMALLINT,
	" skip_flag " SMALLINT,
	" ad_last_time " SMALLINT,
	" target_url " VARCHAR ( 120 ),
	" enable_flag " SMALLINT,
	" LANGUAGE " VARCHAR ( 32 ) COLLATE " pg_catalog "." DEFAULT " NOT NULL,
	" device " int4 DEFAULT 0,
	" project " VARCHAR ( 32 ) COLLATE " pg_catalog "." DEFAULT ",
	" create_user " VARCHAR ( 32 ) COLLATE " pg_catalog "." DEFAULT ",
	" create_time " TIMESTAMP ( 6 ),
	" update_user " VARCHAR ( 32 ) COLLATE " pg_catalog "." DEFAULT ",
	" update_time " TIMESTAMP ( 6 ),
	" delete_flag " int4 NOT NULL DEFAULT 1,
	" park_uuid " VARCHAR ( 32 ) COLLATE " pg_catalog "." DEFAULT " NOT NULL,
	CONSTRAINT " ban_launch_page_pkey " PRIMARY KEY ( " uuid " ) 
);
COMMENT ON TABLE " ban "." launch_page " IS '闪屏页，即App启动页‘；
comment on COLUMN " ban "." launch_page "." ad_name " is '广告名称'；
comment on COLUMN " ban "." launch_page "." ad_resource_type " is '广告资源类型， 1 :图片； 2 :视频 '；
comment on COLUMN " ban "." launch_page "." resource_url " is '广告素材地址，即图片 /广告地址，前台限制尺寸和大小 '；
comment on column " ban "." launch_page "." begin_time " is '广告生效开始时间，精确到秒';
comment on column " ban "." launch_page "." end_time " is '广告生效结束时间，精确到秒';
comment on column " ban "." launch_page "." show_times_per_cycle " is '每周期广告显示次数';
comment on column " ban "." launch_page "." ad_cycle " is '广告显示周期， 0-每次启动，1-每天，2-每周，3-每月 ';
comment on column " ban "." launch_page "." skip_flag " is '可跳过标志： 1 :可跳过， 0 :不可跳过 ';
comment on column " ban "." launch_page "." ad_last_time " is '广告持续时间';
comment on column " ban "." launch_page "." target_url " is '广告跳转地址，链接地址';
COMMENT ON COLUMN " ban "." launch_page "." LANGUAGE " IS ' zh - cn / en - us ';
COMMENT ON COLUMN " ban "." launch_page "." park_uuid " IS '园区 uuid ';

COMMENT ON COLUMN " ban "." launch_page "." enable_flag " is ’广告启用标志，1-启用，2-禁用‘；

COMMENT ON COLUMN " ban "." launch_page "." device " IS ' 0-web,
1-app,
2-html5 ';

COMMENT ON COLUMN " ban "." launch_page "." project " IS '项目名称';

COMMENT ON COLUMN " ban "." launch_page "." create_user " IS '创建者';

COMMENT ON COLUMN " ban "." launch_page "." create_time " IS '创建时间';

COMMENT ON COLUMN " ban "." launch_page "." update_user " IS '修改者';

COMMENT ON COLUMN " ban "." launch_page "." update_time " IS '修改时间';

COMMENT ON COLUMN " ban "." launch_page "." delete_flag " IS '删除标志 ( 1 :未删除; 0 :已删除 ) ';
```

6. pgl 函数

```sql
-- 函数

CREATE OR REPLACE FUNCTION public.update_image ( arr TEXT [] ) RETURNS TEXT AS 
$$ 
DECLARE
image TEXT;
i int4 := 0;
len int4 := array_length(arr, 1);
summer TEXT := '';
BEGIN
		foreach image IN ARRAY arr
		loop
		i := i + 1;
		summer := summer || split_part(image, '?', 1);
		if i < len 
		then summer := summer || '",';
		else summer := summer || '"]';
		end if;
END loop;
raise notice ': %', summer;
RETURN summer;
END $$ LANGUAGE plpgsql;

-- 订单
update "tm"."hotel_room_information" set room_image_album = update_image(string_to_array(room_image_album, ',')) where room_image_album is not null;
update "tm"."hotel_room_information_preview" set room_image_album = update_image(string_to_array(room_image_album, ',')) where room_image_album is not null;
update "tm"."theater_basic_information" set album_images = update_image(string_to_array(album_images, ',')) where album_images is not null;
update "tm"."theater_repertoire_info" set screenshot = split_part(screenshot, '?', 1) where screenshot is not null;
update "tm"."theater_repertoire_info_preview" set screenshot = split_part(screenshot, '?', 1) where screenshot is not null;

-- 餐饮
update "fb"."restaurant_information" set restaurant_image = update_image(string_to_array(restaurant_image, ',')) where restaurant_image is not null;

```