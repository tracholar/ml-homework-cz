package com.tracholar.demo.api;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:28
 *
 * 推荐API
 */
public interface RecsysApi {
    /**
     * 获取推荐结果列表
     * @param req
     * @return
     */
    Response recommend(Request req);
}
