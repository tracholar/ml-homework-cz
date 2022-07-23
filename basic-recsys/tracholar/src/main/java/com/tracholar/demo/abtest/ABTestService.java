package com.tracholar.demo.abtest;

import com.google.gson.Gson;
import com.tracholar.demo.abtest.config.ABTestConfig;
import com.tracholar.demo.abtest.config.ExpRegion;
import com.tracholar.demo.abtest.config.LayerConfig;
import com.tracholar.demo.abtest.config.StrategyConfig;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.InputStreamReader;
import java.io.Reader;

/**
 * @author zuoyuan
 * @date 2021/10/2 15:44
 */
@RestController
@RequestMapping("/abtest")
public class ABTestService implements IABTest{
    private ABTestConfig config;
    public ABTestService(){
        updateConfig();
    }

    // TODO 完成热更新；当前配置文件在jar包内，无法做到热更新，
    //  只要将路径该到jar包外或者外部存储即可
    private void updateConfig(){
        Gson gson = new Gson();
        Reader reader = new InputStreamReader(getClass().getResourceAsStream("/abtest.json"));
        config = gson.fromJson(reader, ABTestConfig.class);
    }

    @RequestMapping("/update")
    public ABTestConfig update(){
        updateConfig();
        return config;
    }

    @RequestMapping("/config")
    public ABTestConfig getConfig(){
        return config;
    }

    private int hash(String flowId, int seed){
        int code = flowId.hashCode();
        if(code < 0){
            code = - code;
        }
        return code % config.getBucketNum();
    }

    @RequestMapping("/query/{flowId}")
    @Override
    public IABTestInfo getABTestInfo(@PathVariable("flowId") String flowId) {

        ABTestInfo info = new ABTestInfo();
        if(flowId == null){
            return info;
        }

        // 试验区，默认是正交实验区
        return config.generateExpInfo(flowId);
    }
}
