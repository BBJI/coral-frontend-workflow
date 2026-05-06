#!/usr/bin/env python3
"""
Coral Frontend Workflow Plugin 一键安装脚本

通过 Claude Code 的 marketplace 机制安装 coral-frontend-workflow 插件。

用法:
  # 一键安装（推荐）
  git clone --depth 1 https://github.com/BBJI/coral-frontend-workflow.git /tmp/cfw && python /tmp/cfw/scripts/install.py && rm -rf /tmp/cfw

  # 从已克隆的仓库运行
  python scripts/install.py

  # 自动克隆并安装
  python scripts/install.py --clone

  # 使用 SSH 克隆
  python scripts/install.py --clone --ssh

  # 卸载
  python scripts/install.py --uninstall
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── 常量 ────────────────────────────────────────────────

PLUGIN_NAME = "coral-frontend-workflow"
MARKETPLACE_NAME = "coral-frontend-workflow"
REPO_URL_HTTPS = "https://github.com/BBJI/coral-frontend-workflow.git"
REPO_URL_SSH = "git@github.com:BBJI/coral-frontend-workflow.git"

CLAUDE_DIR = Path.home() / ".claude"
PLUGINS_DIR = CLAUDE_DIR / "plugins"
MARKETPLACES_DIR = PLUGINS_DIR / "marketplaces"
CACHE_DIR = PLUGINS_DIR / "cache"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
KNOWN_MARKETPLACES_FILE = PLUGINS_DIR / "known_marketplaces.json"
INSTALLED_PLUGINS_FILE = PLUGINS_DIR / "installed_plugins.json"

MARKETPLACE_INSTALL_DIR = MARKETPLACES_DIR / MARKETPLACE_NAME


def get_plugin_version_from_source(source_dir: Path) -> str:
    plugin_json = source_dir / ".claude-plugin" / "plugin.json"
    if plugin_json.exists():
        try:
            with open(plugin_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("version", "1.0.0")
        except (json.JSONDecodeError, OSError):
            pass
    return "1.0.0"


PLUGIN_VERSION = get_plugin_version_from_source(
    MARKETPLACE_INSTALL_DIR
) if MARKETPLACE_INSTALL_DIR.exists() else get_plugin_version_from_source(
    Path(__file__).resolve().parent.parent
)
PLUGIN_CACHE_DIR = CACHE_DIR / MARKETPLACE_NAME / PLUGIN_NAME / PLUGIN_VERSION

# ─── 工具函数 ────────────────────────────────────────────


def print_step(msg: str) -> None:
    print(f"\n\033[1;36m[步骤]\033[0m {msg}")


def print_ok(msg: str) -> None:
    print(f"\033[1;32m[成功]\033[0m {msg}")


def print_warn(msg: str) -> None:
    print(f"\033[1;33m[警告]\033[0m {msg}")


def print_error(msg: str) -> None:
    print(f"\033[1;31m[错误]\033[0m {msg}")


def load_json(path: Path) -> dict:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_repo_root() -> Path | None:
    script_parent = Path(__file__).resolve().parent.parent
    if (script_parent / ".claude-plugin" / "plugin.json").exists():
        return script_parent
    current = Path.cwd()
    for _ in range(5):
        if (current / ".claude-plugin" / "plugin.json").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def get_git_commit_sha(repo_dir: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=str(repo_dir)
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "unknown"


# ─── 安装逻辑 ────────────────────────────────────────────


def clone_repo(repo_url: str, target_dir: Path) -> bool:
    print_step(f"正在从 {repo_url} 克隆仓库...")
    try:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(target_dir)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print_error(f"克隆失败: {result.stderr.strip()}")
            print_warn("提示: 如果是私有仓库，请确保已配置 Git 凭证")
            return False
        print_ok("仓库克隆成功")
        return True
    except FileNotFoundError:
        print_error("未找到 git 命令，请先安装 Git")
        return False


def clone_to_marketplace(repo_url: str) -> bool:
    print_step("正在安装 marketplace...")
    return clone_repo(repo_url, MARKETPLACE_INSTALL_DIR)


def setup_cache() -> bool:
    print_step("正在设置插件缓存...")
    source = MARKETPLACE_INSTALL_DIR
    if not source.exists():
        print_error(f"Marketplace 目录不存在: {source}")
        return False

    PLUGIN_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    items_to_copy = [".claude", ".claude-plugin", "references", "scripts"]
    optional_items = ["LICENSE", "README.md", "INSTALL.md", "evals"]

    for item in items_to_copy:
        src = source / item
        dst = PLUGIN_CACHE_DIR / item
        if not src.exists():
            print_warn(f"  跳过不存在的必需项: {item}")
            continue
        try:
            if dst.exists():
                shutil.rmtree(dst)
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        except OSError as e:
            print_error(f"  复制 {item} 失败: {e}")
            return False

    for item in optional_items:
        src = source / item
        dst = PLUGIN_CACHE_DIR / item
        if src.exists():
            try:
                if dst.exists() and dst.is_dir():
                    shutil.rmtree(dst)
                if src.is_dir():
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            except OSError:
                pass

    print_ok(f"插件缓存已设置: {PLUGIN_CACHE_DIR}")
    return True


def register_known_marketplace(repo_url: str) -> bool:
    print_step("正在注册 marketplace...")
    data = load_json(KNOWN_MARKETPLACES_FILE)
    data[MARKETPLACE_NAME] = {
        "source": {
            "source": "git",
            "url": repo_url,
        },
        "installLocation": str(MARKETPLACE_INSTALL_DIR).replace("\\", "/"),
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }
    save_json(KNOWN_MARKETPLACES_FILE, data)
    print_ok("Marketplace 已注册")
    return True


def register_installed_plugin() -> bool:
    print_step("正在注册已安装插件...")
    data = load_json(INSTALLED_PLUGINS_FILE)
    if "version" not in data:
        data["version"] = 2
    if "plugins" not in data:
        data["plugins"] = {}

    plugin_key = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
    now = datetime.now(timezone.utc).isoformat()
    commit_sha = get_git_commit_sha(MARKETPLACE_INSTALL_DIR)

    data["plugins"][plugin_key] = [
        {
            "scope": "user",
            "installPath": str(PLUGIN_CACHE_DIR).replace("\\", "/"),
            "version": PLUGIN_VERSION,
            "installedAt": now,
            "lastUpdated": now,
            "gitCommitSha": commit_sha,
        }
    ]
    save_json(INSTALLED_PLUGINS_FILE, data)
    print_ok("已安装插件已注册")
    return True


def register_settings(repo_url: str) -> bool:
    print_step("正在注册插件到 Claude Code 设置...")
    settings = load_json(SETTINGS_FILE)

    plugin_key = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
    if "enabledPlugins" not in settings:
        settings["enabledPlugins"] = {}
    settings["enabledPlugins"][plugin_key] = True

    if PLUGIN_NAME in settings.get("enabledPlugins", {}):
        del settings["enabledPlugins"][PLUGIN_NAME]

    if "extraKnownMarketplaces" not in settings:
        settings["extraKnownMarketplaces"] = {}
    settings["extraKnownMarketplaces"][MARKETPLACE_NAME] = {
        "source": {
            "source": "git",
            "url": repo_url,
        }
    }

    if "plugins" in settings:
        del settings["plugins"]

    save_json(SETTINGS_FILE, settings)
    print_ok("插件已注册到 Claude Code 设置")
    return True


def verify_installation() -> bool:
    print_step("正在验证安装...")
    checks = []

    if MARKETPLACE_INSTALL_DIR.exists():
        checks.append(("Marketplace 目录", True, str(MARKETPLACE_INSTALL_DIR)))
    else:
        checks.append(("Marketplace 目录", False, "目录不存在"))

    plugin_json = MARKETPLACE_INSTALL_DIR / ".claude-plugin" / "plugin.json"
    if plugin_json.exists():
        from importlib import reload
        import __main__
        version = get_plugin_version_from_source(MARKETPLACE_INSTALL_DIR)
        checks.append(("plugin.json", True, f"版本 {version}"))
    else:
        checks.append(("plugin.json", False, "文件不存在"))

    skills_dir = MARKETPLACE_INSTALL_DIR / ".claude" / "skills"
    if skills_dir.exists():
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        checks.append(("Skills 目录", True, f"{skill_count} 个技能"))
    else:
        checks.append(("Skills 目录", False, "目录不存在"))

    if PLUGIN_CACHE_DIR.exists():
        checks.append(("插件缓存", True, str(PLUGIN_CACHE_DIR)))
    else:
        checks.append(("插件缓存", False, "目录不存在"))

    km_data = load_json(KNOWN_MARKETPLACES_FILE)
    if MARKETPLACE_NAME in km_data:
        checks.append(("Marketplace 注册", True, "已注册"))
    else:
        checks.append(("Marketplace 注册", False, "未注册"))

    ip_data = load_json(INSTALLED_PLUGINS_FILE)
    plugin_key = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
    if plugin_key in ip_data.get("plugins", {}):
        checks.append(("插件安装记录", True, "已记录"))
    else:
        checks.append(("插件安装记录", False, "未记录"))

    settings = load_json(SETTINGS_FILE)
    plugin_enabled = settings.get("enabledPlugins", {}).get(plugin_key, False)
    checks.append(("设置启用", plugin_enabled, "已启用" if plugin_enabled else "未启用"))

    extra_mk = MARKETPLACE_NAME in settings.get("extraKnownMarketplaces", {})
    checks.append(("Marketplace 设置", extra_mk, "已配置" if extra_mk else "未配置"))

    all_ok = True
    print()
    for name, ok, detail in checks:
        status = "\033[1;32mOK\033[0m" if ok else "\033[1;31mX\033[0m"
        print(f"  {status} {name}: {detail}")
        if not ok:
            all_ok = False

    return all_ok


def uninstall_plugin() -> None:
    print_step("正在卸载 coral-frontend-workflow 插件...")

    if MARKETPLACE_INSTALL_DIR.exists():
        shutil.rmtree(MARKETPLACE_INSTALL_DIR)
        print_ok(f"已删除 marketplace 目录: {MARKETPLACE_INSTALL_DIR}")
    else:
        print_warn("Marketplace 目录不存在，跳过删除")

    cache_base = CACHE_DIR / MARKETPLACE_NAME
    if cache_base.exists():
        shutil.rmtree(cache_base)
        print_ok(f"已删除插件缓存目录: {cache_base}")
    else:
        print_warn("插件缓存目录不存在，跳过删除")

    km_data = load_json(KNOWN_MARKETPLACES_FILE)
    if MARKETPLACE_NAME in km_data:
        del km_data[MARKETPLACE_NAME]
        save_json(KNOWN_MARKETPLACES_FILE, km_data)
        print_ok("已从 known_marketplaces.json 移除")

    ip_data = load_json(INSTALLED_PLUGINS_FILE)
    plugin_key = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
    if plugin_key in ip_data.get("plugins", {}):
        del ip_data["plugins"][plugin_key]
        save_json(INSTALLED_PLUGINS_FILE, ip_data)
        print_ok("已从 installed_plugins.json 移除")

    settings = load_json(SETTINGS_FILE)
    changed = False

    if "enabledPlugins" in settings and plugin_key in settings["enabledPlugins"]:
        del settings["enabledPlugins"][plugin_key]
        changed = True
    if "enabledPlugins" in settings and PLUGIN_NAME in settings["enabledPlugins"]:
        del settings["enabledPlugins"][PLUGIN_NAME]
        changed = True
    if "extraKnownMarketplaces" in settings and MARKETPLACE_NAME in settings["extraKnownMarketplaces"]:
        del settings["extraKnownMarketplaces"][MARKETPLACE_NAME]
        changed = True
    if "plugins" in settings:
        del settings["plugins"]
        changed = True

    if changed:
        save_json(SETTINGS_FILE, settings)
        print_ok("已从 Claude Code 设置中移除插件")

    print_ok("卸载完成")


# ─── 主函数 ────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Coral Frontend Workflow Plugin 一键安装脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/install.py                              # 从当前仓库安装
  python scripts/install.py --clone                      # 自动克隆并安装
  python scripts/install.py --clone --ssh                # 使用 SSH 克隆
  python scripts/install.py --uninstall                  # 卸载插件
""",
    )
    parser.add_argument("--clone", action="store_true", help="自动从 GitHub 克隆仓库并安装")
    parser.add_argument("--repo", default=None, help="指定仓库 URL")
    parser.add_argument("--ssh", action="store_true", help="使用 SSH URL 克隆")
    parser.add_argument("--uninstall", action="store_true", help="卸载插件")

    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  Coral Frontend Workflow Plugin 安装程序")
    print("=" * 60)

    if args.uninstall:
        uninstall_plugin()
        return

    repo_url = args.repo or (REPO_URL_SSH if args.ssh else REPO_URL_HTTPS)
    repo_root = None

    if args.clone:
        if not clone_to_marketplace(repo_url):
            sys.exit(1)
        repo_root = MARKETPLACE_INSTALL_DIR
    else:
        repo_root = find_repo_root()
        if not repo_root:
            print_error("未找到 coral-frontend-workflow 仓库")
            print("请使用以下方式之一:")
            print("  1. 在仓库目录中运行: python scripts/install.py")
            print("  2. 自动克隆安装: python scripts/install.py --clone")
            print("  3. 指定仓库 URL: python scripts/install.py --clone --repo <URL>")
            sys.exit(1)

        if repo_root != MARKETPLACE_INSTALL_DIR:
            print_step("正在将本地仓库同步到 marketplace 目录...")
            MARKETPLACES_DIR.mkdir(parents=True, exist_ok=True)
            if MARKETPLACE_INSTALL_DIR.exists():
                shutil.rmtree(MARKETPLACE_INSTALL_DIR)
            shutil.copytree(
                repo_root, MARKETPLACE_INSTALL_DIR,
                ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc')
            )
            print_ok("Marketplace 目录已准备")

    version = get_plugin_version_from_source(MARKETPLACE_INSTALL_DIR)
    print(f"\n  插件版本: {version}")
    print(f"  Marketplace: {MARKETPLACE_INSTALL_DIR}")

    success = True
    if success and not setup_cache():
        success = False
    if success and not register_known_marketplace(repo_url):
        success = False
    if success and not register_installed_plugin():
        success = False
    if success and not register_settings(repo_url):
        success = False
    if success and not verify_installation():
        success = False

    print()
    print("=" * 60)
    if success:
        print_ok("安装完成！")
        print()
        print("下一步操作:")
        print("  1. 重启 Claude Code（或重新加载 VSCode 窗口）")
        print("  2. 在 Claude Code 中输入: /coral-workflow <需求描述>")
        print()
        print("如需卸载: python scripts/install.py --uninstall")
    else:
        print_error("安装过程中出现错误，请检查上方输出")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
