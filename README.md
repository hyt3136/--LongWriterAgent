# wen_ben

LangGraph 单模型串行编排工程与课程化文档项目。

## 目录

- code/: 可运行源码与测试
- md/: 课程章节文档（代码解析、知识点、记录）
- docs/: 工程架构与运维文档
- artifacts/: 运行产物目录
- scripts/: 自动化脚本

## 快速验证

在 PowerShell 中执行：

```powershell
Set-Location .\code
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -p "test_*.py"
```
