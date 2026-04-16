# LangGraph工业级从零设计蓝图

适用范围：在空目录从0到1设计“多Agent内容生产系统（以小说/长文生成为例）”。
目标：不是写Demo，而是直接按可上线、可扩展、可审计、可回放的工业标准规划。

---

## 1. 设计目标与边界

### 1.1 目标

1. 可控编排：所有流程用有向状态图描述，可视化、可追踪。
2. 强约束调用：工具调用与函数调用全部Schema化，拒绝自由文本协议。
3. 可靠运行：支持重试、断点恢复、幂等、防重复执行。
4. 可观测：节点级日志、耗时、Token、错误类型、重试次数完整采集。
5. 可扩展：新增Agent/Tool不破坏主流程。

### 1.2 非目标

1. 不追求“首版就全自动无人工介入”。
2. 不追求“所有节点并行”。优先确定性和稳定性。
3. 不追求“模型自由发挥”。优先可验证输出。

---

## 2. 顶层架构（建议）

## 2.1 分层

1. Orchestration层：LangGraph状态图、路由、重试策略。
2. Agent层：规划、检索、写作、评审、修订。
3. Tool层：检索、存储、去重、规则检查、导出、审计。
4. Memory/State层：共享状态、检查点、事件日志、版本控制。
5. Infra层：模型网关、队列、监控、配置中心、权限。

## 2.2 推荐目录

```text
wen_ben/
  src/
    graph/
      state.py
      nodes/
      routes.py
      subgraphs/
    agents/
    tools/
      retrieval/
      quality/
      storage/
      safety/
    domain/
      schemas/
      policies/
    infra/
      llm_gateway.py
      telemetry.py
      idempotency.py
      locks.py
  tests/
    unit/
    integration/
    replay/
  docs/
  artifacts/
    checkpoints/
    outputs/
    traces/
```

---

## 3. LangGraph如何编排

## 3.1 先定State，再定Node

工业实践里最容易踩坑：先写Node，最后才补State，导致字段失控。
正确顺序：
1. 冻结GraphState（字段、类型、版本）。
2. 定义每个Node输入/输出契约。
3. 再定义Edge条件。

## 3.2 GraphState建议字段

```python
class GraphState(TypedDict):
    meta: dict                  # trace_id, project_id, run_id, state_version
    request: dict               # 用户需求、约束、目标长度、风格
    plan: dict                  # 任务分解、阶段目标、依赖
    context: dict               # 检索结果、历史摘要、缓存
    draft: dict                 # 当前章节草稿与历史版本
    quality: dict               # 评分、问题、修复建议
    tool_calls: list            # 工具调用记录（含idempotency_key）
    errors: list                # 错误事件
    control: dict               # 重试次数、路由标记、终止信号
    outputs: dict               # 最终产物索引
```

关键约束：
1. 仅允许Node通过“补丁（patch）”更新状态，不允许整对象覆盖。
2. 每次更新必须附带state_version（CAS模式）。
3. 任意节点都不能直接删除历史，只能追加事件。

## 3.3 主流程图（建议）

```text
START
 -> normalize_request
 -> plan_project
 -> build_outline
 -> build_characters
 -> build_world
 -> plan_chapters
 -> for_each_chapter_subgraph
 -> assemble_book
 -> final_review
 -> export_outputs
 -> END
```

章节子图（for_each_chapter_subgraph）：
```text
chapter_prepare
 -> retrieve_context
 -> write_draft
 -> quality_review
 -> route:
    pass -> chapter_commit
    fail_and_retryable -> revise_draft -> quality_review
    fail_non_retryable -> human_gate
```

## 3.4 路由规则

1. 路由条件必须基于结构化字段，不基于模型自由文本。
2. 每条边定义最大重试次数与退避策略。
3. 到达human_gate的条件必须可解释（例如连续2次低于阈值）。

---

## 4. Tool需要哪些（工业清单）

按能力域拆分，建议至少具备以下工具：

## 4.1 检索类

