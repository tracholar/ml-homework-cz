package com.tracholar.demo.utils;

import com.google.common.collect.Lists;
import org.springframework.stereotype.Component;

import java.util.LinkedList;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/3 10:31
 */
@Component
public class MyUtils {
    public <T> List<List<T>> resizeList(List<T> users, int n){
        List<List<T>> resizedUsers = new LinkedList<>();
        for(int i=0; i< Math.ceil(1.0 * users.size() / n); i++){
            List<T> tmp = new LinkedList<>();
            for(int j=i*n; j<users.size() && j<(i+1)*n; j++){
                tmp.add(users.get(j));
            }

            resizedUsers.add(tmp);
        }

        return resizedUsers;
    }

    public String stringFormat(String fmt, Object... args){
        return String.format(fmt, args);
    }

    public String percentFormat(Number number, int n){
        return String.format("%." + n + "f%%", number.doubleValue() *  100);
    }
}

