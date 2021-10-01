package com.tracholar.demo.feature.dag;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import org.springframework.util.CollectionUtils;

import java.util.LinkedList;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:20
 *
 * 简单执行计算逻辑，如出错忽略直接执行下游节点
 * TODO：节点的并行计算
 */
public class SimpleDagEngine implements IDagEngine{
    @Getter(AccessLevel.PROTECTED)
    @Setter(AccessLevel.PROTECTED)
    private List<INode> nodes = new LinkedList<>();

    private boolean run(INode node, IEngineContext ctx){
        // 跳出条件
        if(ctx.isExecuted(node)){
            return true;
        }

        List<INode> parentNodes = node.getDependenceNode();
        if(!CollectionUtils.isEmpty(parentNodes)) {
            for (INode pNode : parentNodes) {
                run(pNode, ctx);
            }
        }
        ctx.addFinishedNode(node, node.run(ctx));
        return true;
    }
    @Override
    public boolean run(IEngineContext ctx) {
        if(CollectionUtils.isEmpty(nodes)){
            return true;
        }

        for(INode node : nodes){
            run(node, ctx);
        }
        return true;
    }
}
