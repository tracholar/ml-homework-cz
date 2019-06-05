package com.tracholar.hive.udf;

import org.apache.hadoop.hive.ql.exec.UDF;
import java.util.*;

class FeatureNameToId extends UDF {
    /**
     * 将特征名替换成ID
     * @param features 特征KV字符串: fn1:v1,fn2:v2,fn3:v5
     * @param name2id  名字到ID映射: fn1:1,fn2:2,fn3:3
     * @return libsvm格式:  1:v1 2:v2 3:v3
     */
    public String evaluate(String features, String name2id){
        //TODO 实现你的逻辑
        return null;
    }
    public HashMap<String, String> evaluate(HashMap<String, String> features, HashMap<String, String> name2id){
        //TODO 实现你的逻辑
        return null;
    }
}