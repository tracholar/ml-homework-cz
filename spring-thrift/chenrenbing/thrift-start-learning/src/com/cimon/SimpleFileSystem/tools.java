package com.cimon.SimpleFileSystem;

import org.apache.thrift.TException;

import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.Paths;

public class tools {
    public static byte[] toByteArray(String filePath){
        /*
        * 把 文件转换成Byte 数组
        * */
        byte[] buffer = null;
        try {
            File file = new File(filePath);
            FileInputStream fis = new FileInputStream(file);
            ByteArrayOutputStream bos = new ByteArrayOutputStream(1000);
            byte[] b = new byte[1000];
            int n;
            while ((n = fis.read(b)) != -1) {
                bos.write(b, 0, n);
            }
            fis.close();
            bos.close();
            buffer = bos.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return buffer;
    }
    public static boolean writeByteBuffer(String filename,ByteBuffer data){
        try
        {
            File file = new java.io.File(filename);
            FileOutputStream fos = new FileOutputStream(file);
            // 值得思考的是，会自动把 byte 输出为 字符。
            FileChannel channel = fos.getChannel();
            channel.write(data);
            channel.close();
        }
        catch (FileNotFoundException x)
        {
            System.out.println(" Erro in function writeByteBuffer "+" FileNotFoundException");
            x.printStackTrace();
            return false;
        }catch(Exception x){
            x.printStackTrace();
            return false;
        }
        return true;
    }
    public static String byte2HexString(byte[] data) {
        //System.out.println(byte2String(bytes).getBytes()[0]);
        char[] hexArray = "0123456789ABCDEF".toCharArray();
        char[] hexChars = new char[data.length * 2];

        for (int j = 0; j < data.length; j++) {
            int v = data[j] & 0xFF;
            hexChars[j * 2] = hexArray[v >>> 4];
            hexChars[j * 2 + 1] = hexArray[v & 0x0F];
        }

        String result = new String(hexChars);
        //result = result.replace(" ", "");
        return result;
    }
    public static void printThriftFile(ThriftFile tf){
        System.out.println("FileName : "+tf.getName());
        System.out.println("\t\tFileMode:"+tf.getFilemode());
        System.out.println("\t\tPath : "+tf.getPath());
        System.out.println("\t\tSize : "+tf.getSize());
        System.out.println("\t\tMime : "+tf.getMime());

    }
    public static ThriftFile getFileInfo(File file) throws TException {

        //System.out.println(file.getClass().getName());
        ThriftFile tf = new ThriftFile();

        tf.filemode= (file.canWrite() ? "canWrite ":"can\'t Write")+","+(file.canRead() ? "canRead":"can\'t Read");
        tf.name=file.getName();
        tf.size=String.valueOf(file.length())+"B";
        try {
            tf.mime = Files.probeContentType(Paths.get(file.getPath()));
        }catch (Exception x)
        {
            x.printStackTrace();
            return null;
        }
        tf.path=file.getPath();
        //System.out.println(file.getPath());
        //System.out.println(" is null "+(tf==null));
        return tf;

    }
}
