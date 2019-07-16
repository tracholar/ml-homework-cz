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
		val counts = text.flatMap(_.toLowerCase.split("\\W+").filter(_.nonEmpty))
		    .map((_, 1))
		    .groupBy(0)
		    .sum(1)

		counts.print()
	}
}