1. search_vector_context：向量检索上下文。
2. fetch_recent_chapters：取最近章节摘要。
3. fetch_entity_memory：取角色/设定记忆。

## 4.2 质量类

1. check_fact_consistency：设定一致性检查。
2. check_character_consistency：角色行为一致性。
3. detect_duplication：重复段落/语义重复检测。
4. score_content_quality：结构化评分。

## 4.3 存储类

1. save_draft_version：保存草稿版本。
2. load_checkpoint：恢复检查点。
3. commit_chapter：提交章节并冻结版本。
4. append_event_log：写审计日志。

## 4.4 安全与治理类

1. validate_tool_args：参数Schema校验。
2. rate_limit_guard：调用频率控制。
3. policy_guard：内容/策略合规检查。

## 4.5 工具设计原则

1. 必须纯函数化输入输出（尽量无隐式副作用）。
2. 必须返回统一错误码（如VALIDATION_ERROR/TIMEOUT/CONFLICT）。
3. 必须支持幂等键（idempotency_key）。
4. 必须记录耗时、输入摘要、输出摘要。

---

## 5. Function Call如何设计

## 5.1 协议骨架

每次函数调用都要有统一Envelope：

```json
{
  "call_id": "uuid",
  "idempotency_key": "chapter3_write_v2",
  "tool_name": "save_draft_version",
  "arguments": {},
  "trace_id": "...",
  "state_version": 17,
  "timestamp": "2026-04-16T12:00:00Z"
}
```

## 5.2 参数约束

1. arguments必须对应JSON Schema并先校验后执行。
2. 关键字段设置枚举和长度上限（避免超长污染状态）。
3. 可选字段明确默认值，禁止工具内部“猜测参数”。

## 5.3 返回约束

```json
{
  "call_id": "uuid",
  "status": "ok|error|duplicate|conflict",
  "error_code": "",
  "result": {},
  "state_patch": {},
  "metrics": {"latency_ms": 120}
}
```

必须要求：
1. 成功时返回state_patch，不直接改全局状态。
2. 失败时返回结构化error_code与retryable标记。
3. duplicate/conflict要可区分。

---

## 6. 无效调用/重复调用怎么解决

## 6.1 无效调用（参数错、前置条件不满足）

处理策略：
1. 预执行校验：Schema + 业务前置条件。
2. 快速失败：返回VALIDATION_ERROR，不进入真实执行。
3. 自动修复：可定义“参数修复器”节点，只修一次，防止死循环。
4. 连续无效调用阈值：超过阈值直接转human_gate。

## 6.2 重复调用（模型抖动重复触发）

处理策略：
1. 幂等键：同idempotency_key只允许一次生效。
2. 调用指纹：tool_name + 参数哈希 + 窗口时间去重。
3. 状态机约束：节点只在特定phase允许调用特定工具。
4. 结果复用：识别重复后直接返回历史结果，不再执行。

## 6.3 防“空转循环”

典型症状：review->revise->review无限循环。
解决：
1. 设最大回环次数。
2. 设最小改进阈值（例如评分提升<0.2视为无提升）。
3. 连续无提升触发early_stop或human_gate。

---

## 7. 共享状态怎么设计

## 7.1 状态更新模型

推荐“事件溯源 + 快照”混合模式：
1. 每次节点执行写事件（append-only）。
2. 周期性生成快照用于恢复。
3. 回放时先读最近快照再重放事件。

## 7.2 状态更新接口

统一API：
1. read_state(run_id) -> state, version
2. apply_patch(run_id, expected_version, patch) -> new_version
3. append_event(run_id, event)

这样可实现乐观并发控制（CAS）：
- expected_version不匹配时返回CONFLICT，节点自动重读并重试。

## 7.3 字段所有权

必须定义“字段写入所有权”，例如：
1. plan.* 仅plan类节点可写。
2. quality.* 仅评审节点可写。
3. outputs.* 仅提交/导出节点可写。

这能显著降低并发写冲突。

---

## 8. 多Agent并发写同一状态怎么解决

## 8.1 核心原则：单写者优先

