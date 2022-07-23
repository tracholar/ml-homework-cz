package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.job.item.ItemJobResults;

/**
 * @author zuoyuan
 * @date 2021/10/1 16:44
 */
public interface IJobResults<T extends IJobResults> {
    /**
     * 跟其他job的结果合并
     * @param r
     */
    void merge(T r);
}
