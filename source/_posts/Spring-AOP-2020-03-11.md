---
title: Spring-AOP
tags:
  - Spring-AOP
  - AOP
  - 切面
  - Spring-切面
categories:
  - Spring-AOP
  - Spring
  - AOP
date: 2020-03-11 19:51:19
---

面向切面编程是对面向对象编程的一种补充，提供了另一种编程结构的方式。切面允许关注点的模块化(例如：日志，事务，安全)，能够跨多种类型和对象。

<!-- more -->

以下是一个日志切面实现：

```Java
import com.alibaba.fastjson.JSON;
import io.swagger.annotations.ApiOperation;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

@Aspect
@Component
public class LoggingAspect implements Ordered {
    private static final Logger loggingAspectLogger = LoggerFactory.getLogger("LoggingAspect");

    @Pointcut("@annotation(org.springframework.web.bind.annotation.RequestMapping)")
    private void anyRequest() {
    }

    @Pointcut("@annotation(io.swagger.annotations.ApiOperation)")
    private void anySwaggerApiOperation() {
    }

    /**
     * 打印日志，请求参数，返回结果，接口耗时
     */
    @Around("anyRequest() || anySwaggerApiOperation()")
    public Object logging(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Class clazz = signature.getDeclaringType();
        Logger logger = getLogger(clazz);
        Method method = signature.getMethod();
        String methodName = method.getName();

        if (args.length > 0) {
            logger.info("************* {} begin, request parameters : {}", methodName, args);
        }

        long beginTicks = System.currentTimeMillis();
        Object responseDto = joinPoint.proceed();
        long timeCost = System.currentTimeMillis() - beginTicks;

        ApiOperation apiOperation = method.getAnnotation(ApiOperation.class);
        logger.info("************* {} end, result : {}", methodName, JSON.toJSONString(responseDto));
        logger.info("{}-[{}] Interface Time Cost: {} ms", methodName, apiOperation.value(), timeCost);

        return responseDto;
    }

    /**
     * 获取 Logger 实体域
     *
     * @param clazz
     * @return
     */
    private Logger getLogger(Class clazz) {
        Field[] declaredFields = clazz.getDeclaredFields();
        Logger logger = null;

        for (Field field : declaredFields) {
            if (field.getType() == Logger.class) {
                field.setAccessible(true);
                try {
                    logger = (Logger) field.get(field.getName());
                } catch (IllegalAccessException e) {
                    loggingAspectLogger.error(e.getMessage());
                }
            }
        }
        if (logger == null) {
            logger = LoggerFactory.getLogger(clazz);
        }
        return logger;
    }

    @Override
    public int getOrder() {
        return 10;
    }
}

```

## Advice 类型

`@Before, @AfterReturning, @AfterThrowing, @After, @Around`

## 切面顺序

标记切面顺序有两种方式：1. 添加 `@Order` 标记；2. 实现 `org.springframework.core.Ordered` 接口。

## 参考

1. [Aspect Oriented Programming with Spring][0]

[0]: https://docs.spring.io/spring-framework/docs/current/spring-framework-reference/core.html#aop