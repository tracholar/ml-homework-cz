package com.tracholar.hive.udf;

import org.apache.hadoop.hive.ql.exec.UDAF;
import org.apache.hadoop.hive.ql.exec.UDAFEvaluator;


public final class AUC extends UDAF {

    public static class State {
        /** 定义UDAF的状态类, 保存不同阈值下的 TP, TN, FP, FN
         */
        public State(){ }

        public void merge(State s){
            //TODO 实现merge方法, 用于两个状态的merge
        }
        public void clear(){
            //TODO 实现clear方法, 用于reset
        }
    }
    public static class AUCEvaluator implements UDAFEvaluator {

        private State s = new State();

        public AUCEvaluator() {
            super();
            init();
        }

        public void init() {
            s.clear();
        }

        // 该方法对应于udaf使用时 select auc(predict, label)
        public boolean iterate(Integer y, Double value) throws HiveException {
            //TODO 实现增量更新State

            return true;
        }

        public State terminatePartial() {
            return s;
        }

        // 该方法用于合并中间结果
        public boolean merge(State intermediateResult) {
            if(intermediateResult == null) return true;
            s.merge(intermediateResult);
            return true;
        }

        // 该方法对应最后输出最终结果
        public Double terminate() {
            // TODO 用梯形法计算ROC曲线面积
        }
    }
}