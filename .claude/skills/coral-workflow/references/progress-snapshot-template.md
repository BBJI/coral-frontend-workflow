# 进度快照模板

```markdown
# 项目进度快照

## 基本信息
- 项目名称：
- 项目模式：A-新建 / B-迭代
- 当前阶段：阶段X — {阶段名称}
- 最后更新时间：

## 阶段完成情况
- [ ] 阶段0：项目模式识别
- [ ] 阶段1：需求分析
- [ ] 阶段2：UI/UX设计
- [ ] 阶段3：逻辑梳理与技术方案
- [ ] 阶段4：测试用例编写
- [ ] 阶段5：任务拆分与分配
- [ ] 阶段6：开发执行
- [ ] 阶段7：功能测试
- [ ] 阶段8：回归测试与交付

## 任务分配表状态
| 任务ID | 任务名称 | 指派开发者 | 进度状态 |
|--------|---------|-----------|---------|
| ...    | ...     | ...       | ...     |

## 测试用例状态
| 用例ID | 用例标题 | 优先级 | 测试结果 |
|--------|---------|--------|---------|
| ...    | ...     | ...    | ...     |

## 待处理事项
### 疑问
- ...

### Bug
- ...

## 关键决策记录
| 决策 | 选项 | 选择 | 原因 |
|------|------|------|------|
| ...  | ...  | ...  | ...  |
```

## JSON Schema

```json
{
  "projectName": "",
  "projectMode": "A",
  "currentPhase": 0,
  "currentPhaseName": "",
  "lastUpdated": "",
  "phases": [
    { "id": 0, "name": "项目模式识别", "completed": false },
    { "id": 1, "name": "需求分析", "completed": false },
    { "id": 2, "name": "UI/UX设计", "completed": false },
    { "id": 3, "name": "逻辑梳理与技术方案", "completed": false },
    { "id": 4, "name": "测试用例编写", "completed": false },
    { "id": 5, "name": "任务拆分与分配", "completed": false },
    { "id": 6, "name": "开发执行", "completed": false },
    { "id": 7, "name": "功能测试", "completed": false },
    { "id": 8, "name": "回归测试与交付", "completed": false }
  ],
  "taskStatus": [],
  "testCaseStatus": [],
  "pendingItems": { "questions": [], "bugs": [] },
  "decisions": []
}
```
