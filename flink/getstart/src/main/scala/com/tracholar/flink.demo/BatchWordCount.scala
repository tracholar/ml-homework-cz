package com.tracholar.flink.demo

import org.apache.flink.api.scala._

/**
  * Created by zuoyuan on 2019/7/12.
  */
object BatchWordCount {
	def main(args: Array[String]) {
		val env = ExecutionEnvironment.getExecutionEnvironment
		val text = env.fromElements("Who's there?",
			"I think I hear them. Stand, ho! Who's there?")
		//TODO 实现word count,并打印,你可能需要了解dataset api https://ci.apache.org/projects/flink/flink-docs-release-1.8/dev/batch/
		val number = text.flatMap(_.toLowerCase.split("\\W+")).filter(_!= null).map((_,1)).groupBy(0).sum(1)
		text.print()
		number.print()
	}
}
