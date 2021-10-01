package com.tracholar.demo.feature.dag;

import org.springframework.util.CollectionUtils;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:20
 *
 * 简单执行计算逻辑，如出错忽略直接执行下游节点
 * TODO：节点的并行计算
 */
public class SimpleEngine implements IDagEngine{

    @Override
    public boolean run(List<INode> nodes) {
        // 跳出条件
        if(CollectionUtils.isEmpty(nodes)){
            return true;
        }

        for(INode node : nodes){
            if(node.isExecuted()){
                continue;
            }

            // 执行依赖的节点
            run(node.getDependenceNode());

            // 执行节点
            node.run();
        }
        return true;
    }
}
