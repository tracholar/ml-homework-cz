package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.job.item.ItemJobResults;

/**
 * @author zuoyuan
 * @date 2021/10/1 12:28
 *
 * item特征生产JOB
 */
public interface IItemJob extends IFeatureJob<FeatureJobContext, ItemJobResults> {
}
