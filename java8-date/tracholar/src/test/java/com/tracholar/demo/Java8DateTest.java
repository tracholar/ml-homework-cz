package com.tracholar.demo;

import org.junit.Test;

import java.time.LocalDate;
import java.time.Period;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.time.temporal.TemporalUnit;
import java.util.Date;

/**
 * @author zuoyuan
 * @date 2022/8/17 20:13
 */
public class Java8DateTest {
    @Test
    public void test(){
        LocalDate today = LocalDate.now();
        System.out.println(today);

        LocalDate thisday = LocalDate.of(1991, 1, 1);
        System.out.println(thisday);

        today.plusDays(10);
        today.plusMonths(2);

        Period p = Period.between(today, thisday);
        System.out.println(p.getDays());

        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        System.out.println(LocalDate.parse("2022-10-01", fmt));
    }
}
