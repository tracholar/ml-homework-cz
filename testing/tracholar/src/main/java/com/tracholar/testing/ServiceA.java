package com.tracholar.testing;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class ServiceA {
    private ServiceB serviceB = new ServiceB();

    public int method () {
        return serviceB.check();
    }

    public Node getRemoteNode(int num){
        Node node = new Node();
        node.setNum(num);
        return node;
    }
}
