#!/bin/bash
# Looply 文档自动同步脚本
# 用法: ./sync.sh          (手动同步一次)
#       ./sync.sh --watch   (持续监控，文件变化自动同步)

REPO_DIR="$HOME/looply-docs"
SOURCE_DIR="$HOME/Desktop/海外业务登录注册"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

sync_files() {
    echo -e "${YELLOW}[同步中]${NC} 检查文件变化..."

    CHANGED=0

    # 产品架构图 - 复制最新版 SVG
    for f in "$SOURCE_DIR/产品架构图/"*.svg; do
        [ -f "$f" ] && cp "$f" "$REPO_DIR/docs/产品架构图/" && CHANGED=1
    done

    # 实体关系图 - 复制 HTML
    for f in "$SOURCE_DIR/实体关系图/"*.html; do
        [ -f "$f" ] && cp "$f" "$REPO_DIR/docs/实体关系图/" && CHANGED=1
    done

    # 系统流程图 - 复制 SVG
    for f in "$SOURCE_DIR/系统流程图/"*.svg; do
        [ -f "$f" ] && cp "$f" "$REPO_DIR/docs/系统流程图/" && CHANGED=1
    done

    # PRD - 复制 docx 和 md
    for f in "$SOURCE_DIR/PRD/"*.docx "$SOURCE_DIR/PRD/"*.md; do
        [ -f "$f" ] && cp "$f" "$REPO_DIR/docs/PRD/" && CHANGED=1
    done

    # UI 设计稿 - 复制 pen 文件
    for f in "$SOURCE_DIR/UI/"*.pen; do
        [ -f "$f" ] && cp "$f" "$REPO_DIR/docs/UI/" && CHANGED=1
    done

    # 检查 git 是否有变化
    cd "$REPO_DIR"
    if [ -n "$(git status --porcelain)" ]; then
        git add -A
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
        git commit -m "sync: 文档更新 $TIMESTAMP"
        git push origin main 2>&1
        echo -e "${GREEN}[完成]${NC} 已同步并推送 ($TIMESTAMP)"
    else
        echo -e "${GREEN}[无变化]${NC} 文件没有更新"
    fi
}

# 手动同步模式
if [ "$1" != "--watch" ]; then
    sync_files
    exit 0
fi

# 监控模式
echo -e "${GREEN}[监控模式]${NC} 正在监控文件变化，按 Ctrl+C 停止"
echo "  监控目录: $SOURCE_DIR"
echo ""

# 用 fswatch（macOS 自带）或 fallback 到轮询
if command -v fswatch &> /dev/null; then
    fswatch -r -l 5 \
        "$SOURCE_DIR/产品架构图" \
        "$SOURCE_DIR/实体关系图" \
        "$SOURCE_DIR/系统流程图" \
        "$SOURCE_DIR/PRD" \
        "$SOURCE_DIR/UI" | while read -r event; do
        # 忽略 .DS_Store
        [[ "$event" == *".DS_Store"* ]] && continue
        echo -e "${YELLOW}[检测到变化]${NC} $event"
        sync_files
    done
else
    echo "  (未安装 fswatch，使用 30 秒轮询模式)"
    while true; do
        sync_files
        sleep 30
    done
fi
