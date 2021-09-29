package com.tracholar.demo.api;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:29
 *
 * 推荐的响应
 */
public interface Response {
    /**
     * 获取推荐结果列表
     * @return
     */
    List<Item> getResults();
}
