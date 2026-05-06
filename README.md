# coral-workflow-skill

Coral 前端全流程协作开发技能 — Claude Code Skill

## 概述

从需求分析到测试交付的完整多角色协作工作流。覆盖产品经理、UI/UX设计师、项目经理、开发工程师、测试工程师五大角色，支持从0创建项目和已有项目迭代两种模式。作为 coral-frontend 的上游技能，完成规划后自动交接给 coral-frontend 执行开发。

## 安装

将 `.claude/skills/coral-workflow/` 目录复制到你的项目的 `.claude/skills/` 目录下即可。

## 使用

在 Claude Code 中输入：

```
/coral-workflow
```

或描述你的前端开发需求，技能会自动触发。

## 工作流程

```
阶段0: 项目模式识别（新建 / 迭代）
  ↓
阶段1: 需求分析（产品经理）→ PRD + 原型
  ↓
阶段2: UI/UX 设计（设计师）→ 设计稿 + 规范
  ↓
阶段3: 逻辑梳理与技术方案（架构师）→ 流程图 + 技术选型
  ↓
阶段4: 测试用例编写（测试）→ 完整测试用例
  ↓
阶段5: 任务拆分与分配（项目经理）→ 任务分配总表
  ↓
阶段6: 开发执行（交接 coral-frontend）→ 代码实现
  ↓
阶段7: 功能测试（测试工程师）→ 逐条验证
  ↓
阶段8: 回归测试与交付（项目经理）→ 整体验收
```

## 文件结构

```
.claude/skills/coral-workflow/
├── SKILL.md                              # 主技能定义
└── references/
    ├── prd-template.md                   # PRD 文档模板
    ├── test-case-template.md             # 测试用例模板
    ├── task-assignment-template.md       # 任务分配表模板
    └── progress-snapshot-template.md     # 进度快照模板
```

## 与 coral-frontend 的关系

- **coral-workflow**：上游流程，负责需求分析、设计、规划、任务拆分
- **coral-frontend**：下游执行，负责实际编码、质量检测、风格检测

两者串联使用：coral-workflow 完成规划后，将产出交接给 coral-frontend 执行开发。

## 核心原则

1. 不急于写代码 — 先理清需求，再拆分任务
2. 提问先于产出 — 有疑问就问，不假设答案
3. 测试前置 — 开发前编写测试用例，以测试驱动开发
4. 任务可并行 — 拆分时确保多人可并行无代码冲突
5. 上下文双保险 — 项目文件 + memory 双重持久化

## License

MIT
