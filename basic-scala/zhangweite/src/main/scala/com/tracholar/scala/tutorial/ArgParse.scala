package com.tracholar.scala.tutorial

/**
  * Created by zuoyuan on 2019/7/23.
  */
object ArgParse {
	def parseCmd(args: Array[String]): Map[String, String] = {
		// TODO parse 命令行参数 args
		var map:Map[String,String]=Map()
		var pre:String=""
		for(x <- args.filter(_.size>0)){
			if(x(0)=='-'){
				pre=x.slice(2,x.length)
			}else{
				map+=(pre->x)
			}
		}
		map
	}
	def main(args: Array[String]) {
		val args = Array("--input", "Input file",
			"--output",
			"--mode", "cmd",
			"--user", "demo",
			""
		)
		println(parseCmd(args))
	}
}
