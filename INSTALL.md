# 安装说明

## 一行命令安装（推荐）

在任意终端中复制粘贴以下命令即可完成安装：

### Bash / Git Bash

```bash
git clone --depth 1 https://github.com/BBJI/coral-frontend-workflow.git /tmp/cfw && python /tmp/cfw/scripts/install.py && rm -rf /tmp/cfw
```

### PowerShell

```powershell
git clone --depth 1 https://github.com/BBJI/coral-frontend-workflow.git $env:TEMP\cfw; python $env:TEMP\cfw\scripts\install.py; ri -r -fo $env:TEMP\cfw
```

### CMD

```cmd
git clone --depth 1 https://github.com/BBJI/coral-frontend-workflow.git "%TEMP%\cfw" && python "%TEMP%\cfw\scripts\install.py" && rmdir /s /q "%TEMP%\cfw"
```

### 使用 SSH（适合已配置 SSH 密钥的用户）

```bash
# Bash / Git Bash
git clone --depth 1 git@github.com:BBJI/coral-frontend-workflow.git /tmp/cfw && python /tmp/cfw/scripts/install.py && rm -rf /tmp/cfw

# PowerShell
git clone --depth 1 git@github.com:BBJI/coral-frontend-workflow.git $env:TEMP\cfw; python $env:TEMP\cfw\scripts\install.py; ri -r -fo $env:TEMP\cfw

# CMD
git clone --depth 1 git@github.com:BBJI/coral-frontend-workflow.git "%TEMP%\cfw" && python "%TEMP%\cfw\scripts\install.py" && rmdir /s /q "%TEMP%\cfw"
```

> **原理**：命令会临时克隆仓库到临时目录，运行安装脚本，安装完成后自动清理临时目录。

---

## 方法 2：从已克隆的仓库安装

如果已经手动克隆了仓库：

```bash
cd coral-frontend-workflow
python scripts/install.py
```

## 方法 3：使用 --clone 自动克隆安装

```bash
# HTTPS
python scripts/install.py --clone

# SSH
python scripts/install.py --clone --ssh

# 指定仓库 URL
python scripts/install.py --clone --repo <URL>
```

---

## 安装脚本做了什么

1. 将仓库同步到 `~/.claude/plugins/marketplaces/coral-frontend-workflow/`
2. 设置插件缓存到 `~/.claude/plugins/cache/coral-frontend-workflow/`
3. 注册到 `known_marketplaces.json`
4. 注册到 `installed_plugins.json`
5. 更新 `settings.json`（`enabledPlugins` + `extraKnownMarketplaces`）

---

## 验证安装

安装完成后，在 Claude Code 中输入：

```
/coral-workflow
```

如果技能正常工作，会进入项目模式识别阶段。

## 更新技能

```bash
# 删除旧 marketplace 目录
rm -rf ~/.claude/plugins/marketplaces/coral-frontend-workflow

# 重新安装
python scripts/install.py --clone
```

## 卸载

```bash
python scripts/install.py --uninstall
```
