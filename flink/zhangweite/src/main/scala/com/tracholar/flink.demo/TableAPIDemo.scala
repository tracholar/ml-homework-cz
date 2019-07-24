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
			//TODO 实现UDF
			str.split(sep)(0)
		}
	}

	def main(args: Array[String]) {
		val env = ExecutionEnvironment.getExecutionEnvironment
		val tEnv = BatchTableEnvironment.create(env)

		// TODO 从csv文件创建数据表并注册到环境
		val catalog: ExternalCatalog = new InMemoryExternalCatalog("log")
		val table = CsvTableSource.builder()
			.path(getClass.getResource("/order.csv").getPath)
			.field("uid", Types.STRING)
			.field("cnt", Types.INT)
			.build()

		// TODO 注册UDF spliter
		tEnv.registerTableSource("Orders", table)
		tEnv.registerFunction("mysplit", new Spliter("#"))

		// TODO 用table api 和 SQL 两种方式实现csv表中数据统计,并使用注册的UDF spliter





		val orders = tEnv.scan("Orders")
		val result = orders.groupBy('uid)
			.select('uid, 'cnt.sum as 'cnt)
			.toDataSet[Row].print()

		print(">>>>>>>>>>>>>>>>>>>")

		val result2 = tEnv.sqlQuery(
			"""
							  |select mysplit(uid) as len, sum(cnt) as cnt
							  |from Orders
							  |group by mysplit(uid)
						""".stripMargin)
			.toDataSet[Row].print()

	}
}
