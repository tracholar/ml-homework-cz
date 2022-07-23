package com.tracholar.demo.engine.api;

import com.tracholar.demo.api.Request;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:54
 */
@Getter
@Setter
public class ApiRequest implements Request {
    private long uid;
    /**
     * 返回结果数目，默认20
     */
    private int limitSize = 20;
}
