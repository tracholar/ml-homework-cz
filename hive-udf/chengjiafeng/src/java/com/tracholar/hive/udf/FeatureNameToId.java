package com.tracholar.hive.udf;

import org.apache.hadoop.hive.ql.exec.UDF;

import java.util.*;

class FeatureNameToId extends UDF {
    /**
     * 将特征名替换成ID
     *
     * @param features 特征KV字符串: fn1:v1,fn2:v2,fn3:v5
     * @param name2id  名字到ID映射: fn1:1,fn2:2,fn3:3
     * @return libsvm格式:  1:v1 2:v2 3:v3
     */
    public String evaluate(String features, String name2id) {
        //TODO 实现你的逻辑
        HashMap<String, String> features = new HashMap<String, String>();
        HashMap<String, String> name2id = new HashMap<String, String>();
        for (String feature : features.split(',')) {
            String[] str = feature.split(':');
            String fn = str[0];
            String v = str[1];
            features.put(fn, v);
        }
        for (String nameid : name2id.split(',')) {
            String[] strid = nameid.split(':');
            String name = strid[0];
            String id = strid[1];
            name2id.put(name, id);
        }
        HashMap<String, String> libsvm = evaluate(features, name2id);
        String output="";
        for (Map.Entry<String, String> entry : libsvm.entrySet()){
            output += entry.getKey() + ":" + entry.getValue() + " ";
        }
        return output.trim();
    }

    public HashMap<String, String> evaluate(HashMap<String, String> features, HashMap<String, String> name2id) {
        //TODO 实现你的逻辑
        HashMap<String, String> libsvm = new HashMap<String, String>();
        for (Map.Entry<String, String> entry : features.entrySet()){
            libsvm.put(name2id.get(entry.getKey()), entry.getValue());
        }
        return libsvm;
    }
}