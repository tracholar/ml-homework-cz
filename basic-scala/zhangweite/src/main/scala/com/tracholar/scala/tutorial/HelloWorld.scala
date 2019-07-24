package com.tracholar.scala.tutorial

object HelloWorld {
	def randString : String = {
		// TODO 实现一个随机字符串
		""
//		scala.util.Random.nextInt(100).toString
		scala.util.Random.alphanumeric.take(2).mkString("")
	}
	def main(args: Array[String]) {
		// TODO 修改name为一个
		val name = randString;
		println("Hello World! " + name)
	}
}