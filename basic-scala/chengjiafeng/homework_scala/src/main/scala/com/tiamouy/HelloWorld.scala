package com.tiamouy

import scala.util.Random

object HelloWorld {
	def randString(size: Int) : String = {
		// TODO 实现一个随机字符串
		""
		Random.alphanumeric.take(size).mkString
	}
	def main(args: Array[String]) {
		// TODO 修改name为一个
		val name = randString(10);
		println("Hello World! " + name)
	}
}