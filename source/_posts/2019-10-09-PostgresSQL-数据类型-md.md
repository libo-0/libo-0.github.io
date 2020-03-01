---
title: PostgresSQL-数据类型.md
date: 2019-10-09 15:51:27
tags:
---

# PostgreSQL 数据类型

Postgresql 不仅包含了 SQL 定义的数据类型：bigint, bit, bit varying, boolean, char, character varying, character, varchar, date, double precision, integer, interval, numeric, decimal, real, smallint, time(with or without time zone), timestamp(with or without time zone), xml 等等，还定义了很多自己的数据类型。

Postgresql 的数据类型大概分为： 数值类型，金钱类型，字符类型，二进制数据类型，日期时间类型，布尔类型，枚举类型，地理类型，网络地址类型，位字符串类型，文本搜索类型，UUID 类型，XML 类型， JSON 类型，数组类型， 复合类型，范围类型， 对象标识符类型， pg_lsn 类型，Pseudo 类型 等等。

## 数值类型

数值类型包括 2，4，8 字节的整数，4，8 字节的浮点数，可选精度的十进制数。

smallint, integer, bigint, decimal, numeric, real, double precision, smallserial, serial, bigserial

## 金钱类型

money

## 字符类型

character varying， varchar（n），character(n), char(n), text

## 二进制数据类型

bytea

## 日期/时间 类型

timastamp[without time zone], timestamp with time zone, date, time without time zone, time with time zxone, interval

## 布尔类型

boolean

## 枚举类型

``` SQL
create type mood as enum('sad', 'ok', 'happy');
```

## 地理类型

point, line, lseg, box, path, path, polygon, circle

## 网络地址类型

cidr, inet, macaddr

## bit 字符串类型

bit

## 文本搜索类型

tsvector, tsquery

## UUID 类型

## XML 类型

## JSON 类型

## 数组

## 复合类型

``` SQL
create type inventory_item as(
    name text,
    supplier_id, integer,
    price numeric
);
```

## 范围类型

## 对象标识符类型

## pg_lsn 类型

## pseudo 类型


