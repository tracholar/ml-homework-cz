package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.job.global.GlobalJobResults;

/**
 * @author zuoyuan
 * @date 2021/10/1 12:27
 *
 * 全局特征JOB，用于user、context特征抽取
 */
public interface IGlobalJob extends IFeatureJob<FeatureJobContext, GlobalJobResults> {
}
