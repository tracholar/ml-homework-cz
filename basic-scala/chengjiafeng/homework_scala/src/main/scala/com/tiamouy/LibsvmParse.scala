package com.tiamouy

/**
  * Created by zuoyuan on 2019/7/23.
  */
object LibsvmParse {
	def parse(line: String) : (Double, Array[Int], Array[Double]) = {
		//TODO 实现parse过程
		val r = line.split(" ")
		val res = r.slice(1, r.length).map(e => {
			val e_split = e.split(":")
			(e_split(0).toInt, e_split(1).toDouble)
		}).unzip
		(r(0).toDouble, res._1, res._2)
	}

	def main(args: Array[String]) {
		val line = Array(
			"1 3:2 5:2 90:2",
			"0",
			"0 5:3"
		)
		//TODO 执行parse,保证没有异常数据
		for(r <-line){
			val (a,b,c) = parse(r)
			print(a)
			print(b.foreach(print))
			print(c.foreach(print))
		}
	}
}

