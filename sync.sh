#!/bin/bash
# Looply 文档自动同步脚本
# 用法: ./sync.sh          (手动同步一次)
#       ./sync.sh --watch   (持续监控，文件变化自动同步)

REPO_DIR="$HOME/looply-docs"

# 模块配置：本地源目录 → 仓库目标目录
declare -A MODULES
MODULES["$HOME/Desktop/海外业务登录注册"]="docs"
MODULES["$HOME/Desktop/海外业务首页"]="docs-首页"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

sync_files() {
    echo -e "${YELLOW}[同步中]${NC} 检查文件变化..."

    for SOURCE_DIR in "${!MODULES[@]}"; do
        TARGET="${MODULES[$SOURCE_DIR]}"

        # 产品架构图 - SVG
        if [ -d "$SOURCE_DIR/产品架构图" ]; then
            mkdir -p "$REPO_DIR/$TARGET/产品架构图"
            for f in "$SOURCE_DIR/产品架构图/"*.svg; do
                [ -f "$f" ] && cp "$f" "$REPO_DIR/$TARGET/产品架构图/"
            done
        fi

        # 实体关系图 - HTML
        if [ -d "$SOURCE_DIR/实体关系图" ]; then
            mkdir -p "$REPO_DIR/$TARGET/实体关系图"
            for f in "$SOURCE_DIR/实体关系图/"*.html; do
                [ -f "$f" ] && cp "$f" "$REPO_DIR/$TARGET/实体关系图/"
            done
        fi

        # 系统流程图 - SVG
        if [ -d "$SOURCE_DIR/系统流程图" ]; then
            mkdir -p "$REPO_DIR/$TARGET/系统流程图"
            for f in "$SOURCE_DIR/系统流程图/"*.svg; do
                [ -f "$f" ] && cp "$f" "$REPO_DIR/$TARGET/系统流程图/"
            done
        fi

        # PRD - docx 和 md
        if [ -d "$SOURCE_DIR/PRD" ]; then
            mkdir -p "$REPO_DIR/$TARGET/PRD"
            for f in "$SOURCE_DIR/PRD/"*.docx "$SOURCE_DIR/PRD/"*.md; do
                [ -f "$f" ] && cp "$f" "$REPO_DIR/$TARGET/PRD/"
            done
        fi

        # UI 设计稿 - pen 文件
        if [ -d "$SOURCE_DIR/UI" ]; then
            mkdir -p "$REPO_DIR/$TARGET/UI"
            for f in "$SOURCE_DIR/UI/"*.pen; do
                [ -f "$f" ] && cp "$f" "$REPO_DIR/$TARGET/UI/"
            done
        fi
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
for SOURCE_DIR in "${!MODULES[@]}"; do
    echo "  监控目录: $SOURCE_DIR"
done
echo ""

# 用 fswatch 或 fallback 到轮询
if command -v fswatch &> /dev/null; then
    WATCH_DIRS=()
    for SOURCE_DIR in "${!MODULES[@]}"; do
        for sub in 产品架构图 实体关系图 系统流程图 PRD UI; do
            [ -d "$SOURCE_DIR/$sub" ] && WATCH_DIRS+=("$SOURCE_DIR/$sub")
        done
    done
    fswatch -r -l 5 "${WATCH_DIRS[@]}" | while read -r event; do
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
