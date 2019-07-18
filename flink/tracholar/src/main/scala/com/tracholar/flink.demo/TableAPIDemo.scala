package com.tracholar.flink.demo

import org.apache.flink.api.scala._
import org.apache.flink.table.api.scala._
import org.apache.flink.table.catalog.{ExternalCatalog, InMemoryExternalCatalog}
import org.apache.flink.table.sources.CsvTableSource
import org.apache.flink.types.Row
import org.apache.flink.api.common.typeinfo.Types
import org.apache.flink.table.functions.{ScalarFunction, TableFunction}

/**
  * Created by zuoyuan on 2019/7/15.
  */
object TableAPIDemo {

	class Spliter(val sep: String) extends ScalarFunction{
		def eval(str:String) = {
			str.split(sep).head
		}
	}

	def main(args: Array[String]) {
		val env = ExecutionEnvironment.getExecutionEnvironment
		val tEnv = BatchTableEnvironment.create(env)

		val catalog: ExternalCatalog = new InMemoryExternalCatalog("log")
		val table = CsvTableSource.builder()
		    .path(getClass.getResource("/order.csv").getPath)
		    .field("uid", Types.STRING)
		    .field("cnt", Types.INT)
		    .build()

		tEnv.registerTableSource("Orders", table)
		tEnv.registerFunction("mysplit", new Spliter("#"))

		val orders = tEnv.scan("Orders")
		val result = orders.groupBy('uid)
		    .select('uid, 'cnt.sum as 'cnt)
		    .toDataSet[Row]
		    .print()
		val result2 = tEnv.sqlQuery(
			"""
			  |select mysplit(uid) as len, sum(cnt) as cnt
			  |from Orders
			  |group by mysplit(uid)
			""".stripMargin)
		    .toDataSet[Row]
		    .print()

		env.execute(getClass.getName)
	}
}
