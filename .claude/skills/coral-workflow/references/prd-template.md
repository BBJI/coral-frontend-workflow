# PRD 模板

```markdown
# PRD — {功能名称}

## 1. 背景与目标
- 业务背景
- 目标用户
- 核心价值

## 2. 用户角色与权限
| 角色 | 权限描述 |
|------|---------|
| ...  | ...     |

## 3. 功能清单（按优先级排列）
| 优先级 | 功能点 | 描述 | 备注 |
|--------|-------|------|------|
| P0     | ...   | ...  | ...  |
| P1     | ...   | ...  | ...  |
| P2     | ...   | ...  | ...  |

## 4. 详细功能描述

### 4.1 {功能点1}
- **描述：**
- **输入：**
- **输出：**
- **业务规则：**
- **异常处理：**

### 4.2 {功能点2}
...

## 5. 非功能需求
- 性能要求
- 兼容性要求
- 无障碍要求
- 国际化要求

## 6. 数据模型与接口约定
### 数据模型
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ...  | ...  | ...  | ...  |

### 接口约定
| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| ...  | ...  | ...  | ...  |

## 7. 待确认事项
| 序号 | 事项 | 状态 |
|------|------|------|
| 1    | ...  | 待确认/已确认 |
```

## JSON Schema

```json
{
  "title": "",
  "version": "1.0",
  "background": { "context": "", "targetUsers": "", "coreValue": "" },
  "roles": [{ "name": "", "permissions": "" }],
  "features": [
    {
      "priority": "P0",
      "name": "",
      "description": "",
      "details": { "input": "", "output": "", "rules": [], "exceptions": [] }
    }
  ],
  "nonFunctional": { "performance": "", "compatibility": "", "accessibility": "", "i18n": "" },
  "dataModel": [{ "field": "", "type": "", "required": false, "description": "" }],
  "interfaces": [{ "name": "", "method": "", "path": "", "description": "" }],
  "pendingItems": [{ "id": 1, "item": "", "status": "pending" }]
}
```
