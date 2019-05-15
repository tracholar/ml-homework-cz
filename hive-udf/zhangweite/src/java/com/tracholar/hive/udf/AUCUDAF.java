package com.tracholar.hive.udf;

import org.apache.hadoop.hive.ql.exec.UDAF;
import org.apache.hadoop.hive.ql.exec.UDAFEvaluator;



public final class AUC extends UDAF {

    public static class State {
        /** 定义UDAF的状态类, 保存不同阈值下的 TP, TN, FP, FN
         */
        int[][] st =  new int[4][100];

        public State(){ }

        public void merge(State s){
            //TODO 实现merge方法, 用于两个状态的merge
            for(int i=0;i<4;i++){
                for(int j=0;j<100;j++){
                    self.st[i][j]+=s.st[i][j];
                }
            }
        }
        public void clear(){
            //TODO 实现clear方法, 用于reset
            for(int i=0;i<4;i++){
                for(int j=0;j<100;j++){
                    self.st[i][j]=0;
                }
            }
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
            // tp tn fp fn
            if(y==0){ // tn fp
                for(int j=0;j<100;j++){
                    if(value<j*0.01) s.st[1][j]++;
                    else self.s.st[3][j]++;
                }
            }else{ // tp fn
                for(int j=0;j<100;j++){
                    if(value>j*0.01) s.st[0][j]++;
                    else self.s.st[2][j]++;
                }
            }
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
        // tp tn fp fn
        // TPR=TP/ (TP+ FN)，FPR= FP / (FP + TN)
        public Double terminate() {
            // TODO 用梯形法计算ROC曲线面积
            double res=0, fpr_pre=0;
            for(int k=0;k<100;k++){
                double tpr=self.s.st[k][0]/(self.s.st[k][0]+self.s.st[k][3]);
                double fpr=self.s.st[k][2]/(self.s.st[k][1]+self.s.st[k][3]);
                res+=tpr*(fpr-fpr_pre);
                fpr_pre=fpr;
            }
            return res;
        }
    }
}