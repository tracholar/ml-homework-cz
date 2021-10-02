package com.tracholar.demo.model;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:53
 */
public interface IPredictResponse {
    /**
     * 预测结果，key是uniqueId，sample.uniqueId()
     * @see Sample
     * @return
     */
    Map<String, PredictResult> getResults();
}
