---
title: PostgreSQL-索引
tags:
  - PostgreSQL
  - 索引
categories:
  - PostgreSQL
  - 索引
img: /images/PostgreSQL.png
toc: true
date: 2020-03-05 14:06:27
---


Indexes 索引是一种优化数据库性能的常用方式。索引允许数据库服务器查询更快。PostgreSQL 提供 B-tree, hash, GiST, SP-GiST, GIN, 和 BRIN 索引方法。

<!-- more -->

1. 创建索引

```SQL
CREATE INDEX test1_id_index ON test1 (id);
```

## 索引简述

一旦索引创建，无须干涉：系统会自动在表更新的时候更新索引。在一个大表上建立索引很花时间。

在索引创建后，系统会让它与表保持同步。这对数据操作添加了工作量。因此，几乎不用或很少使用的索引应该删除。

## PostgreSQL 索引简述

PostgreSQL 提供了集中索引类型，B-tree， Hash， GiST，SP-GiST， GIN， 和 BRIN。每种索引类型使用不同的算法，最适合特定类型的查询。默认，`CREATE INDEX` 创建 B-tree 索引，使用与大多数情况。

B-trees 索引支持在能够排序的数据上处理相等或范围查询。尤其，PostgreSQL query planner 会考虑使用 B-tree 索引，当以下操作符被使用时：<, <=, =, >=, >。

Hash 索引只能处理简单的相等比较。接下来创建一个 Hash 索引：

```SQL
CREATE INDEX name ON table USING HASH (column);
```

Gist 索引不是一种索引，而是很多不同索引策略的基础。PostgreSQL 的标准发行版包含二维地理数据类型的操作符支持：`<<, &<, &>, >>, <<, &<, |&>, |>>, @>, <@, ~=, &&`。

GiST 索引同时能够优化“近邻”搜索，例如：

```SQL
SELECT * FROM places ORDER BY locatin <-> point '(101, 456)' LIMIT 10;
```

SP-GiST 索引，像 GiST 索引，提供了基础设施来支持各种搜索。SP-GiST 允许实现大范围的不同的不平衡的基于设备的数据结构，例如 quadtrees， k-d trees， radix trees。标准 PostgreSQL 发行版包括二维点的 SP-GiST 操作符，这些操作符支持索引查询：<<, >>, ~=, <@, <^, >^。

GIN 索引，像反转索引，合适于包含多个组件值，例如数组。一个反转索引为每个组件值包含了分离的入口，能够有效地处理“测试特定组件值存在性”的查询。

像 GiST 和 SP-GiST，GIN 能够支持很多不同的用户定义索引策略，GIN 索引能够使用的操作符取决于索引策略。作为示例，PostgreSQL 标准发行版包含一个数组的 GIN 操作符类，支持下列操作符索引查询：`<@, @>, =, &&`。

BRIN (Block Range Indexes) 索引，存储一个表中连续物理块的总结。

## 多列索引

```SQL
        CREATE TABLE test2 (
          major int,
          minor int,
          name varchar
);
```

查询
```SQL
SELECT name FROM test2 WHERE major = constant AND minor = constant;
```

创建索引
```SQL
CREATE INDEX test2_mm_idx ON test2 (major, minor);
```

目前，只有 B-tree， GiST，GIN， BRIN 支持多列索引，最多 32 列。

一个多列 B-tree 索引可以用来查询包含索引列的任意子集。

## 索引和 ORDER BY

索引除了简化查询，同样能够按特定顺序输出。这允许 ORDER BY 启用而不用单独的排序步骤。PostgreSQL 当前仅支持 B-tree 有序输出。

planner 考虑满足  `ORDER BY`，要么通过扫描一个索引，要么扫描表的物理顺序，然后另外做一个排序步骤。对于一个大分数表的查询，一个具体的排序比使用索引更快，因为它去要更少的磁盘 IO，因为跟随了顺序进入模式。但当只需要获取少量行的时候，索引更有用。一个重要的特别的例子是 `ORDER BY` 与 `LIMIT n` 的结合：为了获得前 n 条数据，必须处理所有的数据，但是如果有一个索引匹配 `ORDER BY`, 前 n 行可能直接提取，而不用扫描剩下的。

