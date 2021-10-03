package com.tracholar.demo.abtest.config;

/**
 * @author zuoyuan
 * @date 2021/10/3 11:26
 */
public class Hash {
    public static int hash(String flowId, int seed){
        byte[] data = flowId.getBytes();
        int code = hash(data, data.length, seed);
        if(code < 0){
            code = - code;
        }
        return code;
    }

    /**
     * 源自 org.apache.hadoop.hadoop-common 包中的 Murmurhash 的代码
     * @param data
     * @param length
     * @param seed
     * @return
     */
    public static int hash(byte[] data, int length, int seed) {
        int m = 1540483477;
        int r = 24;
        int h = seed ^ length;
        int len_4 = length >> 2;

        int len_m;
        int left;
        for(len_m = 0; len_m < len_4; ++len_m) {
            left = len_m << 2;
            int k = data[left + 3];
            k = k << 8;
            k |= data[left + 2] & 255;
            k <<= 8;
            k |= data[left + 1] & 255;
            k <<= 8;
            k |= data[left + 0] & 255;
            k *= m;
            k ^= k >>> r;
            k *= m;
            h *= m;
            h ^= k;
        }

        len_m = len_4 << 2;
        left = length - len_m;
        if (left != 0) {
            if (left >= 3) {
                h ^= data[length - 3] << 16;
            }

            if (left >= 2) {
                h ^= data[length - 2] << 8;
            }

            if (left >= 1) {
                h ^= data[length - 1];
            }

            h *= m;
        }

        h ^= h >>> 13;
        h *= m;
        h ^= h >>> 15;
        return h;
    }
}
