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
		}
	}

	def main(args: Array[String]) {
		val env = ExecutionEnvironment.getExecutionEnvironment
		val tEnv = BatchTableEnvironment.create(env)

		// TODO 从csv文件创建数据表并注册到环境

		// TODO 注册UDF spliter

		// TODO 用table api 和 SQL 两种方式实现csv表中数据统计,并使用注册的UDF spliter
	}
}
