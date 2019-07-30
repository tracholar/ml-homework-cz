package com.tracholar.scala.tutorial

/**
  * Created by zuoyuan on 2019/7/23.
  */
object LibsvmParse {
	def asPair(x:String) = (x.split(":")(0).toInt,x.split(":")(1).toDouble)
	def parse(line: String) : (Double, Array[Int], Array[Double]) = {
		//TODO 实现parse过程
		val temp=line.split(" ")
		val (feat,value)=temp.slice(1,temp.length).map(asPair(_)).unzip
		(temp(0).toDouble, feat , value)
	}

	def main(args: Array[String]) {
		val line = Array(
			"1 3:2 5:2 90:2",
			"0",
			"0 5:3"
		)
		//TODO 执行parse,保证没有异常数据
		for(x<-line){
			val (a,b,c)=parse(x)
			println(a)
			for(y<-b){print(y+" ")}
			for(y<-c){print(y+" ")}
			println()
		}
	}
}
