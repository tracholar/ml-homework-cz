package com.tracholar.demo.model;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:53
 */
public interface IPredictRequest {
    /**
     * 获取结果
     * @return
     */
    List<Sample> getItems();
}
