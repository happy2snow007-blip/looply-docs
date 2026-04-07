#!/bin/bash
# Looply 文档自动同步脚本
# 用法: ./sync.sh          (手动同步一次)
#       ./sync.sh --watch   (持续监控，文件变化自动同步)

REPO_DIR="$HOME/looply-docs"

# 模块配置：源目录|目标目录（用 | 分隔）
MODULE_LIST=(
    "$HOME/Desktop/海外业务登录注册|docs"
    "$HOME/Desktop/海外业务首页|docs-首页"
)

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 只在文件内容有变化时才复制（避免刷新未改动文件的修改时间）
# 兜底：源文件 mtime 更新时强制复制（防 Pencil MCP 延迟写入导致 cmp 误判）
smart_cp() {
    local src="$1" dst="$2"
    # 如果目标是目录，拼上文件名
    if [ -d "$dst" ]; then
        dst="$dst/$(basename "$src")"
    fi
    if [ ! -f "$dst" ]; then
        cp "$src" "$dst"
    elif ! cmp -s "$src" "$dst"; then
        cp "$src" "$dst"
    elif [ "$src" -nt "$dst" ]; then
        cp "$src" "$dst"
    fi
}

sync_files() {
    echo -e "${YELLOW}[同步中]${NC} 检查文件变化..."

    for ENTRY in "${MODULE_LIST[@]}"; do
        SOURCE_DIR="${ENTRY%%|*}"
        TARGET="${ENTRY##*|}"

        # 调研 - md
        if [ -d "$SOURCE_DIR/调研" ]; then
            mkdir -p "$REPO_DIR/$TARGET/调研"
            for f in "$SOURCE_DIR/调研/"*.md; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/调研/"
            done
        fi

        # 产品架构图 - SVG
        if [ -d "$SOURCE_DIR/产品架构图" ]; then
            mkdir -p "$REPO_DIR/$TARGET/产品架构图"
            for f in "$SOURCE_DIR/产品架构图/"*.svg; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/产品架构图/"
            done
        fi

        # 实体关系图 - HTML
        if [ -d "$SOURCE_DIR/实体关系图" ]; then
            mkdir -p "$REPO_DIR/$TARGET/实体关系图"
            for f in "$SOURCE_DIR/实体关系图/"*.html; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/实体关系图/"
            done
        fi

        # 系统流程图 - SVG
        if [ -d "$SOURCE_DIR/系统流程图" ]; then
            mkdir -p "$REPO_DIR/$TARGET/系统流程图"
            for f in "$SOURCE_DIR/系统流程图/"*.svg; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/系统流程图/"
            done
        fi

        # PRD - docx 和 md
        if [ -d "$SOURCE_DIR/PRD" ]; then
            mkdir -p "$REPO_DIR/$TARGET/PRD"
            for f in "$SOURCE_DIR/PRD/"*.docx "$SOURCE_DIR/PRD/"*.md; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/PRD/"
            done
            # 自动将最新版 md 复制为 latest.md（供在线阅读页使用）
            LATEST_MD=$(ls -t "$SOURCE_DIR/PRD/"*.md 2>/dev/null | head -1)
            if [ -n "$LATEST_MD" ]; then
                smart_cp "$LATEST_MD" "$REPO_DIR/$TARGET/PRD/latest.md"
            fi
        fi

        # 评审记录 - md
        if [ -d "$SOURCE_DIR/评审记录" ]; then
            mkdir -p "$REPO_DIR/$TARGET/评审记录"
            for f in "$SOURCE_DIR/评审记录/"*.md; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/评审记录/"
            done
        fi

        # 验收记录 - md
        if [ -d "$SOURCE_DIR/验收记录" ]; then
            mkdir -p "$REPO_DIR/$TARGET/验收记录"
            for f in "$SOURCE_DIR/验收记录/"*.md; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/验收记录/"
            done
        fi

        # UI 设计稿 - pen 文件
        if [ -d "$SOURCE_DIR/UI" ]; then
            mkdir -p "$REPO_DIR/$TARGET/UI"
            for f in "$SOURCE_DIR/UI/"*.pen; do
                [ -f "$f" ] && smart_cp "$f" "$REPO_DIR/$TARGET/UI/"
            done
        fi
    done

    # 检查 git 是否有变化
    cd "$REPO_DIR"
    if [ -n "$(git status --porcelain)" ]; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
        git add -A
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
for ENTRY in "${MODULE_LIST[@]}"; do
    SOURCE_DIR="${ENTRY%%|*}"
    echo "  监控目录: $SOURCE_DIR"
done
echo ""

# 用 fswatch 或 fallback 到轮询
if command -v fswatch &> /dev/null; then
    WATCH_DIRS=()
    for ENTRY in "${MODULE_LIST[@]}"; do
        SOURCE_DIR="${ENTRY%%|*}"
        for sub in 调研 产品架构图 实体关系图 系统流程图 PRD 评审记录 验收记录 UI; do
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
