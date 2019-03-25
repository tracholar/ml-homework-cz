package com.tracholar.hive.udf;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDTF;
import org.apache.hadoop.hive.serde2.objectinspector.*;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Writable;

import java.util.ArrayList;
import java.util.List;

/**
 * 实现一个UDTF, 对输入的每一行数据,按照n个一行输出,函数原型是 one_to_many(col1[, col2, ..., colk], n)
 * select one_to_many(col1, col2, col3, col4, col5, col6, 2) as (col1, col2)
 */
public class OneToManyUDTF extends GenericUDTF {
    private static final Log logger = LogFactory.getLog(OneToManyUDTF.class);
    int n = -1;

    @Override
    public StructObjectInspector initialize(ObjectInspector[] argOIs) throws UDFArgumentException {
        //TODO 校验输入参数, 输入为常数可以直接通过 `getWritableConstantValue` 方法获得他的常数值
        //TODO 初始化 n
        // 一些有用的函数
        // - ObjectInspectorUtils.isConstantObjectInspector
        // - ConstantObjectInspector.getWritableConstantValue
        // - PrimitiveObjectInspectorFactory.writableStringObjectInspector


        //TODO 构造输出的 ObjectInspector
        // 一些有用的函数
        // - ObjectInspectorFactory.getStandardStructObjectInspector

    }

    @Override
    public void process(Object[] args) throws HiveException {
        // TODO 实现one to many的逻辑, 使用 this.forward(Object[]) 输出一行
    }

    @Override
    public void close() throws HiveException {
        return;
    }
}