工业上最稳妥的是“Single Writer per Aggregate”：
1. 同一聚合（例如chapter_3）同一时刻只允许一个Writer节点提交。
2. 其他节点并发计算可以做，但提交要串行。

## 8.2 三种并发控制方案

### 方案A：悲观锁（强一致）

- 提交前加分布式锁（按chapter_id）。
- 优点：简单直观。
- 缺点：吞吐受限，锁超时处理复杂。

### 方案B：乐观锁CAS（推荐）

- 每次提交带expected_version。
- 冲突则重读状态并merge后重试。
- 优点：吞吐高，适合AI工作流。
- 缺点：需要良好merge策略。

### 方案C：CRDT/OT（复杂高阶）

- 用于多人实时协同编辑场景。
- 对当前Agent编排通常过重，不建议首版采用。

## 8.3 冲突合并策略

建议按字段类型处理：
1. append型字段（events/tool_calls/errors）：直接追加。
2. map型字段（quality_scores）：按时间戳或优先级覆盖。
3. 文本型字段（draft.content）：禁止自动盲合并，采用“候选版本+评审选择”。

---

## 9. 工业常见坑与难点（重点）

## 9.1 架构层坑

1. 把Agent当服务，不做状态契约，后期不可维护。
2. 把Prompt当协议，缺Schema导致线上脆弱。
3. 节点职责不清，出现“万能节点”。

## 9.2 运行层坑

1. 工具超时未隔离，拖垮整图。
2. 重试无幂等，造成重复写入。
3. 缺回放能力，线上问题无法复现。

## 9.3 数据层坑

1. 状态对象越长越大，序列化/反序列化成本爆炸。
2. 不做分层缓存，RAG检索成本飙升。
3. 输出不版本化，难以溯源“哪个版本生成了这个结果”。

## 9.4 质量层坑

1. 仅靠主观评审，缺客观指标。
2. 没有最小改进阈值，陷入无效迭代。
3. 审核提示词漂移，评分口径不一致。

## 9.5 组织协作坑

1. 文档与代码不同步。
2. 缺ADR（架构决策记录），团队认知分裂。
3. 缺发布门禁，改动直接上线。

---

## 10. 工程治理与上线门禁

## 10.1 可观测性

必须采集：
1. 节点级：开始/结束时间、输入摘要、输出摘要、错误码。
2. 模型级：Token、延迟、成功率、重试次数。
3. 工具级：调用频率、失败率、重复调用率。

## 10.2 测试体系

1. 单元测试：每个工具的Schema与错误分支。
2. 集成测试：关键子图端到端。
3. 回放测试：线上失败trace可重放。
4. 回归基线：固定输入必须达到最低质量分。

## 10.3 发布策略

1. 灰度发布：新图仅部分流量。
2. 双轨比对：新旧流程并行评估。
3. 一键回滚：切回稳定图版本。

---

## 11. 从零落地实施计划（建议4周）

第1周：基础设施与契约
1. 冻结GraphState与Schema。
2. 搭建工具注册中心与统一Envelope。
3. 建立幂等与冲突控制组件。

第2周：主流程子图
1. 完成请求->规划->章节子图->导出主链。
2. 接入检查点与回放。
3. 打通最小可运行样例。

第3周：质量与治理
1. 接入评审/修订闭环与early_stop。
2. 接入监控指标与告警。
3. 建立回归基线样本。

第4周：稳定化与灰度
1. 压测并优化热点节点。
2. 灰度发布和双轨评估。
3. 输出运维手册与故障SOP。

---

## 12. 最小可行工业标准（MVP-Industrial）

若资源有限，至少保证以下8项：
1. 显式LangGraph状态图（非脚本串联）。
2. GraphState版本化与字段所有权。
3. Tool/Function Call全部Schema化。
4. 幂等键与重复调用去重。
5. 乐观锁CAS或等价并发控制。
6. 检查点与失败回放。
7. 质量阈值与early_stop。
8. 监控+告警+回滚闭环。

做到这8项，项目就具备工业可持续演进基础；其余优化可按业务节奏逐步补齐。
