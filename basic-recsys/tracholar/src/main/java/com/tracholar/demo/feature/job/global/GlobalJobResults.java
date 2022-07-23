package com.tracholar.demo.feature.job.global;

import com.tracholar.demo.feature.job.IJobResults;

import java.util.HashMap;

/**
 * @author zuoyuan
 * @date 2021/10/1 16:44
 */
public class GlobalJobResults extends HashMap<String, Object>
        implements IJobResults<GlobalJobResults> {

    @Override
    public void merge(GlobalJobResults r) {
        this.putAll(r);
    }
}
