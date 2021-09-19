package com.tracholar.hive.udf;

import org.apache.hadoop.hive.ql.exec.UDAF;
import org.apache.hadoop.hive.ql.exec.UDAFEvaluator;

import java.util.Arrays;


public final class AUC extends UDAF {

    public static class State {
        /**
         * 定义UDAF的状态类, 保存不同阈值下的 TP, TN, FP, FN
         */
        public State() {
        }


        int l = 4;
        int n = 10;
        int[][] arrs = new int[l][n];

        public void merge(State s) {
            //TODO 实现merge方法, 用于两个状态的merge
            for (int i = 0; i < s.arrs.length; i++) {
                for (int j = 0; j < s.arrs[0].length; j++) {
                    this.arrs[i][j] += s.arrs[i][j];
                }
            }
        }

        public void clear() {
            //TODO 实现clear方法, 用于reset
            for (int i = 0; i < 4; i++) {
                Arrays.fill(arrs[i], 0);
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
            if (y == 0) {
                for (int j = 0; j < s.arrs[0].length; j++) {
                    if (value < j * 0.01) {
                        s.st[1][j]++;
                    } else {
                        this.s.st[3][j]++;
                    }
                }
            } else {
                for (int j = 0; j < s.arrs[0].length; j++) {
                    if (value > j * 0.01) {
                        s.st[0][j]++;
                    } else {
                        this.s.st[2][j]++;
                    }
                }
            }

            return true;
        }

        public State terminatePartial() {
            return s;
        }

        // 该方法用于合并中间结果
        public boolean merge(State intermediateResult) {
            if (intermediateResult == null) return true;
            s.merge(intermediateResult);
            return true;
        }

        // 该方法对应最后输出最终结果
        // AUC += 0.5 * (TPR + TPR_last) * (FPR - FPR_last);
        // TPR = TP / P = TP / (TP + FN); FPR = FP / N = FP / (TN + FP);
        // TP, TN, FP, FN
        public Double terminate() {
            // TODO 用梯形法计算ROC曲线面积
            Float AUC = 0.0f;
            Float temp_TPR = 0.0f;
            Float temp_FPR = 0.0f;
            for (int i = 0; i < s.arrs[0].length; i++) {
                Float TPR = s.arrs[0][i] * 1.0f / (s.arrs[0][i] + s.arrs[3][i]);
                Float FPR = s.arrs[2][i] * 1.0f / (s.arrs[1][i] + s.arrs[2][i]);
                AUC += 0.5 * (TPR + temp_TPR) * (FPR - temp_TPR);
                temp_FPR = FPR;
                temp_TPR = TPR;
            }
            return AUC;
        }
    }
}