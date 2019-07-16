package com.tracholar.flink.demo

import org.apache.flink.api.scala._
import org.apache.flink.table.api.scala._
import org.apache.flink.table.catalog.{ExternalCatalog, InMemoryExternalCatalog}
import org.apache.flink.types.Row

/**
  * Created by zuoyuan on 2019/7/15.
  */
object TableAPIDemo {
	def main(args: Array[String]) {
		val env = ExecutionEnvironment.getExecutionEnvironment
		val tEnv = BatchTableEnvironment.create(env)

		val catalog: ExternalCatalog = new InMemoryExternalCatalog("log")
		tEnv.registerExternalCatalog("Orders", catalog)

		val orders = tEnv.scan("Orders")
		val result = orders.groupBy('a)
		    .select('a, 'b.count as 'cnt)
		    .toDataSet[Row]
		    .print()
	}
}
