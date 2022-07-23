package com.tracholar.demo.feature.feature;

import com.tracholar.demo.feature.IFeature;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.util.StringUtils;

/**
 * @author zuoyuan
 * @date 2021/9/29 21:02
 *
 * 简单特征
 */
@Data
@AllArgsConstructor
public class SimpleFeature implements IFeature {
    private String name;
    private Object value;

    public static SimpleFeature EMPTY_FEATURE =
            new SimpleFeature("EMPTY", "");

    public boolean isEmpty(){
        return StringUtils.isEmpty(value);
    }
    public String stringValue(){
        if(value != null){
            return value.toString();
        }
        return "";
    }

    public long longValue(){
        if(isEmpty()){
            return 0;
        }
        try {
            return Long.valueOf(value.toString());
        }catch (Exception ex){
            return 0;
        }
    }

    public float floatValue(){
        if(isEmpty()){
            return 0.0f;
        }
        try {
            return Float.valueOf(value.toString());
        }catch (Exception ex){
            return 0.0f;
        }
    }
}
