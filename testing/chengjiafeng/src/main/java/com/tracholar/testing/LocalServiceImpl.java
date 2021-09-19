package com.tracholar.testing;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class LocalServiceImpl {
    private ServiceA remoteService;

    public Node getRemoteNode(int num) {
        return remoteService.getRemoteNode(num);
    }
}
