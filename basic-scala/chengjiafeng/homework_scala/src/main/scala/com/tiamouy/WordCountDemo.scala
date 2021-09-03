package com.tiamouy

/**
  * Created by zuoyuan on 2019/7/23.
  */
object WordCountDemo {
	def dataset = Range(0, 10000).map(_ => HelloWorld.randString(1)).mkString(" ")

	def main(args: Array[String]) {
		// TODO 实现word count
		val res = dataset.split(" ").map((_,1)).groupBy(_._1).map(r => (r._1, r._2.size))
		for ((key, value) <- res) {
			println("string is " + key + ", num is " + value)
		}
	}
}
