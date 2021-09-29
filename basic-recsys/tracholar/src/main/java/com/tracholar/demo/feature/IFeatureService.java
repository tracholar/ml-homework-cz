package com.tracholar.demo.feature;

import com.tracholar.demo.model.Sample;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:43
 *
 * 特征服务，获取item、user等实体的特征列表
 */
public interface IFeatureService{
    /**
     * 获取实体的特征列表
     * @param req
     * @return
     */
    List<Sample> getFeatures(FeatureServiceRequest req);
}