默认， B-tree 索引升序存储 entries，null 最后。但是，可以在创建索引的时候修改。例如：

```SQL
CREATE INDEX test2_info_nulls_low ON test2 (info NULLS FIRST);
 CREATE INDEX test3_desc_index ON test3 (id DESC NULLS LAST);
```

## 表达式索引

一个索引列不仅仅可以是表的一个列，还可以是一个一列或多列组成的表达式。这个特点在需要快速获取计算结果是特别有用。

例如：使用 lower 函数的大小写不敏感的比较：

```SQL
SELECT * FROM test1 WHERE lower(col1) = 'value';
```

这个查询可以用下列的索引：

```SQL
CREATE INDEX test1_lower_col1_idx ON test1 (lower(col1));
```

索引表达式维护起来代价很大，因为每行插入或更新的时候都要计算表达式。因此，当只有提取速度比插入或更新更重要时，对表达式的索引才有用。

## Partial Indexes（部分索引）

部分索引是构建在表上的一个子集的索引；子集由状态表达式定义。索引只会包含满足条件的行。部分索引是一个独特的特点，因为在几种条件下非常有用。

一个使用部分索引的主要原因是避免索引“常见值”。因为不管怎样，“常见值” 的查询不会使用索引，保存这些行的索引没有意义。这减少了索引的大小，加速了这些查询。它也同样会加速很多更新操作的查询，因为不是所有情况都需要更新索引。

创建索引使用如下类似命令：

```SQL
CREATE INDEX access_log_client_ip_ix ON access_log (client_ip) WHERE NOT (client_ip > inet '192.168.100.0' AND
client_ip < inet '192.168.100.255');
```

一个会使用这个索引的查询：

```SQL
SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '212.78.10.32';
```

一个不会使用这个索引的例子：

```SQL
SELECT *
FROM access_log
WHERE client_ip = inet '192.168.100.23';
```

### 建立索引排除不感兴趣的值

```SQL
CREATE INDEX orders_unbilled_index ON orders (order_nr) WHERE billed is not true;
```

以下 SQL 查询能够用到以上索引：

```SQL
SELECT * FROM orders WHERE billed is not true AND order_nr < 10000;
SELECT * FROM orders WHERE billed is not true AND amount > 5000.00;
```

## Operator Classes 和 Operator Families

一个索引定义可以为每个索引列定义一个 operator class。

操作符类 text_pattern_ops, varchar_pattern_ops, 和 bpchar_pattern_ops 在 B-tree 索引上相应的支持 text, varchar, char。

可以定义自己的操作符类。

如果使用 C locale，默认的操作符类就足够了。

## Index-Only Scans

PostgreSQL 中所有的索引都是次要索引，意味着每个索引存储与表的主数据区（表堆）分离。这意味着，一个寻常的索引扫描，每一行数据的提取需要从索引和堆中获取。而且，索引扫描进入堆是随机进入的，会很慢，尤其在传统的旋转式介质上。bitmap 扫描试图减轻这个花费通过有序进入，但是远远不能解决问题。

为了解决这个问题，PostgreSQL 支持仅索引扫描。基础想法是只从索引直接获取值，而不去调用堆入口。然而，有两个基础的限制：

1. 索引类型必须支持仅索引扫描。B-tree 总是支持的。GiST 和 SP-GiTST 索引仅支持部分操作符类的仅索引所描，其他的索引类型不支持。底层需要索引必须是物理存储的，或者能够从每个索引入口的原始数据值重构的。因此，GIN 索引不支持仅索引扫描，因为每个索引入口只保存部分原始数据值。

2. 查询只能应用存储在索引中的列。

3. 表的堆页所有的 visible map bits 必须设置。

参考 PostgreSQL 10.10 Documentation Chapter 11.

