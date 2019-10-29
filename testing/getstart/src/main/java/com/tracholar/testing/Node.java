package com.tracholar.testing;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class Node {
    public Node(){

    }
    public Node(int num, String name) {
        this.num = num;
        this.name = name;
    }

    public int getNum() {
        return num;

    }

    public void setNum(int num) {
        this.num = num;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    private int num;
    private String name;
}
