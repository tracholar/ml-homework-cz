package com.tracholar.scala.tutorial

/**
  * Created by zuoyuan on 2019/7/23.
  */
object WordCountDemo {
	def dataset = Range(0, 100).map(_ => HelloWorld.randString).mkString(" ")

	def main(args: Array[String]) {
		// TODO 实现word count
//		print(dataset)
		val res=dataset.split(" ").map((_,1)).groupBy(_._1).mapValues(_.size).toList.sortBy(_._2).reverse
		print(res)
	}
}
