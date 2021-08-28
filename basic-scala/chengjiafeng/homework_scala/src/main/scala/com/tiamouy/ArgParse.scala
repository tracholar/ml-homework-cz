package com.tiamouy

/**
 * Created by zuoyuan on 2019/7/23.
 */
object ArgParse {
  def parseCmd(args: Array[String]): Map[String, String] = {
    // TODO parse 命令行参数 args
    var res: Map[String, String] = Map()
    var key = ""
    for (arg <- args.filter(_.size > 0)) {
      if (arg(0) == '-') {
        key = arg.slice(2, arg.length)
      } else {
        res += (key -> arg)
      }
    }
    res
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
