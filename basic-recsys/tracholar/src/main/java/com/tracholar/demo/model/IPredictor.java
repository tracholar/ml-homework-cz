package com.tracholar.demo.model;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:53
 *
 * 模型打分预测器
 */
public interface IPredictor {
    /**
     * 模型打分接口
     * @param request
     * @return
     */
    IPredictResponse predict(IPredictRequest request);
}
