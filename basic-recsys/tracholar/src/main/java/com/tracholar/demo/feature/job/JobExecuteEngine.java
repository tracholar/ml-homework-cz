package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.IEngineContext;
import com.tracholar.demo.feature.dag.SimpleDagEngine;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

import java.util.*;

/**
 * @author zuoyuan
 * @date 2021/10/1 21:46
 *
 * 特征Job执行引擎
 */
@Component
public class JobExecuteEngine extends SimpleDagEngine implements InitializingBean {
    private void init(Collection<IFeatureJob> jobs) throws Exception{
        Map<String, IFeatureJob> feat2Job = new HashMap<>();
        for(IFeatureJob job : jobs){
            List<String> featNames = job.getOutputNames();
            for(String name : featNames){
                if(feat2Job.containsKey(name)){
                    throw new Exception("特征" + name + "存在多个Job生产逻辑");
                }
                feat2Job.put(name, job);
            }
        }

        // 添加依赖节点
        for(IFeatureJob job : jobs){
            List<String> parents = job.getDependence();
            if(CollectionUtils.isEmpty(parents)){
                continue;
            }
            for(String name : parents){
                if(!feat2Job.containsKey(name)){
                    throw new Exception("无法找到 Job " + job.getClass().getSimpleName()
                        + " 的上游依赖" + name );
                }
                job.addDependence(feat2Job.get(name));
            }
        }

        // TODO: 检查是否循环依赖
    }

    public JobEngineResults run(FeatureJobContext ctx){
        super.run(ctx);
        return ctx.getResults();
    }

    @Autowired
    private ApplicationContext context;
    @Override
    public void afterPropertiesSet() throws Exception {
        Map<String, IFeatureJob> jobsMap = context.getBeansOfType(IFeatureJob.class);
        Collection<IFeatureJob> jobs = jobsMap.values();
        init(jobs);
        super.getNodes().addAll(jobs);
    }
}
